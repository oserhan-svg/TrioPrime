#!/usr/bin/env python3
"""
Review Agent - Reviews suggestions and makes final decision
"""
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Decision(Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    RETRY = "RETRY"

def review_suggestions(suggestion_result: Dict, image_path: str) -> Dict:
    """Review suggestions and make final decision"""
    try:
        quality_score = suggestion_result.get("quality_score", 50)
        suggestions = suggestion_result.get("suggestions", [])
        issues = suggestion_result.get("issues_found", [])
        recommendation = suggestion_result.get("recommendation", "RETRY")
        
        # Check for critical issues
        critical_issues = [s for s in suggestion_result.get("suggestions", []) if s.get("priority") == "CRITICAL"]
        high_priority = [s for s in suggestion_result.get("suggestions", []) if s.get("priority") == "HIGH"]
        
        # Decision logic
        if any(s.get("priority") == "CRITICAL" for s in suggestion_result.get("suggestions", [])):
            decision = "REJECT"
            reason = f"Critical issues found: {[s.get('action') for s in suggestion_result.get('suggestions', []) if s.get('priority') == 'CRITICAL']}"
        elif recommendation == "REJECT":
            decision = "REJECT"
            reason = f"Quality issues: {', '.join(suggestion_result.get('issues_found', []))}"
        elif recommendation == "RETRY":
            decision = "RETRY"
            reason = "Needs manual review"
        elif quality_score >= 70 and "screenshot" not in suggestion_result.get("issues_found", []):
            decision = "APPROVE"
            reason = f"Quality score: {quality_score}, issues: {', '.join(suggestion_result.get('issues_found', [])) if suggestion_result.get('issues_found') else 'none'}"
        else:
            decision = "REJECT"
            reason = f"Quality score too low: {quality_score}, issues: {', '.join(suggestion_result.get('issues_found', []))}"
        
        return {
            "decision": decision,
            "reason": reason,
            "quality_score": quality_score,
            "issues": suggestion_result.get("issues_found", []),
            "timestamp": datetime.now().isoformat(),
            "reviewed_by": "review-agent"
        }
        
    except Exception as e:
        logger.error(f"Review agent error: {e}")
        return {"decision": "RETRY", "reason": f"Review error: {e}"}

if __name__ == "__main__":
    print("Review Agent - Ready to review suggestions")