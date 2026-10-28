#!/usr/bin/env python3
"""
Suggestion Agent - Analyzes Cosmos3 output and provides processing suggestions
"""
import os
import json
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_cosmos3_analysis(analysis_text: str) -> Dict:
    """Parse Cosmos3 analysis JSON from response"""
    try:
        # Extract JSON from response text
        json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        logger.warning(f"Failed to parse Cosmos3 analysis: {e}")
    return {}

def generate_suggestions(analysis_data: Dict, image_path: str) -> List[Dict]:
    """Generate processing suggestions based on Cosmos3 analysis"""
    suggestions = []
    issues = []
    
    if not analysis_data:
        return [{"action": "manual_review", "priority": "HIGH", "method": "manual", "reason": "Failed to parse analysis"}]
    
    # Watermark detection
    if analysis_data.get("has_watermark"):
        suggestions.append({
            "action": "remove_watermark",
            "priority": "HIGH",
            "method": "photocraft_content_aware",
            "reason": f"Watermark detected: {analysis_data.get('watermark_details', 'detected')}",
            "params": {"watermark_type": analysis_data.get("watermark_details", "unknown")}
        })
        issues.append("watermark")
    
    # Glitch/render artifacts
    if analysis_data.get("has_glitch_artifacts"):
        suggestions.append({
            "action": "fix_glitch",
            "priority": "HIGH",
            "method": "photocraft_inpaint",
            "reason": analysis_data.get("glitch_details", "Glitch artifacts detected"),
            "params": {"glitch_type": analysis_data.get("glitch_details", "unknown")}
        })
        issues.append("glitch")
    
    # Censorship bars
    if analysis_data.get("has_censorship_bars"):
        suggestions.append({
            "action": "remove_censorship",
            "priority": "HIGH",
            "method": "photocraft_inpaint",
            "reason": analysis_data.get("censorship_details", "Censorship bars detected"),
            "params": {"censorship_type": analysis_data.get("censorship_details", "bars")}
        })
        issues.append("censorship")
    
    # UI elements (screenshot artifacts)
    if analysis_data.get("has_download_button") or analysis_data.get("has_ui_elements"):
        suggestions.append({
            "action": "remove_ui_elements",
            "priority": "MEDIUM",
            "method": "photocraft_content_aware",
            "reason": analysis_data.get("ui_elements_details", "UI elements detected (screenshot artifacts)"),
            "params": {"element_types": ["download_button", "ui_elements"]}
        })
        issues.append("ui_elements")
    
    # Glitch artifacts
    if analysis_data.get("has_glitch_artifacts"):
        suggestions.append({
            "action": "fix_render_errors",
            "priority": "HIGH",
            "method": "photocraft_inpaint",
            "reason": analysis_data.get("glitch_details", "Render/glitch artifacts detected"),
            "params": {"glitch_type": analysis_data.get("glitch_details", "unknown")}
        })
        issues.append("glitch")
    
    # Screenshot detection
    if analysis_data.get("is_screenshot"):
        return [{
            "action": "flag_screenshot",
            "priority": "CRITICAL",
            "method": "reject",
            "reason": f"Image is a screenshot: {analysis_data.get('screenshot_evidence', 'UI elements detected')}",
            "params": {"screenshot_evidence": analysis_data.get("screenshot_evidence", "UI elements detected")}
        }]
    
    quality_score = analysis_data.get("quality_score", 50)
    
    return {
        "image": "",  # Will be filled by caller
        "timestamp": datetime.now().isoformat(),
        "quality_score": quality_score,
        "issues_found": issues,
        "suggestions": suggestions,
        "recommendation": "REJECT" if quality_score < 50 or "screenshot" in issues else "PROCESS_WITH_CAUTION",
        "cosmos3_analysis": {}
    }

if __name__ == "__main__":
    print("Suggestion Agent - Ready to process Cosmos3 analysis")