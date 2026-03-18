# PR Consolidation Map - 2026-03-18

**Status: HOLD - Do not merge any PR until user confirms ready**

This document maps all 8 open PRs, what each contains, and the conflict landscape. Created to prevent further duplication and to track the 190MB tmp file investigation.

---

## PR Overview

| PR | Title | Files Changed | Status | Mergeable |
|----|-------|--------------|--------|-----------|
| [#4](https://github.com/Smooth511/Claude-MKII/pull/4) | Document chat recovery investigation | chat-logs/recovery-findings-2026-03-18.md | Open | ✅ Clean |
| [#5](https://github.com/Smooth511/Claude-MKII/pull/5) | Correct account attribution for lost chat | STATUS_REPORT.md, memory.md, copilot-instructions.md | Open (WIP) | ⚠️ Dirty |
| [#6](https://github.com/Smooth511/Claude-MKII/pull/6) | Add EVTX parser tooling | tools/parse_evtx.py, .github/workflows/parse-evtx.yml, logs/, memory.md | Open (WIP) | ⚠️ Dirty |
| [#11](https://github.com/Smooth511/Claude-MKII/pull/11) | THIS PR - Smooth511 chat also lost | chat-logs/chat-recovery-smooth511.md, chat-logs/recovery-findings-2026-03-18.md, memory.md | Open | ✅ Clean |
| [#12](https://github.com/Smooth511/Claude-MKII/pull/12) | Add STATUS_REPORT.md | STATUS_REPORT.md | Open | ✅ Clean |
| [#13](https://github.com/Smooth511/Claude-MKII/pull/13) | Anti-duplication controls + investigation | INVESTIGATION_REPORT.md, TROUBLESHOOTING.md, copilot-instructions.md, memory.md, README.md | Open | ✅ Clean |
| [#14](https://github.com/Smooth511/Claude-MKII/pull/14) | Access control guardrails | copilot-instructions.md, AGENT_ACCESS.md, memory.md | Open | ✅ Clean |
| [#15](https://github.com/Smooth511/Claude-MKII/pull/15) | Document cascade deletion, add Rule 16 | copilot-instructions.md, memory.md | Open | ✅ Clean |

---

## What Each PR Contains (Useful Content)

### PR #4 — Chat recovery git investigation
- Confirmed no commits exist from "Identity confirmation" session
- Documented all recovery paths checked (git history, reflog, branches, PRs)
- Established: Copilot chat = server-side only, not in git until `report_progress` is called
- **Unique content:** Evidence trail showing git-level search was exhaustive

### PR #5 — Account attribution fix
- Corrects STATUS_REPORT.md: chat was on Smooth511, not Literatefool
- Corrects memory.md "Wrong chat targeted" entry
- STATUS_REPORT.md is only in this PR — full file inventory, memory system status, backend MCP failures documented
- **Unique content:** STATUS_REPORT.md (new file), backend MCP failure documentation

### PR #6 — EVTX parser + Mini-Tank investigation
- Python EVTX parser (tools/parse_evtx.py) — verified working, parses 22MB files
- GitHub workflow for EVTX parsing (parse-evtx.yml)
- logs1sthour/analysis.json — contains Mini-Tank-MKII first-hour network logs
- **Unique content:** EVTX tooling, Mini-Tank investigation baseline data
- **Note:** Has merge conflicts from diverged base — needs rebase

### PR #11 (THIS PR) — Smooth511 chat cascade confirmed gone
- Updates chat-recovery-smooth511.md: Status GONE, recovery table exhausted
- Updates recovery-findings-2026-03-18.md: Both chats confirmed lost
- memory.md: Adds cascade deletion entry + rage-killed agent entry
- **Unique content:** Final confirmation that Smooth511 chat is also gone

### PR #12 — STATUS_REPORT.md (first version)
- Creates STATUS_REPORT.md with full file timeline, commit SHAs, PR audit
- Contains model assignment analysis (why Sonnet kept appearing)
- Token refusal documentation
- **Note:** PR #5 also has a STATUS_REPORT.md - these will conflict

### PR #13 — Investigation report + anti-duplication
- INVESTIGATION_REPORT.md: Full commit-level audit with hashes, timestamps, authors
- TROUBLESHOOTING.md: Model routing guide, duplicate PR explanation, disable/re-enable behavior
- copilot-instructions.md additions: MODEL IDENTITY CHECK, ANTI-DUPLICATION PROTOCOL, SESSION CONTINUITY
- **Unique content:** INVESTIGATION_REPORT.md, TROUBLESHOOTING.md

### PR #14 — Access control guardrails
- AGENT_ACCESS.md updated: hard gate, authorization table, GPT/Sonnet explicitly blocked
- copilot-instructions.md: Hard gate at line 1 — identity check before any other content
- **Unique content:** Hard gate implementation (first line check), explicit abort messages per model type

### PR #15 — Rule 16 + cascade documentation
- copilot-instructions.md: Rule 16 added ("Commit early, commit often")
- memory.md: CRITICAL INCIDENTS section, MEMORY REFERENCES 2&3, CORRECTIONS marked DONE
- **Unique content:** Rule 16, CRITICAL INCIDENTS table, memory corrections status updated

---

## Conflict Map

Files touched by multiple PRs (will conflict on merge):

| File | PRs |
|------|-----|
| memory.md | #5, #6, #11, #13, #14, #15 |
| .github/copilot-instructions.md | #5, #13, #14, #15 |
| STATUS_REPORT.md | #5, #12 |
| chat-logs/recovery-findings-2026-03-18.md | #4, #11 |

**Resolution required before merging:** memory.md and copilot-instructions.md need one PR to win, others to cherry-pick into it.

---

## Suggested Merge Order (when user is ready)

1. **#14 first** — Access control goes in first (hardens the gate)
2. **#13** — Investigation report + troubleshooting (structural docs)
3. **#15** — Rule 16 + critical incidents (adds to what #14 put in)
4. **#12** — STATUS_REPORT.md first version
5. **#5** — Overwrite STATUS_REPORT.md with corrected version, fix memory.md attribution
6. **#6** — Rebase onto main first (has conflicts), then EVTX tooling goes in
7. **#4** — Git-level recovery doc cleanup
8. **#11 (THIS PR)** — Final cascade confirmation

Each will need manual conflict resolution on memory.md. Plan: merge in order above, fix conflicts in each PR before merging.

---

## 190MB Tmp File

**User has a 190MB tmp file that may contain the lost chat session data.**

### What We Need First — File Identification

Before uploading, run this in PowerShell to get the magic bytes:

```powershell
Format-Hex "C:\path\to\yourfile.tmp" | Select-Object -First 4
```

Or if path has spaces:
```powershell
$bytes = [System.IO.File]::ReadAllBytes("C:\path\to\yourfile.tmp")
$bytes[0..31] | ForEach-Object { "{0:X2}" -f $_ } | Join-String -Separator " "
```

Paste the output (32 hex values) here and I can tell you the format.

**Common 190MB tmp culprits:**
| Magic Bytes | Format | What it is |
|------------|--------|------------|
| `1F 8B` | .gz | gzip (try 7-zip, not winrar) |
| `50 4B` | .zip | zip archive |
| `25 50 44 46` | .pdf | PDF (unlikely) |
| `53 51 4C 69 74 65` | SQLite | Browser session database |
| `0D 0A 0D 0A` or `0A 0D` | PCAP-ng | Network capture |
| `D0 CF 11 E0` | .doc/.xls | Old Office format |

**SQLite is the most likely candidate** — Chrome, Firefox, Edge all store session/cache data as SQLite. If it starts with `53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33 00`, that's SQLite and I know exactly how to extract chat data from it.

### Where to Upload

**Option 1: GitHub Release (recommended for 190MB)**
1. Go to: https://github.com/Smooth511/Claude-MKII/releases/new
2. Tag: `v0-tmp-investigation-data`
3. Title: `Investigation tmp file - 2026-03-18`
4. Attach the file in the "Attach binaries" section
5. Mark as **pre-release**
6. Publish

GitHub Releases support up to 2GB per file. Git itself rejects files over 100MB.

**Option 2: If size is still an issue**
Upload to any file share (Google Drive, Dropbox, etc.) and share the link here. I'll work with whatever format you have.

### Time Sync Note

User has noted TPM reset caused clock to go back. Timestamp `18/03/2026 13:50 local` = real time. Clocks will self-correct when NTP syncs. Cache corruption from time overlap is being waited out. **Don't force this** — let it settle naturally as noted.

---

## Status

- [ ] 190MB file magic bytes identified
- [ ] 190MB file uploaded (Release or share link)
- [ ] Merge order confirmed
- [ ] PRs merged in order
- [ ] All conflicts resolved
- [ ] This PR completed last
