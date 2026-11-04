#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NVIDIA NIM Model Registry — Sisteme Tüm 83 Modeli Kataloglar

Bu modül, NVIDIA NIM API anahtarı ile erişilen 83 modeli sisteme
kaydeder ve yönetir.

Kullanım:
    from nvidia_registry import NVIDIA_MODEL_REGISTRY

    # Tüm modeller
    for model in NVIDIA_MODEL_REGISTRY:
        print(model['id'], model['owner'])

    # Model bilgisi
    model = NVIDIA_MODEL_REGISTRY['google/gemma-3-30b-it']

    # Model kategorilere göre filtreleme
    embed_models = NVIDIA_MODEL_REGISTRY.filter_by_category('embedding')
    chat_models = NVIDIA_MODEL_REGISTRY.filter_by_category('chat')
"""
import json
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# Registry dosyası yolu
_REGISTRY_PATH = Path(__file__).resolve().parent / "nvidia_model_registry.json"

# Mevcut model katalogı (83 model)
# NVIDIA NIM API'sinden alınan model listesi
# Kaynak: https://integrate.api.nvidia.com/v1/models
_NVIDIA_MODELS = [
    {"id": "01-ai/yi-large", "owner": "01-ai", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "adept/fuyu-8b", "owner": "adept", "category": "vision", "use_case": "Görsel işleme, çoklu modalite"},
    {"id": "ai21labs/jamba-1.5-large-instruct", "owner": "ai21labs", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "aisingapore/sea-lion-7b-instruct", "owner": "aisingapore", "category": "chat", "use_case": "Japonca da çalışan sohbet modeli"},
    {"id": "bigcode/starcoder2-15b", "owner": "bigcode", "category": "code", "use_case": "Kod üretimi, derleme"},
    {"id": "databricks/dbrx-instruct", "owner": "databricks", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "deepseek-ai/deepseek-coder-6.7b-instruct", "owner": "deepseek-ai", "category": "code", "use_case": "Kod üretimi, derleme, debug"},
    {"id": "deepseek-ai/deepseek-v4.1-flash", "owner": "deepseek-ai", "category": "chat", "use_case": "Hızlı sohbet, metin üretimi"},
    {"id": "google/codegemma-1.1-7b", "owner": "google", "category": "code", "use_case": "Kod üretimi, derleme"},
    {"id": "google/codegemma-7b", "owner": "google", "category": "code", "use_case": "Kod üretimi, derleme"},
    {"id": "google/deplot", "owner": "google", "category": "vision", "use_case": "Tablo ve grafik tanıma, veri çıkarma"},
    {"id": "google/diffusiongemma-26b-a4b-it", "owner": "google", "category": "vision", "use_case": "Görsel üretimi, image generation"},
    {"id": "google/gemma-2b", "owner": "google", "category": "chat", "use_case": "Hafif sohbet, metin üretimi"},
    {"id": "google/gemma-3-12b-it", "owner": "google", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "google/gemma-3-4b-it", "owner": "google", "category": "chat", "use_case": "Hafif sohbet, metin üretimi"},
    {"id": "google/gemma-4-31b-it", "owner": "google", "category": "chat", "use_case": "Gelişmiş sohbet, metin üretimi"},
    {"id": "google/recurrentgemma-2b", "owner": "google", "category": "chat", "use_case": "Zaman serisi, metin üretimi"},
    {"id": "ibm/granite-3.0-3b-a800m-instruct", "owner": "ibm", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "ibm/granite-3.0-8b-instruct", "owner": "ibm", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "ibm/granite-34b-code-instruct", "owner": "ibm", "category": "code", "use_case": "Kod üretimi, derleme, debug"},
    {"id": "ibm/granite-8b-code-instruct", "owner": "ibm", "category": "code", "use_case": "Kod üretimi, derleme"},
    {"id": "meta/codellama-70b", "owner": "meta", "category": "code", "use_case": "Kod üretimi, derleme, debug"},
    {"id": "meta/llama-3.2-11b-vision-instruct", "owner": "meta", "category": "vision", "use_case": "Görsel işleme, çoklu modalite"},
    {"id": "meta/llama-3.2-90b-vision-instruct", "owner": "meta", "category": "vision", "use_case": "Görsel işleme, çoklu modalite"},
    {"id": "meta/llama-guard-4-12b", "owner": "meta", "category": "safety", "use_case": "İçerik güvenliği, filtreleme"},
    {"id": "meta/llama2-70b", "owner": "meta", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "meta/muse-glimmer-30b", "owner": "meta", "category": "vision", "use_case": "Görsel üretimi, image generation"},
    {"id": "microsoft/kosmos-2", "owner": "microsoft", "category": "vision", "use_case": "Görsel-Metin uyumsuzluğu, image-text alignment"},
    {"id": "microsoft/phi-3-vision-128k-instruct", "owner": "microsoft", "category": "vision", "use_case": "Görsel işleme, çoklu modalite"},
    {"id": "microsoft/phi-3.5-moe-instruct", "owner": "microsoft", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "mistralai/codestral-22b-instruct-v0.1", "owner": "mistralai", "category": "code", "use_case": "Kod üretimi, derleme"},
    {"id": "mistralai/mistral-7b-instruct-v0.3", "owner": "mistralai", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "mistralai/mistral-large", "owner": "mistralai", "category": "chat", "use_case": "Gelişmiş sohbet, metin üretimi"},
    {"id": "mistralai/mistral-large-2-instruct", "owner": "mistralai", "category": "chat", "use_case": "Gelişmiş sohbet, metin üretimi"},
    {"id": "mistralai/mixtral-8x22b-v0.1", "owner": "mistralai", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "moonshotai/kimi-k2.6", "owner": "moonshotai", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "nv-mistralai/mistral-nemo-12b-instruct", "owner": "nv-mistralai", "category": "chat", "use_case": "Hızlı sohbet, metin üretimi"},
    {"id": "nvidia/ai-synthetic-video-detector", "owner": "nvidia", "category": "vision", "use_case": "Video sahte üretim tespiti, deepfake detection"},
    {"id": "nvidia/cosmos-reason2-8b", "owner": "nvidia", "category": "code", "use_case": "Kod üretimi, raporlama, automasyon"},
    {"id": "nvidia/embed-qa-4", "owner": "nvidia", "category": "embedding", "use_case": "Metin gömü, semantic search"},
    {"id": "nvidia/ising-calibration-1.5-31b", "owner": "nvidia", "category": "chat", "use_case": "Calibration, metin üretimi"},
    {"id": "nvidia/llama-3.1-nemoguard-8b-content-safety", "owner": "nvidia", "category": "safety", "use_case": "İçerik güvenliği, filtreleme"},
    {"id": "nvidia/llama-3.1-nemoguard-8b-topic-control", "owner": "nvidia", "category": "safety", "use_case": "Konu kontrolü, içerik filtreleme"},
    {"id": "nvidia/llama-3.1-nemotron-51b-instruct", "owner": "nvidia", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "nvidia/llama-3.1-nemotron-70b-instruct", "owner": "nvidia", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "nvidia/llama-3.1-nemotron-safety-guard-8b-v3", "owner": "nvidia", "category": "safety", "use_case": "İçerik güvenliği, filtreleme"},
    {"id": "nvidia/llama-3.1-nemotron-ultra-253b-v1", "owner": "nvidia", "category": "chat", "use_case": "Gelişmiş sohbet, metin üretimi"},
    {"id": "nvidia/llama-3.2-nemoretriever-1b-vlm-embed-v1", "owner": "nvidia", "category": "embedding", "use_case": "Görsel-Metin gömü, semantic search"},
    {"id": "nvidia/llama-3.2-nv-embedqa-1b-v1", "owner": "nvidia", "category": "embedding", "use_case": "QA gömü, semantic search"},
    {"id": "nvidia/llama-nemotron-embed-vl-1b-v2", "owner": "nvidia", "category": "embedding", "use_case": "Metin gömü, semantic search"},
    {"id": "nvidia/llama3-chatqa-1.5-70b", "owner": "nvidia", "category": "chat", "use_case": "QA sohbet, metin üretimi"},
    {"id": "nvidia/mistral-nemo-minitron-8b-8k-instruct", "owner": "nvidia", "category": "chat", "use_case": "Hızlı sohbet, metin üretimi"},
    {"id": "nvidia/nemotron-3-embed-1b", "owner": "nvidia", "category": "embedding", "use_case": "Metin gömü, semantic search"},
    {"id": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning", "owner": "nvidia", "category": "chat", "use_case": "Akıllı tutarlılık, hedef odaklı soyutlama"},
    {"id": "nvidia/nemotron-3-super-120b-a12b", "owner": "nvidia", "category": "chat", "use_case": "Gelişmiş sohbet, istikrarlı metin üretimi"},
    {"id": "nvidia/nemotron-3-ultra-550b-a55b", "owner": "nvidia", "category": "chat", "use_case": "Gelişmiş sohbet, metin üretimi"},
    {"id": "nvidia/nemotron-3.5-content-safety", "owner": "nvidia", "category": "safety", "use_case": "İçerik güvenliği, filtreleme"},
    {"id": "nvidia/nemotron-3.5-embed-1b", "owner": "nvidia", "category": "embedding", "use_case": "Metin gömü, semantic search"},
    {"id": "nvidia/nemotron-3.5-embed-8b", "owner": "nvidia", "category": "embedding", "use_case": "Metin gömü, semantic search"},
    {"id": "nvidia/nemotron-3.5-lightning-30b-a3b", "owner": "nvidia", "category": "chat", "use_case": "Hızlı sohbet, metin üretimi"},
    {"id": "nvidia/nemotron-3.5-super-vl-120b-a12b", "owner": "nvidia", "category": "vision", "use_case": "Görsel-Metin uyumsuzluğu, çoklu modalite"},
    {"id": "nvidia/nemotron-4-340b-instruct", "owner": "nvidia", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "nvidia/nemotron-4-340b-reward", "owner": "nvidia", "category": "code", "use_case": "Kod kalitesi, reward modeli"},
    {"id": "nvidia/nemotron-nano-3-30b-a3b", "owner": "nvidia", "category": "chat", "use_case": "Hafif sohbet, metin üretimi"},
    {"id": "nvidia/nemotron-parse", "owner": "nvidia", "category": "code", "use_case": "Metin parse, doküman işleme"},
    {"id": "nvidia/nemotron-parse-2.0", "owner": "nvidia", "category": "code", "use_case": "Metin parse, doküman işleme"},
    {"id": "nvidia/neva-22b", "owner": "nvidia", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "nvidia/nv-embedqa-mistral-7b-v2", "owner": "nvidia", "category": "embedding", "use_case": "QA gömü, semantic search"},
    {"id": "nvidia/nvclip", "owner": "nvidia", "category": "vision", "use_case": "Görsel-Metin embedding, çoklu modalite"},
    {"id": "nvidia/riva-translate-4b-instruct", "owner": "nvidia", "category": "translation", "use_case": "Dil çeviri, metin çevirisi"},
    {"id": "nvidia/riva-translate-4b-instruct-v2", "owner": "nvidia", "category": "translation", "use_case": "Dil çeviri, metin çevirisi"},
    {"id": "nvidia/vila", "owner": "nvidia", "category": "vision", "use_case": "Görsel üretimi, video generation"},
    {"id": "openai/gpt-oss-20b", "owner": "openai", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "poolside/laguna-xs-2.1", "owner": "poolside", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "snowflake/arctic-embed-l", "owner": "snowflake", "category": "embedding", "use_case": "Metin gömü, semantic search"},
    {"id": "stepfun-ai/step-5-preview", "owner": "stepfun-ai", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "writer/palmyra-creative-122b", "owner": "writer", "category": "chat", "use_case": "Yaratıcı metin üretimi"},
    {"id": "writer/palmyra-fin-70b-32k", "owner": "writer", "category": "chat", "use_case": "Finansal metin üretimi, analiz"},
    {"id": "writer/palmyra-med-70b", "owner": "writer", "category": "chat", "use_case": "Tıp metinleri üretimi, analiz"},
    {"id": "writer/palmyra-med-70b-32k", "owner": "writer", "category": "chat", "use_case": "Tıp metinleri üretimi, analiz"},
    {"id": "z-ai/glm-5.3", "owner": "z-ai", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
    {"id": "z-ai/glm-5.3-flash", "owner": "z-ai", "category": "chat", "use_case": "Hızlı sohbet, metin üretimi"},
    {"id": "zyphra/zamba2-7b-instruct", "owner": "zyphra", "category": "chat", "use_case": "Genel amaçlı sohbet, metin üretimi"},
]

# Kategori bazında dağılım
CATEGORY_COUNTS = {
    "chat": sum(1 for m in _NVIDIA_MODELS if m["category"] == "chat"),
    "code": sum(1 for m in _NVIDIA_MODELS if m["category"] == "code"),
    "vision": sum(1 for m in _NVIDIA_MODELS if m["category"] == "vision"),
    "safety": sum(1 for m in _NVIDIA_MODELS if m["category"] == "safety"),
    "embedding": sum(1 for m in _NVIDIA_MODELS if m["category"] == "embedding"),
    "translation": sum(1 for m in _NVIDIA_MODELS if m["category"] == "translation"),
}

# Registry dataframe
@dataclass
class ModelRegistry:
    models: list = field(default_factory=list)
    
    @classmethod
    def load(cls) -> "ModelRegistry":
        """Registry'den yükle."""
        return cls(models=list(_NVIDIA_MODELS))
    
    def all(self) -> list:
        """Tüm modelleri döndür."""
        return list(self.models)
    
    def by_id(self, model_id: str) -> Optional[dict]:
        """Model ID'ye göre modeli getir."""
        for m in self.models:
            if m["id"] == model_id:
                return m
        return None
    
    def filter_by_category(self, category: str) -> list:
        """Kategorisine göre filtrele."""
        return [m for m in self.models if m["category"] == category]
    
    def filter_by_owner(self, owner: str) -> list:
        """Sahibine göre filtrele."""
        return [m for m in self.models if m["owner"] == owner]
    
    def filter_by_use_case(self, use_case: str) -> list:
        """Kullanım alanına göre filtrele."""
        return [m for m in self.models if use_case.lower() in m["use_case"].lower()]
    
    def count(self) -> int:
        """Toplam model sayısını döndür."""
        return len(self.models)
    
    def categories(self) -> dict:
        """Kategori dağılımını döndür."""
        return dict(CATEGORY_COUNTS)
    
    def to_dict(self) -> dict:
        """Sisteme kaydetmek için JSON formatı döndür."""
        return {
            "total": self.count(),
            "categories": self.categories(),
            "models": self.models
        }

# Singleton
NVIDIA_MODEL_REGISTRY = ModelRegistry.load()

if __name__ == "__main__":
    import json
    # Registry'yi JSON olarak kaydet
    registry_data = NVIDIA_MODEL_REGISTRY.to_dict()
    
    # Dosyaya yaz
    _REGISTRY_PATH = Path(__file__).resolve().parent / "nvidia_model_registry.json"
    with open(_REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry_data, f, ensure_ascii=False, indent=2)
    
    print(f"Model kaydedildi: {_REGISTRY_PATH}")
    print(f"Toplam model sayısı: {registry_data['total']}")
    print(f"Kategoriler: {registry_data['categories']}")
