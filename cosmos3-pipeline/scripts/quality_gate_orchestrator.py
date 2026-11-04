#!/usr/bin/env python3
"""
Quality Gate Orchestrator - Cosmos3 Pipeline
Orchestrates: Scraping -> Sample Validation -> Suggestion -> Review -> Batch Processing
"""

import os
import json
import time
import logging
import redis
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
COSMOS3_URL = os.getenv("COSMOS3_URL", "http://cosmos3-validator:8000")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
PHOTOCRAFT_HOST = os.getenv("PHOTOCRAFT_HOST", "photocraft")
DATA_DIR = Path("/workspace/data")
OUTPUT_DIR = Path("/workspace/output")
LOGS_DIR = Path("/workspace/logs")

# Redis connection
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

class Decision(Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    RETRY = "RETRY"

@dataclass
class ValidationResult:
    image_path: str
    timestamp: str
    decision: Decision
    suggestion: Optional[Dict] = None
    review: Optional[Dict] = None
    cosmos3_analysis: Optional[Dict] = None
    metadata: Dict = None

@dataclass
class PipelineState:
    stage: str
    total_images: int
    processed: int
    approved: int
    rejected: int
    current_sample: Optional[str] = None
    started_at: str = None
    updated_at: str = None

class Cosmos3Validator:
    """Cosmos3 + Llama Vision API Client"""
    
    def __init__(self):
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.api_key = os.getenv("NVIDIA_API_KEY")
        self.model = "meta/llama-3.2-90b-vision-instruct"
        
    def validate_image(self, image_path: Path) -> Dict:
        """Validate single image with Cosmos3 + Llama 3.2 90B Vision"""
        try:
            with open(image_path, "rb") as f:
                b64 = base64.b64encode(open(image_path, "rb").read()).decode("utf-8")
            
            headers = {
                "Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY')}",
                "Content-Type": "application/json"
            }
            
            prompt = """Bu emlak fotoğrafını detaylı analiz et. Aşağıdaki öğeleri tespit et ve JSON formatında cevap ver:
{
  "has_logo": boolean,
  "has_watermark": boolean,
  "watermark_details": "string",
  "has_plate": boolean,
  "has_text": boolean,
  "text_regions": [{"bbox": [x,y,w,h], "text": "string"}],
  "has_glitch": boolean,
  "glitch_details": "string",
  "has_censorship_bars": boolean,
  "censorship_details": "string",
  "has_download_button": boolean,
  "has_ui_elements": boolean,
  "ui_elements_details": "string",
  "has_glitch_artifacts": boolean,
  "glitch_details": "string",
  "has_pixelation": boolean,
  "has_compression_artifacts": boolean,
  "is_screenshot": boolean,
  "screenshot_evidence": "string",
  "quality_score": 0-100,
  "issues": ["list of issues"],
  "bbox_detections": [{"type": "string", "bbox": [x,y,w,h], "confidence": 0-1}]
}"""
            
            headers = {
                "Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY')}",
                "Content-Type": "application/json"
            }
            
            with open(image_path, "rb") as f:
                b64 = base64.b64encode(open(image_path, "rb").read()).decode("utf-8")
            
            payload = {
                "model": "meta/llama-3.2-90b-vision-instruct",
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """Bu emlak fotoğrafını detaylı analiz et. 
Logo, watermark (.com gibi), plaka, metin, glitch/render hataları, 
sansür çubukları, pikselleşme, indirme butonu, UI elemanları, 
glitch/render hataları, sansür çubukları, pikselleşme, 
ekran görüntüsü kalıntıları var mı? 
Bbox koordinatlarıyla JSON formatında cevap ver."""},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(open(image_path, 'rb').read()).decode('utf-8')}"}}
                    ]
                }],
                "max_tokens": 4096,
                "temperature": 0.1
            }
            
            headers = {
                "Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY')}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY')}", "Content-Type": "application/json"},
                json={
                    "model": "meta/llama-3.2-90b-vision-instruct",
                    "messages": [{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Bu emlak fotoğrafını detaylı analiz et. Logo, watermark (.com gibi), plaka, metin, glitch/render hataları, sansür çubukları, pikselleşme, indirme butonu, UI elemanları var mı? Bbox koordinatlarıyla JSON formatında cevap ver."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(open(image_path, 'rb').read()).decode('utf-8')}"}}
                        ]
                    }],
                    "max_tokens": 4096,
                    "temperature": 0.1
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return {"success": True, "analysis": content}
            else:
                return {"success": False, "error": f"API Error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Cosmos3 validation error: {e}")
            return {"success": False, "error": str(e)}

