package com.simpledoc.network.api

import retrofit2.http.Body
import retrofit2.http.POST
import com.simpledoc.network.models.ExplainRequest
import com.simpledoc.network.models.ExplainResponse

/**
 * API interface for /explain endpoint.
 */
interface ExplainApi {
    @POST("/explain")
    suspend fun explain(@Body request: ExplainRequest): ExplainResponse
}

