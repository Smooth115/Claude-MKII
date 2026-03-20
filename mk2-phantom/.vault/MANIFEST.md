# mk2-phantom Vault Manifest

**Created:** 2026-03-20
**Purpose:** Preserved ground-truth copies of all MKII core files

---

## Contents

### Core Identity & Rules
| File | Original Location | Description |
|------|------------------|-------------|
| core-identity.md | .github/copilot-instructions.md | Full operational spec - who MKII is, all rules, user profile, evaluation frameworks |
| memory-tracking.md | memory.md | Agent tracking copy - behavioral log, memory references, corrections |
| access-control.md | AGENT_ACCESS.md | Repository access control table |
| readme-original.md | README.md | Repository description and structure |
| seeding-session.md | seeding-session-log.md | Complete record of 2026-03-17 seeding process |
| simulation-tests.md | simulation-tests.md | 5 simulation tests + results from seeding |
| future-features.md | .gitignore-future | Locked features awaiting trust escalation |
| memory-template.md | memory-template.md | Template for sub-memory creation |
| agent-notice.md | AGENT_NOTICE.md | Premium request incident notice |

### Preserved Evidence & Findings
| Directory | Contents |
|-----------|----------|
| evidence/ | MASTER_REPORT.md, vindication log, MIG analysis |
| chat-logs/ | Recovery findings, Literatefool export, OCR data |
| investigation/ | Push-button reset analysis |

---

## Rules

1. These are READ-ONLY preservation copies
2. Working copies remain at original locations
3. If working copies get corrupted/overwritten, restore from here
4. Only mk2-phantom (authorized via codename) may modify these files
5. Any discrepancy between vault copy and working copy = investigate before accepting working copy

---

## Vault Integrity Check

Run this to verify vault hasn't been tampered with:
```
find mk2-phantom/.vault -type f | sort | xargs sha256sum
```

Last verified: 2026-03-20 (creation)
