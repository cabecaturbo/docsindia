package com.simpledoc.network.models

import kotlinx.serialization.Serializable

@Serializable
data class DocMeta(
    val typeHint: String? = null,
    val pages: Int? = null
)

@Serializable
data class ExplainRequest(
    val docText: String,
    val docMeta: DocMeta,
    val locale: String,
    val hints: Boolean = false,
    val deviceId: String
)

