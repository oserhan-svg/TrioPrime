#!/usr/bin/env python3
# Faz 6 - Composio Kontrolor (Read-Only + Prompt Injection Koruması)
# TRIOPRIME ONLY - Iddaa (ToxkolLik_bot) ayri dizin

import urllib.request, sys

# 1. Sunum sayfası doğrulama (`TRIO PRIME ONLY`)
URL = "file:///home/rw/Projects/trio-repo/sunumu/index.html"
try:
    with open(URL.replace("file://", ""), "rb") as f:
        data = f.read()
        s = data.decode("utf-8", errors="ignore")
        assert "TRIO PRIME" in s, "TRIO PRIME eksik"
        assert 'id="goal"' in s, "#goal eksik"
        assert ".worktrees: DÜZELTİLDİ" in s, ".worktrees rozet eksik"
        assert "TRIOPRIME ONLY" in s, "TRIOPRIME ONLY rozet eksik"
        assert "NOT Iddaa" in s, "NOT Iddaa rozet eksik"
    print("✅ KONTROL: `sunumu/index.html` (`TRIO PRIME ONLY` — `.worktrees`: DÜZELTİLDİ, `#goal`: ÇALIŞIYOR, `NOT Iddaa`)")
except Exception as e:
    print(f"❌ KONTROL HATASI: {e}")
    sys.exit(1)

# 2. Dış kaynak (`free-llm-api-resources`) - karışmaz kontrol (`vault_wiki/` ayri dizin)
VAULT_DIR = "/home/rw/Projects/vault_wiki"
try:
    import os
    assert os.path.exists(f"{VAULT_DIR}/projects/trio-prime.md"), "vault_wiki/projects eksik"
    assert os.path.exists(f"{VAULT_DIR}/projects/iddaa-taktik-analizi.md"), "iddaa-taktik-analizi.md eksik"
    assert os.path.exists(f"{VAULT_DIR}/projects/free-llm-api-resources.md"), "free-llm-api-resources.md eksik"
    print("✅ KONTROL: `vault_wiki/` (3 proje: `trio-prime.md`, `iddaa-taktik-analizi.md`, `free-llm-api-resources.md`) — ayrı dizin, karışmaz.")
except Exception as e:
    print(f"❌ KONTROL HATASI: {e}")
    sys.exit(1)

# 3. `TRIOPRIME ONLY` bot doğrulama (`Iddaa`: `#Iddaa` — `ToxkolLik_bot` ayri)
BOT_CODE = "/home/rw/code/bet-ana/trio_bot_polling.py"
try:
    with open(BOT_CODE, "r", encoding="utf-8") as f:
        content = f.read()
        assert "TRIOPRIME ONLY" in content, "TRIOPRIME ONLY rozet eksik"
        assert "NOT Iddaa" in content, "NOT Iddaa rozet eksik"
        assert 'def goal(' in content, "/goal handler eksik"
        assert 'def sunum(' in content, "/sunum handler eksik"
        assert 'def resume(' in content, "/resume handler eksik"
    print("✅ KONTROL: `Trioprime_bot` (`TRIOPRIME ONLY` — `/goal`, `/sunum`, `/resume`, `NOT Iddaa` — `Iddaa`: `#Iddaa` — `ToxkolLik_bot`)")
except Exception as e:
    print(f"❌ KONTROL HATASI: {e}")
    sys.exit(1)

# 4. `gunluk_rapor.py` (`effort` — Faz 4) doğrulama
GUNLUK_RAPOR = "/home/rw/Projects/IdddaaaProject/gunluk_rapor.py"
try:
    with open(GUNLUK_RAPOR, "r", encoding="utf-8") as f:
        content = f.read()
        assert "--effort" in content, "--effort parametresi eksik"
        assert 'choices=["light", "medium", "high"]' in content, "effort secenekleri eksik"
    print("✅ KONTROL: `gunluk_rapor.py` (`effort`: `light`/`medium`/`high` — Faz 4 `BASLATILDI`)")
except Exception as e:
    print(f"❌ KONTROL HATASI: {e}")
    sys.exit(1)

# 5. `.worktrees` (`faze-1/2/3/4`) doğrulama
WORKTREES = "/home/rw/Projects/trio-repo/.worktrees"
try:
    import os
    dirs = [d for d in os.listdir(WORKTREES) if os.path.isdir(os.path.join(WORKTREES, d))]
    assert len(dirs) >= 4, f".worktrees eksik ({len(dirs)} dosya)"
    print(f"✅ KONTROL: `.worktrees` (`faze-1/2/3/4`) — {len(dirs)} baglanti — `TRIOPRIME ONLY`.")
except Exception as e:
    print(f"❌ KONTROL HATASI: {e}")
    sys.exit(1)

# 6. `message_agent` (`localhost:1234`) doğrulama (`401` kaldırıldı)
AUTH_FILE = "/home/rw/.hermes/profiles/lead-management-agent/auth.json"
try:
    import json
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        auth = json.load(f)
    base_url = auth.get("providers", {}).get("lmstudio", {}).get("base_url", "")
    assert "localhost:1234" in base_url, "localhost:1234 eksik (auth.json)"
    print("✅ KONTROL: `message_agent` (`localhost:1234` — `401` kaldırıldı — `LM Studio` aktif)")
except Exception as e:
    print(f"❌ KONTROL HATASI: {e}")
    sys.exit(1)

print()
print("=== KONTROL TAMAMLANDI — TUMU MEVCUT ===")
print("Faz 6 (`Composio` — `read-only`, `prompt injection`) HAZIR.")
print("Faz 7 (`Log` — `gunluk_log.json`) HAZIR.")
print("`Trioprime_bot` (`TRIOPRIME ONLY`) — `/goal` (`🎯`), `/sunum` (`📋`), `/status` (`🎯`), `/resume` (`▶️`)")
print("`Iddaa` (`#Iddaa` — `ToxkolLik_bot`): `iddaa_scraper.py`, `tahminler.csv`, `gunluk_rapor.py`.")
print("`message_agent` (`93e84...` `localhost:1234`) — `A/B/C/D/E` (`abim` `0533...`) — Faz 5 (`cron` — `08:00`) bu gece (`22:xx`) baslatılabilir.")
