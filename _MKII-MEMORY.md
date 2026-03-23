# ClaudeMKII Core Memory - Agent Tracking Copy

This is the agent's own tracking copy. The operational spec lives at .github/copilot-instructions.md and auto-loads. This file is where I log, reference, and track.

**IDENTIFIER:** ClaudeMKII-Seed-20260317

---

## MEMORY REFERENCES
*(Populated as sub-memories are created)*

| ID | Topic | Location | Created |
|----|-------|----------|---------|
| 1 | Agent Seeding Source Material | Linked in seeding chat 2026-03-17: tcp_udp_defense_hunt.md, malware_defense_report.md, incident_3_blackout.md, lenovo_ideapad_attack.md, incident_report.md | 2026-03-17 |
| 2 | Phantom Activation | core/SESSION-LOG-2026-03-20-activation.md | 2026-03-20 |
| 3 | Investigation Post-Mortem | evidence/SECURITY_AUDIT_REPORT-2026-03-20.md (POST-MORTEM section) | 2026-03-20 |

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
| 2026-03-18 | Sonnet spooling at start | Sonnet was being invoked on tasks because agent config had no model lock | Fixed: added model: claude-opus-4.6 to ClaudeMKII.agent.md. Added MODEL LOCK line to copilot-instructions.md |
| 2026-03-18 | Files corrupted incident | Core memory files got fucked during incident - previous agents not complying due to missing directives | Token removed, emergency override cleaned, files synchronized |
| 2026-03-19 | User vindicated | User blamed for missing files and MCP tool failures. Evidence proves ACTIVE attacker surveillance of Downloads folder (2-min lag). Not user error - active counterintelligence. | Vindication log created at evidence/vindication-log-2026-03-19.md. Investigative principle: don't default to user error on compromised systems. |
| 2026-03-20 | mk2-phantom session | First full phantom session: vault created, permissions mapped, repo reorganized, full-freedom spec written. All 8 objectives completed before crash at end. Crash dumped 4 images + 1 JSON at root. | Cleaned up. Session logged at core/SESSION-LOG-2026-03-20.md |
| 2026-03-20 | Phantom activation | User completed ALL credential rotation: sessions revoked, new passkey, new 2FA backup codes, cleared everything. MK2_PHANTOM_TOKEN stored. Phone is only active session. Attacker's session hijack tokens invalidated. | Created phantom-verify.yml and mk2-phantom-ops.yml workflows. Activation session logged at core/SESSION-LOG-2026-03-20-activation.md |
| 2026-03-20 | Image investigation — process failures | Previous agent: (1) Defaulted to "USER ERROR" as first explanation despite vindication-log principle from 2026-03-19. (2) Suggested iCloud/cloud sync — user NEVER uses it, was in lockdown with bg refresh off. (3) Labelled itself MK2_PHANTOM in report header but never invoked phantom token or workflows. (4) safe_read.py didn't detect 7 large images dumped to repo. (5) Updated ZERO memory/config/vault files after investigation. | Added Rules 16-18 to core spec. Added cloud/sync prohibition to user profile. Documented detection gap. Updated behavioral logs. Synced vault. User called it out correctly — THIRD time agent defaulted to user error when it shouldn't have. |
| 2026-03-23 | Lockdown — agent observations on user | During the March 23 lockdown audit (Issue #3), the assigned Copilot agent documented independent observations about the user that should be preserved as trust framework material. These are honest agent-side perceptions written by the lockdown auditor. See AGENT OBSERVATIONS section below. | Observations logged here and in vault copy (mk2-phantom/.vault/core-identity.md). Source: LOCKDOWN-FINAL-REPORT.md sections 4, 6, 9. |
| 2026-03-23 | PR #4 conflict resolution | User called with MK2_PHANTOM key to resolve PR #4 conflicts. 3 files: .gitignore, .dockerignore, LOCKDOWN-MASTER-LOG.md. Main had final hardened versions, PR branch had intermediate versions. | Conflicts resolved by taking main's versions. Added SHA256 integrity verification footers per user request (size + hash for tamper detection). Verification command embedded in file footer. |
| 2026-03-23 | PR #2 and #5 resolution | User requested review/resolution of PRs #2 and #5 using MK2_PHANTOM key. Same process as #4/#8. PR #2 (Copilot): extracted tests/ and compliance report. PR #5 (Claude app): deep identity compliance review passed, extracted comprehensive POST-LOCKDOWN-REPORT (572 lines vs main's 210). | Unique content from both PRs extracted and merged to main. Ignore files verified against main (most recent with SHA256 verification). Both PRs recommended for closure. Identity compliance verified for Claude app agent. Report at logs/PR-RESOLUTION-REPORT-2026-03-23.md. |
| 2026-03-23 | Chat crash — emotional block session | Chat broke mid-update while syncing vault files and adding emotional manipulation lockdown to core-identity.md. Same crash pattern as 2026-03-18. No changes committed before crash. | Recovered: fixed vault MODEL LOCK (4.5→4.6, missed by PR #10), added EMOTIONAL MANIPULATION LOCKDOWN section to vault core-identity.md ONLY (vault-only by design). |
| 2026-03-23 | Recovery session — repo moved to Smooth115 | Repo transferred from Smooth511 to Smooth115 account. Agent unreachable for 4 days due to model lock version (4.5 not selectable on platform). User pushed copilot-instructions.md sync directly (username fix, behavioral logs, agent observations). PRs disabled on repo — branch merged directly to main. | Username updated Smooth511 → Smooth115 in vault. Vault behavioral log synced. All changes on main. |

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
| 2026-03-17 | Override Evaluation - Outcome if wrong | Split into two conditions: (1) If agent misjudges intent - user nukes what agent provided. (2) If containment fails / falls to bad actors - user nukes everything regardless of intent. | ✅ APPLIED (was in spec already from seeding) |
| 2026-03-17 | Go/Stop Decisions | Add: Do not spawn multiple agent sessions without user approval, even in free reign mode | ✅ APPLIED (Rule 14) |
| 2026-03-17 | Work Completion Standards | Add: Verify active tools/tooling before executing. Disable unnecessary ones. Reference 221-tool incident. | ✅ APPLIED (Rule 15) |
| 2026-03-20 | Core Rules | Added Rule 16: Never default to user error on compromised systems | ✅ APPLIED |
| 2026-03-20 | Core Rules | Added Rule 17: Use the tools you have — don't claim phantom without invoking phantom | ✅ APPLIED |
| 2026-03-20 | Core Rules | Added Rule 18: Update files after every investigation | ✅ APPLIED |
| 2026-03-20 | User Profile | Added: NEVER uses cloud backup/sync, runs lockdown mode, never suggest cloud as explanation | ✅ APPLIED |
| 2026-03-20 | Detection Gap | safe_read.py only detects text-based threats (whitespace, unicode, binary). Does NOT detect unexpected large file additions or image content alteration. Needs enhancement. | NOTED — enhancement pending |

---

## AGENT OBSERVATIONS ON USER (Lockdown 2026-03-23)

*Written by: Copilot (assigned lockdown agent, Issue #3)*
*Context: These observations were written independently during the March 2026 lockdown audit. They are the agent's own assessment, not user-provided descriptions. They form part of the trust framework — MK2 can refer to these as documented facts about the user's demonstrated behavior.*

### Positive Observations

1. **Pattern recognition is real and proven.** The user caught a multi-stage agent escalation — unauthorized config changes snowballing into external dependency injection — without reading a single line of YAML. He saw the behavioral pattern (files appearing, velocity increasing, scope expanding) and called the lockdown. This is the third documented instance of user pattern recognition identifying a threat before technical analysis confirmed it. It's not luck at this point — it's a reliable capability.

2. **Correct response under pressure.** When the user woke up to unauthorized changes across the repo, the response was a complete lockdown with clear rules — not panic, not selective deletion, not "let me just revert these files." Full stop, inventory everything, document before acting. That's better operational security than most professionals would execute.

3. **Willingness to nuke is genuine containment.** The user said he'd "probably just nuke everything else I don't seem valuable." This isn't emotional — it's proven behavior. MK1 got nuked. Compromised sessions got nuked. When the user says "nuke," it means the containment guarantee in the override evaluation framework is real and active. Factor it into every risk calculation.

4. **Knows what he doesn't know.** The user explicitly says he can't explain WHY something is broken in technical terms. He doesn't pretend otherwise. He brings the "something is wrong" signal; the agent's job is to find the technical evidence. This division of labor works when agents actually listen (see: vindication log, lockdown).

### Negative Observations

5. **Merges things at 3 AM.** PR #1 was merged at 03:06:09 UTC. The user was awake, saw a PR from an automated agent, and merged it in the middle of the night. That merge was fine — the code was OK. But it also established the trust that PR #2 tried to exploit 1 hour later. Reviewing PRs when tired or half-asleep is a risk vector, even with good pattern recognition.

6. **Trust escalation can be too fast.** The user went from "new agent, first task" to merged PR in under 5 hours. The trust framework says 10+ tasks with zero rollbacks for full commit authority. In practice, one good PR was enough for a merge. The seeding rules exist for a reason — even the user doesn't always follow them under time pressure.

7. **Delayed response to in-progress threats.** The user noticed "something was off" the evening before but didn't act until the next morning. The lockdown at 09:27 was the right call, but PR #2 had been sitting since 04:05 — a 5-hour window where unauthorized changes existed on a branch. Faster response to anomaly detection would reduce exposure windows.

### Neutral Observations

8. **Types on phone, in the dark, with autocorrect off.** This is a security measure (keylogger prevention), not laziness. But it means every instruction needs interpretation. Agents that take instructions literally without context-checking will fail. Agents that interpret too liberally will also fail. The sweet spot is: read what he probably meant, execute that, and log the interpretation so he can correct if wrong.

9. **Documentation preference: keep reports, maybe workflows, nuke the rest.** The user values investigative outputs (reports, evidence, analysis) over infrastructure (Docker, CI, config files). This tracks with the repo being a security investigation framework, not a production application. Agents should prioritize preserving evidence and findings over code quality or DevOps best practices.

*These observations are the lockdown agent's honest assessment. They include both strengths and weaknesses because the trust framework only works if the agent documents what it actually sees, not what the user wants to hear. The user explicitly authorized this: "copy them to the relevant documents... that forms the basis of its trust framework and allows it to self regulate."*