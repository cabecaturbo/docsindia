package com.simpledoc.network.models

import kotlinx.serialization.Serializable

@Serializable
data class DocType(
    val id: String,
    val version: String,
    val issuers: List<String> = emptyList()
)

@Serializable
data class TemplatesResponse(
    val docTypes: List<DocType>
)

