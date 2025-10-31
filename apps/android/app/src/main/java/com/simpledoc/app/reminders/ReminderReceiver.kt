package com.simpledoc.app.reminders

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat

/**
 * Broadcast receiver for reminder notifications.
 * 
 * TODO: Implement notification display
 * TODO: Add notification channel setup
 */
class ReminderReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val reminderId = intent.getIntExtra("reminder_id", 0)
        val amount = intent.getDoubleExtra("amount", 0.0)
        val dueDate = intent.getLongExtra("due_date", 0L)
        
        // TODO: Create and show notification
        // val notification = NotificationCompat.Builder(context, CHANNEL_ID)
        //     .setContentTitle("Payment Reminder")
        //     .setContentText("You have ₹${amount} due")
        //     .setSmallIcon(R.drawable.ic_notification)
        //     .build()
        //
        // NotificationManagerCompat.from(context).notify(reminderId, notification)
    }
}

