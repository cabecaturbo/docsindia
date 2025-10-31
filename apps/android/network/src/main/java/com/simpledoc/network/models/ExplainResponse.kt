package com.simpledoc.network.models

import kotlinx.serialization.Serializable

@Serializable
data class Action(
    val label: String,
    val type: String,
    val payload: Map<String, String>
)

@Serializable
data class Citation(
    val field: String,
    val source: String
)

@Serializable
data class ExplainResponse(
    val summary: String,
    val extractions: Map<String, String>,
    val actions: List<Action>,
    val confidence: Double,
    val docType: String,
    val citations: List<Citation>
)

