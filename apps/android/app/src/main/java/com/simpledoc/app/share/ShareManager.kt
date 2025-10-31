package com.simpledoc.app.share

import android.content.Context
import android.content.Intent
import android.net.Uri

/**
 * Manages WhatsApp sharing and local reminders.
 * 
 * TODO: Implement WhatsApp share with pre-filled message
 * TODO: Add "For learning" watermark to shared content
 * TODO: Implement local notification reminders for payment due dates
 */
class ShareManager(private val context: Context) {
    
    /**
     * Share document explanation to WhatsApp.
     * 
     * @param summary Plain-language summary
     * @param docType Document type
     */
    fun shareToWhatsApp(summary: String, docType: String) {
        val message = buildWhatsAppMessage(summary, docType)
        
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            `package` = "com.whatsapp"
            putExtra(Intent.EXTRA_TEXT, message)
        }
        
        try {
            context.startActivity(intent)
        } catch (e: Exception) {
            // Fallback to generic share if WhatsApp not installed
            val genericIntent = Intent(Intent.ACTION_SEND).apply {
                type = "text/plain"
                putExtra(Intent.EXTRA_TEXT, message)
            }
            context.startActivity(Intent.createChooser(genericIntent, "Share via"))
        }
    }
    
    /**
     * Share referral code via WhatsApp.
     */
    fun shareReferralCode(referralCode: String) {
        val message = "Get 7 days free on SimpleDoc! Use code: $referralCode"
        
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            `package` = "com.whatsapp"
            putExtra(Intent.EXTRA_TEXT, message)
        }
        
        context.startActivity(intent)
    }
    
    private fun buildWhatsAppMessage(summary: String, docType: String): String {
        return """
            📄 SimpleDoc Summary: ${docType.replace("-", " ").replaceFirstChar { it.uppercase() }}
            
            $summary
            
            For learning purposes only.
        """.trimIndent()
    }
}

