package com.simpledoc.extractors

import org.json.JSONObject
import java.util.regex.Pattern

/**
 * Executes compiled JSON templates for field extraction.
 * 
 * TODO: Load templates from assets or API
 * TODO: Implement regex pattern matching with named groups
 * TODO: Apply post-processing rules (amount normalization, date parsing)
 * TODO: Calculate confidence scores
 */
class TemplateExtractor {
    
    /**
     * Extract fields from document text using a compiled template.
     * 
     * @param text Document text content
     * @param template Compiled JSON template
     * @return Map of field names to extracted values with confidence
     */
    fun extract(text: String, template: JSONObject): ExtractionResult {
        val fields = template.getJSONObject("fields")
        val extractions = mutableMapOf<String, Any>()
        val citations = mutableListOf<Citation>()
        
        fields.keys().forEach { fieldName ->
            val fieldDef = fields.getJSONObject(fieldName)
            val patterns = fieldDef.getJSONArray("patterns")
            
            for (i in 0 until patterns.length()) {
                val patternStr = patterns.getString(i)
                val pattern = Pattern.compile(patternStr)
                val matcher = pattern.matcher(text)
                
                if (matcher.find()) {
                    val value = matcher.group("value")
                    extractions[fieldName] = value ?: ""
                    citations.add(Citation(fieldName, "line:${matcher.start()}"))
                    break // Use first match
                }
            }
        }
        
        // Apply post-rules
        val postRules = template.optJSONArray("post_rules") ?: org.json.JSONArray()
        applyPostRules(extractions, postRules)
        
        val confidence = calculateConfidence(extractions, fields.length())
        
        return ExtractionResult(extractions, citations, confidence)
    }
    
    private fun applyPostRules(extractions: MutableMap<String, Any>, rules: org.json.JSONArray) {
        // TODO: Implement post-processing rules
        // - ensure_amount_numeric: Remove currency symbols, commas
        // - date_parsing: Normalize date formats
    }
    
    private fun calculateConfidence(extractions: Map<String, Any>, totalFields: Int): Double {
        if (totalFields == 0) return 0.0
        return extractions.size.toDouble() / totalFields
    }
}

data class ExtractionResult(
    val extractions: Map<String, Any>,
    val citations: List<Citation>,
    val confidence: Double
)

data class Citation(
    val field: String,
    val source: String
)

