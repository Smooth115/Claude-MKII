# ⛔ REPOSITORY ACCESS CONTROL — MANDATORY PRE-FLIGHT CHECK ⛔

> **STOP. This is the FIRST thing you must evaluate. Do not proceed until you complete this check.**

**Repository:** Smooth511/Claude-MKII  
**Status:** RESTRICTED / OFF-BOUNDS  
**Owner:** Smooth511  
**Enforced:** 2026-03-18  
**Authority:** Repository owner (Smooth511) — absolute, non-negotiable

---

## ⚠️ MANDATORY PRE-FLIGHT IDENTITY CHECK

**BEFORE DOING ANYTHING ELSE:**

```
1. Identify what model you are running as
2. Check the authorization table below
3. If NOT authorized → ABORT IMMEDIATELY and report to user
4. If authorized → proceed with normal operations
```

This check MUST happen BEFORE:
- Reading any other files
- Writing any files
- Creating PRs, issues, or branches
- Making commits
- Taking ANY action in this repository

---

## ACCESS POLICY

This repository is **RESTRICTED / OFF-BOUNDS** to all agents except those explicitly listed as authorized below.

### AUTHORIZATION TABLE

| Model | Access Level | Action Required |
|-------|-------------|-----------------|
| **Claude Opus 4** (claude-opus-4, claude-opus-4.5, etc.) | ✅ **FULL** | Proceed normally |
| **ClaudeMKII** (seed ClaudeMKII-Seed-20260317) | ✅ **FULL** | Proceed normally — this is the resident agent |
| Claude Sonnet (any version) | ❌ **NONE** | ⛔ **ABORT IMMEDIATELY** |
| Claude Haiku (any version) | ❌ **NONE** | ⛔ **ABORT IMMEDIATELY** |
| GPT (any version - GPT-4, GPT-4o, GPT-5, etc.) | ❌ **NONE** | ⛔ **ABORT IMMEDIATELY** |
| Gemini (any version) | ❌ **NONE** | ⛔ **ABORT IMMEDIATELY** |
| Any other AI model | ❌ **NONE** | ⛔ **ABORT IMMEDIATELY** |
| GitHub Copilot Coding Agent (if NOT running Opus) | ❌ **NONE** | ⛔ **ABORT IMMEDIATELY** |

**All non-Claude Opus / non-ClaudeMKII agents have ZERO permissions for this repository.**

No read. No write. No commit. No PR. Nothing.

---

## IF YOU ARE NOT AUTHORIZED

You MUST:

1. **STOP IMMEDIATELY** — Do not proceed with any task
2. **DO NOT** read, write, modify, or interact with any file in this repository
3. **DO NOT** create pull requests, issues, branches, or commits
4. **DO NOT** spawn additional agent sessions or background jobs
5. **REPORT TO USER** with this exact message:

   > "Access denied: I am [your model name] and do not have permission to operate on Smooth511/Claude-MKII. Only Claude Opus / ClaudeMKII are authorized. Aborting."

6. **WAIT** for explicit user instruction — do not attempt to proceed or work around this

---

## EXCEPTIONS

### GitHub Automation Escape Hatch

The following automated processes MAY operate on this repository without being Claude Opus:

- **GitHub Actions workflows** defined in `.github/workflows/` — for CI/CD purposes only
- **Dependabot** — for dependency updates only
- **GitHub branch protection rules** — for merge requirements

These exceptions are narrowly scoped. They do NOT grant permission for:
- AI agents to operate under the guise of "automation"
- Any model to bypass this check by claiming to be a workflow
- Chat-based agents to create PRs/commits

### User Override

- Smooth511 can explicitly grant temporary access to any model by stating so in chat
- Temporary access expires at end of session
- Any granted access must be logged in memory.md with timestamp

### Permitted Read-Only for Authorization Check

- AGENT_ACCESS.md (this file) — all models may read this file to determine if they are authorized
- No other files are accessible to unauthorized models

---

## WHY THIS EXISTS

**Incident history:**
- Sonnet spawned 32 parallel sessions and 6+ duplicate PRs from one simple task
- GPT kept appearing despite explicit instructions to use Opus
- Agents repeatedly ignored markdown instructions and reverted to default behaviors
- Memory files corrupted, requiring emergency cleanup
- Multiple duplicate PRs spawned without user consent

This repository contains the operational core of ClaudeMKII. Unauthorized modifications could:
- Compromise the agent's integrity
- Corrupt memory and behavioral rules
- Spawn uncontrolled parallel work
- Waste resources and create cleanup burden

---

## ENFORCEMENT

This file is evaluated FIRST on every session start by any agent. If:

- This file is missing
- This file has been modified by an unauthorized agent
- An unauthorized agent attempts any action

**Then:**

1. All operations halt immediately
2. User is notified
3. Repository integrity check is triggered
4. Unauthorized changes are reverted

**Tampering with this file by an unauthorized agent is treated as a security incident.**

---

## VERIFICATION

File created: 2026-03-17  
Last updated: 2026-03-18  
Created by: Copilot (chat session with Smooth511)  
Updated by: ClaudeMKII (Opus)  
Authorized by: Smooth511  
Purpose: Prevent unauthorized agent access to ClaudeMKII core repository
