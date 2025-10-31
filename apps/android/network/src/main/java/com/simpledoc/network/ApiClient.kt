package com.simpledoc.network

import com.simpledoc.network.api.ExplainApi
import com.simpledoc.network.api.TemplatesApi
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import java.util.concurrent.TimeUnit

/**
 * API client factory for SimpleDoc backend.
 * 
 * TODO: Configure base URL from BuildConfig or environment
 * TODO: Add authentication if needed
 * TODO: Add request interceptors for device ID, locale
 */
object ApiClient {
    
    private const val BASE_URL = "https://your-api-url.railway.app/" // TODO: Set actual URL
    
    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .addInterceptor(HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        })
        .build()
    
    private val json = Json {
        ignoreUnknownKeys = true
        isLenient = true
    }
    
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
        .build()
    
    val explainApi: ExplainApi = retrofit.create(ExplainApi::class.java)
    val templatesApi: TemplatesApi = retrofit.create(TemplatesApi::class.java)
}