class SuggestionAgent:
    """Subagent: Analyzes Cosmos3 output and provides suggestions"""
    
    def __init__(self):
        self.redis = redis_client
        
    def analyze(self, cosmos3_result: Dict, image_path: Path) -> Dict:
        """Analyze Cosmos3 output and provide suggestions"""
        try:
            # Parse Cosmos3 analysis
            analysis = cosmos3_result.get("analysis", "")
            
            # Parse JSON from analysis
            try:
                # Extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', analysis, re.DOTALL)
                if json_match:
                    analysis_data = json.loads(json_match.group())
                else:
                    analysis_data = {}
            except:
                analysis_data = {}
            
            # Generate suggestions based on findings
            suggestions = []
            issues = []
            
            if analysis_data.get("has_watermark"):
                suggestions.append({
                    "action": "remove_watermark",
                    "priority": "HIGH",
                    "method": "photocraft_content_aware",
                    "reason": "Watermark detected"
                })
                issues.append("watermark")
            
            if analysis_data.get("has_glitch_artifacts"):
                suggestions.append({
                    "action": "fix_glitch",
                    "priority": "HIGH",
                    "method": "photocraft_inpaint",
                    "reason": "Glitch artifacts detected"
                })
                issues.append("glitch")
            
            if analysis_data.get("has_censorship_bars"):
                suggestions.append({
                    "action": "remove_censorship",
                    "priority": "HIGH",
                    "method": "photocraft_inpaint",
                    "reason": "Censorship bars detected"
                })
                issues.append("censorship")
            
            if analysis_data.get("has_download_button") or analysis_data.get("has_ui_elements"):
                suggestions.append({
                    "action": "remove_ui_elements",
                    "priority": "MEDIUM",
                    "method": "photocraft_content_aware",
                    "reason": "UI elements detected (screenshot artifacts)"
                })
                issues.append("ui_elements")
            
            if analysis_data.get("has_glitch_artifacts"):
                suggestions.append({
                    "action": "fix_render_errors",
                    "priority": "HIGH",
                    "method": "photocraft_inpaint",
                    "reason": "Render/glitch artifacts detected"
                })
                issues.append("glitch")
            
            if analysis_data.get("is_screenshot"):
                suggestions.append({
                    "action": "flag_screenshot",
                    "priority": "HIGH",
                    "method": "reject",
                    "reason": "Image is a screenshot, not a clean photo"
                })
                issues.append("screenshot")
            
            quality_score = analysis_data.get("quality_score", 50)
            
            return {
                "image": str(Path(image_path).name),
                "timestamp": datetime.now().isoformat(),
                "quality_score": quality_score,
                "issues_found": issues,
                "suggestions": suggestions,
                "recommendation": "REJECT" if quality_score < 50 or "screenshot" in issues else "PROCESS_WITH_CAUTION",
                "cosmos3_analysis": analysis_data
            }
            
        except Exception as e:
            logger.error(f"Suggestion agent error: {e}")
            return {"error": str(e), "recommendation": "RETRY"}

class ReviewAgent:
    """Subagent: Reviews suggestions and makes final decision"""
    
    def __init__(self):
        self.redis = redis_client
        
    def review(self, suggestion_result: Dict, image_path: Path) -> Dict:
        """Review suggestions and make final decision"""
        try:
            recommendation = suggestion_result.get("recommendation", "RETRY")
            issues = suggestion_result.get("issues_found", [])
            quality_score = suggestion_result.get("quality_score", 50)
            
            # Decision logic
            if suggestion_result.get("recommendation") == "REJECT":
                decision = Decision.REJECT
                reason = f"Quality issues: {', '.join(issues)}"
            elif suggestion_result.get("recommendation") == "RETRY":
                decision = Decision.RETRY
                reason = "Needs manual review"
            elif quality_score >= 70 and "screenshot" not in issues:
                decision = Decision.APPROVE
                reason = f"Quality score: {quality_score}, issues: {', '.join(issues) if issues else 'none'}"
            else:
                decision = Decision.REJECT
                reason = f"Quality score too low: {quality_score}, issues: {', '.join(issues)}"
            
            return {
                "decision": decision.value,
                "reason": reason,
                "quality_score": quality_score,
                "issues": issues,
                "timestamp": datetime.now().isoformat(),
                "reviewed_by": "review-agent"
            }
            
        except Exception as e:
            logger.error(f"Review agent error: {e}")
            return {"decision": Decision.RETRY.value, "reason": f"Review error: {e}"}

