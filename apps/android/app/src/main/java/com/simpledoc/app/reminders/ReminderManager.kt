package com.simpledoc.app.reminders

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import java.util.Calendar

/**
 * Manages local notification reminders for document actions.
 * 
 * TODO: Implement AlarmManager for payment reminders
 * TODO: Add WorkManager for more reliable scheduling
 * TODO: Handle reminder cancellation
 */
class ReminderManager(private val context: Context) {
    
    private val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
    
    /**
     * Schedule a payment reminder.
     * 
     * @param dueDate Due date in milliseconds
     * @param amount Amount due
     * @param reminderId Unique ID for this reminder
     */
    fun schedulePaymentReminder(dueDate: Long, amount: Double, reminderId: Int) {
        // Schedule reminder 1 day before due date
        val reminderTime = dueDate - (24 * 60 * 60 * 1000)
        
        val intent = Intent(context, ReminderReceiver::class.java).apply {
            putExtra("reminder_id", reminderId)
            putExtra("amount", amount)
            putExtra("due_date", dueDate)
            action = "com.simpledoc.app.REMINDER_ACTION"
        }
        
        val pendingIntent = PendingIntent.getBroadcast(
            context,
            reminderId,
            intent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
        
        alarmManager.setExactAndAllowWhileIdle(
            AlarmManager.RTC_WAKEUP,
            reminderTime,
            pendingIntent
        )
    }
    
    /**
     * Cancel a scheduled reminder.
     */
    fun cancelReminder(reminderId: Int) {
        val intent = Intent(context, ReminderReceiver::class.java)
        val pendingIntent = PendingIntent.getBroadcast(
            context,
            reminderId,
            intent,
            PendingIntent.FLAG_IMMUTABLE
        )
        alarmManager.cancel(pendingIntent)
    }
}

