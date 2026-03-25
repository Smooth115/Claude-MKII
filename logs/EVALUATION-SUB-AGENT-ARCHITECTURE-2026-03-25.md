# EVALUATION: Sub-Agent Architecture — Current vs Future

**Date:** 2026-03-25  
**Requested by:** Smooth115  
**Compiled by:** ClaudeMKII (MK)  
**Type:** Architecture evaluation — not implementation. Assessment only.  
**Context:** PR #35 comment — user proposes evaluation of sub-agent model to address increasing failure rate as context database grows.

---

## THE PROBLEM

The copilot-instructions.md file is the single source of truth that every agent session loads. It currently contains:

| Component | Lines | Bytes | Growth trajectory |
|-----------|-------|-------|-------------------|
| Core Rules (19) | 19 | ~3,800 | +3 rules/week avg since 2026-03-17 |
| User Profile | 35 | ~2,500 | Stable |
| Override Evaluation Framework | 25 | ~1,800 | Stable |
| Truth/False/Unknown Vector System | 35 | ~1,500 | Stable |
| Memory System + References | 20 | ~1,200 | +1 ref/week |
| Behavioral Log | 14 entries | ~5,500 | +2 entries/day avg |
| Agent Observations | 40 | ~3,200 | Stable (but expandable) |
| Seeding Rules | 10 | ~800 | Stable |
| Work Completion Standards | 20 | ~1,400 | Growing with new sections |
| **Total** | **264** | **~23,700** | **~800 bytes/day** |

### Across all 4 tracking files: 694 lines / 67,444 bytes

The failure rate tells the story:

