package com.simpledoc.app.utils

import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import java.util.Locale

/**
 * Helper for locale switching (English/Hindi).
 * 
 * TODO: Implement locale persistence (SharedPreferences)
 * TODO: Add more regional languages (post-MVP)
 */
object LocaleHelper {
    
    fun setLocale(context: Context, languageCode: String): Context {
        val locale = Locale(languageCode)
        Locale.setDefault(locale)
        
        val resources: Resources = context.resources
        val config: Configuration = resources.configuration
        config.setLocale(locale)
        
        return context.createConfigurationContext(config)
    }
    
    fun getCurrentLocale(): String {
        return Locale.getDefault().language
    }
    
    fun isHindi(): Boolean {
        return getCurrentLocale() == "hi"
    }
}

