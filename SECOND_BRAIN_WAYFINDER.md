# Second Brain / Vault — Wayfinder (Kalıcı İşaretçi)

Bu dosya, Kriss (AI Operator) için her session'da Second Brain / Vault konumunu hatırlatmak amacıyla oluşturulmuştur.

## Ana Konum
`/home/rw/HermesSecondBrain/SecondBrain/`

## PARA Yapısı
| Katman | Yol | Amacı |
|--------|-----|-------|
| 0-raw | `0-raw/` | Ham girişler,Router/Dispatch tarafından yazılır |
| 1-wiki | `0-raw/*/1-wiki/` | Derlenen kalıcı bilgi, Librarian tarafından yazılır |
| 2-digest | `0-raw/*/2-digest/` | Sıkıştırılmış özetler, cron / haftalık raporlar |

## TrioPrime Özel Yolları
- TrioPrime wiki: `0-raw/Ozancan Serhan/1-wiki/TrioPrime Emlak Gayrimenkul/`
- TrioPrime teknik: `0-raw/Ozancan Serhan/1-wiki/TrioPrime Emlak Gayrimenkul/teknoloji/`
- Neural linking playbook: `teknoloji/neural-linking-memory.md`
- Ajanlar: `0-raw/Ozancan Serhan/agents/` (librarian.md, orchestrator.md, developer.md, review_agent.md, suggestion_agent.md, scout_agent.md, loop_agent.md)
- Scout Feed: `0-raw/Ozancan Serhan/scout_feed/` (Scout Agent'ın internetten topladığı ham bilgiler)

## Diğer Notlar
- `soul.md` (`/home/rw/Projects/soul.md`) — Kriss kimlik dosyası, bu wayfinder yolunu içerir.
- `vault_wiki/` (`/home/rw/Projects/vault_wiki/`) — eski/boş wiki klasörü, **aktif second brain değildir**.
- Her yeni session'da bu dosya okunur ve vault konumu doğrudan bu yoldan kullanılır; sıfırdan arama yapılmaz.


## Hermes Kaynak ve Dış Referanslar
Kaynak: /home/rw/Downloads/awesome-agent-cortex-main/hermes/references.md

- Upstream repo: https://github.com/NousResearch/hermes-agent
- Upstream README: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/README.md
- Upstream CONTRIBUTING: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/CONTRIBUTING.md
- Upstream AGENTS.md: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/AGENTS.md
- CLI config example: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/cli-config.yaml.example
- .env example: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/.env.example
- Install script: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/setup-hermes.sh
- Official docs: https://hermes-agent.nousresearch.com/docs/
- Quickstart docs: https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
- Configuration docs: https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- Memory docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- Skills docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- Cron docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
- Architecture docs: https://hermes-agent.nousresearch.com/docs/developer-guide/architecture
- Contributing docs: https://hermes-agent.nousresearch.com/docs/developer-guide/contributing
- Self-evolution: https://github.com/NousResearch/hermes-agent-self-evolution
- Paperclip adapter: https://github.com/NousResearch/hermes-paperclip-adapter
- Hermes-fly: https://github.com/alexfazio/hermes-fly
- AgentSkills: https://agentskills.io
