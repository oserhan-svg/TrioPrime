#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NVIDIA AI Model Client — NVIDIA AI Foundation Models API (integrate.api.nvidia.com)
"""
import os
import sys
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
_ENV_PATH = Path(__file__).resolve().parent / ".env"
if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH)

# Configuration
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_ORG_ID = os.getenv("NVIDIA_ORG_ID", "")
NVIDIA_API_BASE_URL = os.getenv("NVIDIA_API_BASE_URL", "https://integrate.api.nvidia.com/v1")
NVIDIA_DEFAULT_MODEL = os.getenv("NVIDIA_DEFAULT_MODEL", "google/gemma-3-30b-it")
NVIDIA_MAX_TOKENS = int(os.getenv("NVIDIA_MAX_TOKENS", "2048"))
NVIDIA_MIN_TOKENS = int(os.getenv("NVIDIA_MIN_TOKENS", "512"))
NVIDIA_TEMPERATURE = float(os.getenv("NVIDIA_TEMPERATURE", "0.7"))
NVIDIA_TIMEOUT = int(os.getenv("NVIDIA_TIMEOUT", "120"))


class NVIDIAAIError(Exception):
    """NVIDIA AI API exception."""
    pass


def _handle_response(resp: requests.Response, operation: str) -> dict:
    """Handle API response with proper error messages."""
    if resp.status_code == 200:
        return resp.json()
    # 404 means the endpoint or model is not available; don't mask it.
    if resp.status_code == 404:
        raise NVIDIAAIError(
            f"{operation} failed: 404 Not Found (endpoint/model might not be supported by this API key). "
            f"Status: {resp.status_code} | Body: {resp.text[:200]}"
        )
    raise NVIDIAAIError(
        f"{operation} failed: HTTP {resp.status_code}. "
        f"Body: {resp.text[:200]}"
    )


def get_available_models() -> list:
    """List all available NVIDIA AI models."""
    if not NVIDIA_API_KEY:
        raise NVIDIAAIError("NVIDIA_API_KEY not set. Check your .env file.")
    url = f"{NVIDIA_API_BASE_URL}/models"
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json",
    }
    # Add organization ID if available (NVIDIA NIM API)
    if NVIDIA_ORG_ID:
        headers["x-nvorg-id"] = NVIDIA_ORG_ID
    resp = requests.get(url, headers=headers, timeout=NVIDIA_TIMEOUT)
    return _handle_response(resp, "get_available_models").get("data", [])


def list_models() -> list:
    """Return list of available NVIDIA AI models."""
    models = get_available_models()
    return [{"id": m["id"], "owner": m.get("owned_by", "nvidia")} for m in models]


def chat_completion(
    model: str = None,
    messages: list = None,
    temperature: float = None,
    max_tokens: int = None,
    presence_penalty: float = 0.0,
    frequency_penalty: float = 0.0,
    stream: bool = False,
) -> dict:
    """
    Send a chat completion request to NVIDIA AI API.

    NOTE: The NVIDIA API key provided currently returns 404 for chat/completions
    endpoints. The models endpoint works correctly. This function will raise
    NVIDIAAIError with a descriptive message if the endpoint is not available.

    Args:
        model: Model ID (defaults to NVIDIA_DEFAULT_MODEL)
        messages: List of message dicts [{role, content}, ...]
        temperature: Sampling temperature (0.0-2.0)
        max_tokens: Max tokens to generate
        presence_penalty: Presence penalty (0.0-2.0)
        frequency_penalty: Frequency penalty (0.0-2.0)
        stream: Stream response or not

    Returns:
        Dict with full response
    """
    if not NVIDIA_API_KEY:
        raise NVIDIAAIError("NVIDIA_API_KEY not set. Check your .env file.")

    if model is None:
        model = NVIDIA_DEFAULT_MODEL
    if messages is None:
        messages = []
    if temperature is None:
        temperature = NVIDIA_TEMPERATURE
    if max_tokens is None:
        max_tokens = NVIDIA_MAX_TOKENS

    url = f"{NVIDIA_API_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
        "stream": stream,
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=NVIDIA_TIMEOUT)
    return _handle_response(resp, "chat_completion")


def chat_completion_text(
    model: str = None,
    messages: list = None,
    temperature: float = None,
    max_tokens: int = None,
) -> str:
    """Return only the text response from chat completion."""
    if messages is None:
        messages = []
    result = chat_completion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return result["choices"][0]["message"]["content"]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="NVIDIA AI Model Utility")
    parser.add_argument("--list-models", action="store_true", help="List available NVIDIA models")
    parser.add_argument("--chat", type=str, help="Chat message to send")
    parser.add_argument("--model", type=str, help="Model ID to use")
    parser.add_argument("--max-tokens", type=int, default=None, help="Max tokens")
    parser.add_argument("--temperature", type=float, default=None, help="Temperature")
    args = parser.parse_args()

    try:
        if args.list_models:
            models = list_models()
            print(f"Found {len(models)} models:")
            for m in models[:30]:
                print(f"  - {m['id']} ({m['owner']})")
            if len(models) > 30:
                print(f"  ... and {len(models)-30} more")

        if args.chat:
            result = chat_completion_text(
                model=args.model,
                messages=[{"role": "user", "content": args.chat}],
                temperature=args.temperature,
            )
            print("=" * 50)
            print("RESPONSE:")
            print("=" * 50)
            print(result)
    except NVIDIAAIError as e:
        print(f"NVIDIA AI Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
