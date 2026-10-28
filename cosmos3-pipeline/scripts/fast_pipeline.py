#!/usr/bin/env python3
"""
Fast Pipeline - Llama 3.2 90B Vision Only
Simple, fast, effective - no Cosmos3 overhead
"""

import os
import json
import base64
import logging
import asyncio
import aiohttp
import aiofiles
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
VISION_MODEL = "meta/llama-3.2-90b-vision-instruct"

INPUT_DIR = Path("/workspace/data/input")
OUTPUT_DIR = Path("/workspace/output")
LOGS_DIR = Path("/workspace/logs")

MAX_CONCURRENT = 5
MAX_RETRIES = 3
READ_TIMEOUT = 120

class Decision(Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    RETRY = "RETRY"

class LlamaVisionClient:
    """Fast async Llama 3.2 90B Vision client"""
    
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        self.model = "meta/llama-3.2-90b-vision-instruct"
        self.url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.semaphore = asyncio.Semaphore(5)
        
    async def analyze(self, session: aiohttp.ClientSession, image_path: Path) -> Dict:
        async with self.semaphore:
            for attempt in range(3):
                try:
                    async with aiofiles.open(image_path, 'rb') as f:
                        content = await f.read()
                    b64 = base64.b64encode(content).decode('utf-8')
                    
                    timeout = aiohttp.ClientTimeout(total=120, connect=10)
                async with session.post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY')}", "Content-Type": "application/json"},
                json={"model": "meta/llama-3.2-90b-vision-instruct", "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this real estate photo for: logo, watermark (.com), plate, text, glitch/render errors, censorship bars, pixelation, download button, UI elements, screenshot artifacts. Return JSON with bbox coordinates."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                    ]
                }],
                "max_tokens": 2048,
                "temperature": 0.1
                },
                timeout=aiohttp.ClientTimeout(total=120, connect=10)
                ) as resp:
                
                if resp.status == 429:
                    await asyncio.sleep(10)
                    continue
                result = await resp.json()
                content = result['choices'][0]['message']['content']
                return {"success": True, "content": content}
                    
            except asyncio.TimeoutError:
                if attempt == 2:
                    return {"success": False, "error": "Timeout after 3 retries"}
                await asyncio.sleep(5 * (attempt + 1))
            except Exception as e:
                if attempt == 2:
                    return {"success": False, "error": str(e)}
                await asyncio.sleep(2)
        
        return {"success": False, "error": "Max retries exceeded"}

class SuggestionEngine:
    """Fast suggestion engine - no external API calls"""
    
    @staticmethod
    def analyze(analysis: Dict) -> Dict:
        analysis_data = analysis.get("parsed", {})
        
        if analysis_data.get("is_screenshot"):
            return [{"action": "reject", "priority": "CRITICAL", "reason": "Screenshot detected"}]
        
        if analysis_data.get("has_watermark") or analysis_data.get("has_glitch_artifacts") or analysis_data.get("has_censorship_bars"):
            return [{"action": "process_with_photocraft", "priority": "HIGH"}]
        
        quality = analysis_data.get("quality_score", 50)
        return {"recommendation": "APPROVE" if quality >= 70 else "REVIEW"}

class ReviewEngine:
    @staticmethod
    def review(suggestion_result: Dict) -> Dict:
        rec = suggestion_result.get("recommendation", "REVIEW")
        if isinstance(suggestion_result, list) and suggestion_result:
            rec = suggestion_result[0].get("action", "REVIEW")
        
        if isinstance(suggestion_result, list) and any(s.get("priority") == "CRITICAL" for s in suggestion_result):
            return {"decision": "REJECT", "reason": "Critical issues found"}
        
        rec = suggestion_result.get("recommendation", "REVIEW")
        if rec == "reject" or rec == "REJECT":
            return {"decision": "REJECT", "reason": "Critical issues"}
        elif rec == "REJECT":
            return {"decision": "REJECT", "reason": "Quality issues"}
        elif rec == "REVIEW":
            return {"decision": "REVIEW", "reason": "Needs review"}
        else:
            return {"decision": "APPROVE", "reason": "Quality acceptable"}

class FastPipeline:
    def __init__(self):
        self.vision = LlamaVisionClient()
        self.suggestion = SuggestionEngine()
        self.review = ReviewEngine()
        
    async def process_batch(self, image_paths: List[Path]) -> List[Dict]:
        connector = aiohttp.TCPConnector(limit=5, limit_per_host=5)
        timeout = aiohttp.ClientTimeout(total=120, connect=10)
        
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=120)) as session:
            tasks = [self.vision.analyze(session, img) for img in image_paths]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for img_path, result in zip(image_paths, results):
                if isinstance(result, Exception):
                    yield {"image": img_path.name, "error": str(result)}
                elif isinstance(result, dict) and result.get("success"):
                    content = result.get("content", "")
                    try:
                        json_match = re.search(r'\{.*\}', content, re.DOTALL)
                        analysis = json.loads(json_match.group()) if json_match else {}
                    except:
                        analysis = {}
                    
                    suggestion = SuggestionEngine.analyze({"parsed": analysis})
                    review = ReviewEngine.review(suggestion)
                    
                    yield {
                        "image": img_path.name,
                        "analysis": analysis,
                        "suggestion": suggestion,
                        "review": review
                    }
                else:
                    yield {"image": img_path.name, "error": str(result)}

async def main():
    if not os.getenv("NVIDIA_API_KEY"):
        print("NVIDIA_API_KEY not set!")
        return
    
    INPUT_DIR = Path("/workspace/data/input")
    images = list(Path("/workspace/data/input").glob("*.jpg"))[:5]
    
    print(f"Processing {len(images)} images...")
    pipeline = FastPipeline()
    
    async for result in pipeline.process_batch(list(Path("/workspace/data/input").glob("*.jpg"))[:5]):
        print(f"Done: {result}")

if __name__ == "__main__":
    asyncio.run(main())