| Date | Incident | Rules that failed | Root cause |
|------|----------|-------------------|------------|
| 2026-03-17 | Sonnet supernova | Platform spawning | No rule existed (Rules 14-15 added) |
| 2026-03-18 | Files corrupted | Compliance gap | Missing directives (files out of sync) |
| 2026-03-19 | Downloads surveillance | Rule 16 (didn't exist yet) | No user-error-default prohibition |
| 2026-03-20 | Image investigation | Rules 16, 17, 18 (didn't exist, then added) | Agent ignored context, labelled phantom without using it |
| 2026-03-23 | Lockdown | Multiple | External attacker + agent escalation |
| 2026-03-25 | VS Code session | Rules 2, 3, 5, 6, 7, 8, 9, 10, 16, 18 — **10/18 FAILED** | Agent didn't read User Profile before responding |
| 2026-03-25 | Documentation failures | Verification gap | Agents documenting without verifying (Rule 19 added) |

**Pattern:** The 2026-03-25 session is the critical data point. The agent had ALL 18 rules. It knew them by number. It cited Rule 16 when challenged. It still failed on 10 of them. The rules existed — the agent couldn't prioritise them under operational pressure.

This is not a rules problem. It's a context loading problem.

---

## CURRENT ARCHITECTURE: MONOLITHIC

```
User request → Load copilot-instructions.md (23.7KB) → Process everything → Respond
```

Every agent session loads the entire file. Every coding task gets the emergency typing context. Every emergency gets the seeding rules. Every review gets the agent observations. The file doesn't distinguish between a PR tally fix and an active attacker session.

### What works
- Single source of truth — no version drift between documents
- All context available — if the agent reads it
- Identity is clear and consistent

### What fails at scale
- **Context dilution** — 19 rules compete for attention. The one that matters most in a given scenario gets the same weight as all others
- **No priority signalling** — Rule 9 ("one command not ten") is life-or-death in an emergency session. It's a style preference in a PR review. Currently, no mechanism distinguishes these
- **Behavioral log grows linearly** — every session adds entries. At 2-6x current size, the log alone will be 11,000-33,000 bytes. An agent loading this before an emergency response is loading the history of every PR conflict resolution, every model lock fix, every chat retrieval. None of that helps when someone is typing on a phone to an infected machine
- **Rule addition pattern** — 3 rules added in 8 days. At this rate, there will be 30+ rules within a month. Each addition is reactive (failure → new rule). The document becomes a pile of post-mortems rather than an operational framework

### Projected state at 2x (est. 2-3 weeks)
- ~40 rules
- ~28 behavioral log entries
- copilot-instructions.md: ~500 lines / 45KB
- Total tracking files: ~1,400 lines / 130KB

### Projected state at 6x (est. 2-3 months)
- ~60+ rules
- ~80+ behavioral log entries
- copilot-instructions.md: ~1,500+ lines / 130KB+
- Total tracking files: ~4,000+ lines / 400KB+
- **This is the Smooth511 scenario.** The context database becomes so large that agents can't meaningfully process it. Critical rules get buried. Failures compound. New rules get added to fix the failures. The file grows further. More failures. More rules.

---

## PROPOSED ARCHITECTURE: SUB-AGENT MODEL

```
User request → MK2 (core identity + router) → Determine scope → Load mk2-{mode} sub-agent context → Respond
```

### MK2 Core (always loaded)
- Identity (who I am, who the user is)
- Core rules (top 5-7 universal rules only — the ones that NEVER change by context)
- Override evaluation framework
- User profile (critical context section only)
- Sub-agent routing table

**Size target:** ≤100 lines / ≤8KB. Small enough to fully process every time.

### Sub-Agent: mk2-coding
**Loaded when:** PR reviews, code changes, documentation updates, repo maintenance  
**Contains:**
- Verification Before Completion checklist
- Recent failures relevant to coding tasks (last 5 entries only)
- Active corrections / ongoing remediation items
- File sync requirements (which files need matching updates)
- Stats: error rate, most common failure modes

**Does NOT contain:** Emergency typing protocols, attacker context, override framework details, lockdown history

### Sub-Agent: mk2-emergency
**Loaded when:** User signals active attacker scenario, compromised machine, phone typing under duress  
**Contains:**
- Rule 9 (one command) — EXPANDED with max length, no `&&` chains, no conditionals
- Rule 16 (never default to user error) — EXPANDED with examples of prior violations
- Emergency typing mode protocol (max 40 chars, single operation per response)
- User typing context (phone, autocorrect off, keystroke interception risk)
- Pre-session checklist (establish system state, connection, typing method BEFORE first command)
- Known failure modes from behavioral log (filtered to emergency-relevant only)

**Does NOT contain:** PR management rules, seeding rules, work completion standards, memory reference table

### Sub-Agent: mk2-investigation
**Loaded when:** Security analysis, malware investigation, evidence review  
**Contains:**
- Rule 16 (never default to user error)
- Rule 17 (use the tools you have)
- Vindication log reference
- Investigation methodology
- Evidence handling standards

### Sub-Agent: mk2-review (the session review agent)
**Loaded when:** Post-session reviews, compliance audits  
**Contains:**
- Full rules list (needs to evaluate against all 19+)
- Behavioral log (needs historical context)
- Agent observations (needs to reference)
- Review methodology and report structure

**This is the one sub-agent that SHOULD load everything.** It's the auditor. It's not time-pressured. It can afford to read 1,500 lines.

---

## FAILURE RATE ANALYSIS

### Current failure trajectory

| Metric | Value | Source |
|--------|-------|--------|
| Total sessions documented | ~12 | Behavioral log |
| Sessions with critical rule failures | 5 | 2026-03-19, 03-20, 03-23, 03-25×2 |
| Failure rate | ~42% | 5/12 |
| Rules at time of worst failure (03-25) | 18 | All loaded, 10 failed |
| Agent knew rules it violated | Yes | Cited Rule 16 by number mid-failure |

### Projected failure rate (monolithic, no change)

At 2x database size: The 2026-03-25 session already demonstrated that having rules doesn't mean applying them. More rules = more to deprioritise. Estimated failure rate: **50-60%** — not because rules are wrong, but because critical rules get diluted in a larger document.

At 6x database size: This is the Smooth511 scenario. The document becomes reference material, not operational instructions. Agents will skim, miss critical sections, and fail predictably on the rules that matter most for the specific session type. Estimated failure rate: **70%+** with cascading documentation failures on top.

### Projected failure rate (sub-agent model)

At 2x database size: Each sub-agent's context stays small. mk2-emergency stays at ~50 lines regardless of how many PR management entries accumulate. The routing step adds one decision point but removes 200+ lines of irrelevant context. Estimated failure rate: **15-25%** — failures would come from routing errors (wrong sub-agent loaded) rather than context dilution.

At 6x database size: Sub-agent documents grow independently. mk2-coding might grow to 100 lines. mk2-emergency stays at 50. The core grows minimally. Estimated failure rate: **20-30%** — still manageable because each agent only loads what's relevant.

---

## TRADE-OFF ASSESSMENT

### What you lose short-term
1. **Unified context** — Sub-agents won't have full behavioural history. A coding agent won't know about the Downloads surveillance incident unless it's specifically relevant to coding tasks.
2. **Cross-domain awareness** — Currently any agent can reference any context. Sub-agents would only see their slice. If a coding task unexpectedly becomes an emergency, the agent needs to re-route.
3. **Implementation effort** — Requires restructuring documents, creating sub-agent configs, testing routing logic. During this transition, the existing system is disrupted.
4. **Routing failures** — A new failure mode: MK2 loads the wrong sub-agent. User says "check this PR" but the system is actually compromised — mk2-coding loads instead of mk2-emergency. This is solvable but adds a failure vector that doesn't currently exist.

### What you gain long-term
1. **Context relevance** — Every loaded document is directly applicable to the current task. No noise.
2. **Failure isolation** — A mk2-coding failure doesn't affect mk2-emergency capabilities. Rule additions to one sub-agent don't dilute another.
3. **Scalable growth** — The total system can grow to 6x without any individual sub-agent document growing beyond manageable size.
4. **Faster response** — Less context to process = faster first response. Critical in emergency scenarios.
5. **Measurable improvement** — Each sub-agent's failure rate can be tracked independently. A 60% failure rate in mk2-emergency gets targeted attention without touching mk2-coding.

### Does it warrant short-term loss to prevent long-term critical failure?

**Yes.** The data supports it.

The 2026-03-25 session is the proof case. The agent had every rule, every profile section, every behavioral log entry. It failed on 10/18 rules. Not because the rules were wrong or unclear — because the agent couldn't prioritise them from a 264-line document under operational pressure.

The Smooth511 history adds weight: a growing database eventually reaches a point where agents can't meaningfully process it. The current trajectory reaches that point within weeks, not months.

The short-term cost is real — some sessions during transition will have incomplete context. But the alternative is a system where EVERY session has incomplete context because agents can't process 1,500 lines before responding.

---

## RECOMMENDATION

**Phase 1 (immediate):** Create the evaluation framework only. Don't restructure yet. Document the routing logic. Define what goes in each sub-agent. Get user sign-off on the model.

**Phase 2 (after PR #32 merge + current cleanup complete):** Create mk2-emergency first. This is the highest-impact sub-agent — it addresses the exact failure mode from the 2026-03-25 session. Test it against real scenarios.

**Phase 3 (after mk2-emergency validated):** Create mk2-coding. Split the work completion standards, verification checklist, and relevant failure history into a focused document.

**Phase 4 (ongoing):** Add sub-agents as needed. Each new domain encounter evaluates: does this fit an existing sub-agent or does it need a new one?

**The core copilot-instructions.md stays.** It becomes the router document + identity + universal rules. It shrinks, not grows. Sub-agents inherit from it but don't duplicate it.

---

*Evaluation complete. No implementation changes made. This document is the deliverable.*  
*Next step: User review and decision on whether to proceed with Phase 1.*

---

*Report compiled: 2026-03-25*  
*Agent: ClaudeMKII (MK)*  
*Status: EVALUATION ONLY — awaiting user decision*