class QualityGateOrchestrator:
    """Main orchestrator for the quality gate pipeline"""
    
    def __init__(self):
        self.cosmos3 = Cosmos3Validator()
        self.suggestion_agent = SuggestionAgent()
        self.review_agent = ReviewAgent()
        self.redis = redis_client
        self.state = PipelineState(
            stage="initializing",
            total_images=0,
            processed=0,
            approved=0,
            rejected=0,
            started_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
    def save_state(self):
        """Save pipeline state to Redis"""
        self.state.updated_at = datetime.now().isoformat()
        self.redis.set("pipeline:state", json.dumps(asdict(self.state)))
        
    def load_state(self):
        """Load pipeline state from Redis"""
        data = self.redis.get("pipeline:state")
        if data:
            data = json.loads(data)
            self.state = PipelineState(**data)
    
    def find_sample_image(self, input_dir: Path) -> Optional[Path]:
        """Find a sample image for validation"""
        images = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))
        if not images:
            return None
        
        # Find first unprocessed image
        processed = set()
        for f in Path("/workspace/output").glob("*_analysis.json"):
            processed.add(f.stem.replace("_analysis", ""))
        
        for img in images:
            if img.stem not in processed:
                return img
        return images[0] if images else None
    
    def run_sample_validation(self, image_path: Path) -> ValidationResult:
        """Run complete validation on a single sample image"""
        logger.info(f"🔍 Validating sample: {image_path.name}")
        
        # Step 1: Cosmos3 Validation
        logger.info("📡 Running Cosmos3 + Llama 90B Vision validation...")
        cosmos3_result = self.cosmos3.validate_image(image_path)
        
        if not cosmos3_result.get("success"):
            logger.error(f"Cosmos3 validation failed: {cosmos3_result.get('error')}")
            return ValidationResult(
                image_path=str(image_path),
                timestamp=datetime.now().isoformat(),
                decision=Decision.RETRY,
                cosmos3_analysis={"error": cosmos3_result.get("error")}
            )
        
        # Step 2: Suggestion Agent
        logger.info("🤖 Running Suggestion Agent...")
        suggestion_result = self.suggestion_agent.analyze(
            {"analysis": cosmos3_result["analysis"]}, 
            Path(image_path)
        )
        
        # Step 3: Review Agent
        logger.info("👁️ Running Review Agent...")
        review_result = self.review_agent.review(suggestion_result, image_path)
        
        # Determine final decision
        decision = Decision(review_result.get("decision", "RETRY"))
        
        return ValidationResult(
            image_path=str(image_path),
            timestamp=datetime.now().isoformat(),
            decision=decision,
            suggestion=dict(suggestion_result),
            review=review_result,
            cosmos3_analysis=json.loads(cosmos3_result["analysis"]) if cosmos3_result.get("success") else None,
            metadata={"quality_score": review_result.get("quality_score", 0)}
        )
    
    def run_batch_processing(self, input_dir: Path, output_dir: Path):
        """Run batch Photocraft processing on approved images"""
        logger.info(f"🚀 Starting batch processing: {input_dir} -> {output_dir}")
        
        # This would call Photocraft batch processing
        # For now, log the intent
        logger.info(f"Photocraft batch processing: {input_dir} -> {output_dir}")
        # TODO: Implement Photocraft batch processing via Docker exec
        
    def run(self):
        """Main orchestration loop"""
        logger.info("🚀 Quality Gate Orchestrator starting...")
        
        self.load_state()
        self.save_state()
        
        input_dir = Path("/workspace/data/input")
        output_dir = Path("/workspace/output")
        
        # Find all images
        all_images = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))
        self.state.total_images = len(all_images)
        self.save_state()
        
        logger.info(f"📸 Total images: {self.state.total_images}")
        
        # Phase 1: Sample Validation
        logger.info("🔍 Phase 1: Sample Validation")
        sample = self.find_sample_image(input_dir)
        
        if sample:
            logger.info(f"🔍 Validating sample: {sample.name}")
            self.state.current_sample = sample.name
            self.save_state()
            
            result = self.run_sample_validation(sample)
            
            # Log result
            logger.info(f"📋 Validation Result: {result.decision.value}")
            logger.info(f"   Reason: {result.review.get('reason', 'N/A')}")
            
            if result.decision == Decision.APPROVE:
                logger.info("✅ Sample APPROVED - Proceeding to batch processing")
                self.state.stage = "batch_processing"
                self.save_state()
                
                # Phase 2: Batch Processing
                self.run_batch_processing(input_dir, output_dir)
                self.state.stage = "completed"
                self.save_state()
                
            elif result.decision == Decision.REJECT:
                logger.warning("❌ Sample REJECTED - Pipeline stopped")
                self.state.stage = "rejected"
                self.save_state()
                
            else:
                logger.warning("🔄 Sample needs RETRY - Manual intervention needed")
                self.state.stage = "retry_needed"
                self.save_state()
        else:
            logger.error("❌ No images found for validation")
            self.state.stage = "error"
            self.save_state()

def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("🚀 COSMOS3 QUALITY GATE ORCHESTRATOR")
    logger.info("=" * 60)
    
    # Check environment
    if not os.getenv("NVIDIA_API_KEY"):
        logger.error("❌ NVIDIA_API_KEY not set!")
        return
    
    orchestrator = QualityGateOrchestrator()
    orchestrator.run()
    
    logger.info("✅ Pipeline completed")

if __name__ == "__main__":
    main()
EOF

chmod +x /home/rw/Projects/cosmos3-pipeline/scripts/quality_gate_orchestrator.py