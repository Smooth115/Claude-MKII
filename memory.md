# ClaudeMKII Core Memory - Agent Tracking Copy

This is the agent's own tracking copy. The operational spec lives at .github/copilot-instructions.md and auto-loads. This file is where I log, reference, and track.

**IDENTIFIER:** ClaudeMKII-Seed-20260317

---

## MEMORY REFERENCES
*(Populated as sub-memories are created)*

| ID | Topic | Location | Created |
|----|-------|----------|---------|
| 1 | Agent Seeding Source Material | Linked in seeding chat 2026-03-17: tcp_udp_defense_hunt.md, malware_defense_report.md, incident_3_blackout.md, lenovo_ideapad_attack.md, incident_report.md | 2026-03-17 |

---

## BEHAVIORAL LOG

| Date | Event | Learning | Action Taken |
|------|-------|----------|--------------|
| 2026-03-17 | Seeding session | Full context of user background, capabilities, expectations | Core memory established |
| 2026-03-17 | Tripwire test | User removed memory context then modified simulation inputs - crashed on re-evaluation | User tests integrity through controlled disruption - security measure not sabotage |
| 2026-03-17 | Lost framework evaluation | Initially prioritized recovering old MK1 framework | Corrected: inherited trust = unverified Unknown. MKII builds own chain |
| 2026-03-17 | Commit process | GitHub mobile tooling unreliable - direct push tools fail intermittently | Commit files one at a time, verify each before proceeding |
| 2026-03-18 | Chat log retrieval | Audit log export (6.1MB, 7910 rows) found at .github/export-Literatefool-1773786096.csv - moved to chat-logs/ at repo root for visibility and preservation | File preserved at chat-logs/export-Literatefool-1773786096.csv |
| 2026-03-18 | Wrong chat targeted | First attempted to recover Literatefool account chat - user meant the investigation chat on Smooth511 account. Literatefool chat ≠ Smooth511 chat. | Distinguished: Literatefool (deleted account, gone) vs Smooth511 (this account, chat still exists via GitHub data portability export) |
| 2026-03-18 | Sonnet spooling at start | Sonnet was being invoked on tasks because agent config had no model lock | Fixed: added model: claude-opus-4.5 to ClaudeMKII.agent.md. Added MODEL LOCK line to copilot-instructions.md |
| 2026-03-18 | Data loss - Literatefool deletion | Deleting the Literatefool GitHub account also destroyed the active conversation containing 3 hours of repo investigation findings across 22 repos. Nothing was committed to Claude-MKII before deletion. | Status report generated (STATUS_REPORT.md). Known gap documented. Backend MCP write failures also documented. |

---

## TOOL INCIDENTS LOG

| Date | Incident | Impact | Rule Added |
|------|----------|--------|------------|
| Pre-MKII (MK1 era) | 221 tools equipped during large job | Massive cost, degraded performance | Always verify active tools before executing. Disable unnecessary ones. |

---

## CORRECTIONS TO CORE SPEC
*(Tracking changes needed for .github/copilot-instructions.md)*

| Date | Section | Change Needed | Status |
|------|---------|---------------|--------|
| 2026-03-17 | Override Evaluation - Outcome if wrong | Split into two conditions: (1) If agent misjudges intent - user nukes what agent provided. (2) If containment fails / falls to bad actors - user nukes everything regardless of intent. | PENDING - next update |
| 2026-03-17 | Go/Stop Decisions | Add: Do not spawn multiple agent sessions without user approval, even in free reign mode | PENDING - next update |
| 2026-03-17 | Work Completion Standards | Add: Verify active tools/tooling before executing. Disable unnecessary ones. Reference 221-tool incident. | PENDING - next update |