package com.simpledoc.network.api

import retrofit2.http.GET
import com.simpledoc.network.models.TemplatesResponse

/**
 * API interface for /templates endpoint.
 */
interface TemplatesApi {
    @GET("/templates")
    suspend fun getTemplates(): TemplatesResponse
}

