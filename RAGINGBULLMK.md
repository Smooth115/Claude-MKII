# 🛡️ Protocol RagingbullMK — Core Repository Defence

**Codename:** RagingbullMK  
**Status:** ACTIVE  
**Implemented:** 2026-03-24  
**Authority:** Smooth115 (explicit instruction)  
**Enforced by:** `.github/workflows/ragingbull-mk.yml`

---

## What It Does

RagingbullMK is an automated defence hook that fires whenever a PR or commit touches
protected core files. It blocks the event chain **before** review, auto-merge, or merge
can proceed, and notifies the user immediately.

### Trigger conditions

Any PR or commit (push) that modifies:

| Category | Examples |
|----------|---------|
| Files with `_MK` anywhere in path/name | `_MKII-MEMORY.md`, `_MKII-AGENT-ACCESS.md`, `_MKII-AGENT-NOTICE.md` |
| Core agent config | `.github/copilot-instructions.md`, `.github/agents/ClaudeMKII.agent.md` |
| Lockdown records | `LOCKDOWN-FINAL-REPORT.md` |
| Vault identity files | `mk2-phantom/.vault/core-identity.md`, `mk2-phantom/.vault/access-control.md` |
| This workflow itself | `.github/workflows/ragingbull-mk.yml` |

---

## What Happens When Triggered

1. **Unauthorized agent scan** — PR body, title, and commit messages are checked for
   references to banned models (Sonnet, GPT, Gemini). If found, severity escalates to
   CRITICAL and all actions are halted.

2. **Defensive trigger comment** — A `🛡️ RagingbullMK: Defensive Trigger` comment is
   posted to the PR immediately, listing the protected files and block status. This
   appears **before** any review can be requested.

3. **Label applied** — The `RagingbullMK` label (red) is added to the PR for audit trail
   and visibility.

4. **User alert issue** — A GitHub issue is created with `@Smooth115` as the audience,
   severity rating (WARNING / CRITICAL), and a direct link to the PR. The issue serves
   as the notification and action record.

5. **Check fails** — The `RagingbullMK Defence Scan` check exits with a non-zero status.
   When branch protection is configured to require this check, merge is **physically
   blocked** until an authorized agent clears it.

---

## Authorization

| Entity | Override Authority |
|--------|-------------------|
| `claude-opus-4.6` (ClaudeMKII) | ✅ Full — can inspect, verify, approve |
| Smooth115 (repo owner) | ✅ Full — can override via direct push or settings |
| Any Sonnet/GPT/Gemini model | ⛔ NONE — halted on detection |
| Any unrecognized bot | ⛔ NONE — flagged as suspicious |

---

## Enabling Full Merge Block (Branch Protection)

The failing check alone does not prevent merge unless branch protection requires it.
To fully enforce the block:

1. Go to **Settings → Branches → Add branch protection rule**
2. Branch name pattern: `main`
3. Enable **"Require status checks to pass before merging"**
4. Search for and add: `RagingbullMK Defence Scan`
5. Enable **"Require branches to be up to date before merging"**
6. Save

Once configured, **no PR touching a protected file can be merged** without the check passing.

---

## Clearing a Triggered Block

When RagingbullMK fires on a legitimate change (authorized Opus/ClaudeMKII action):

1. Authorized agent (Opus/ClaudeMKII) reviews every change in the PR for compliance
2. Agent confirms no unauthorized model involvement
3. Agent confirms all changes are authorized and correct
4. User (`Smooth115`) approves the PR
5. The RagingbullMK alert issue is closed
6. PR merges normally

The failing check is intentional — it requires **human + authorized agent sign-off**
before any core file can change.

---

## Direct Push Alerts

When core files are modified via direct push (bypassing PRs), RagingbullMK:

- Creates a `⚠️ RagingbullMK [PUSH ALERT]` issue with the commit link and pusher
- Note: A direct push cannot be blocked after it happens — the alert is for immediate
  review. If the push was unauthorized, lock the branch and audit the commit.

---

## Audit Trail

Every RagingbullMK trigger creates:

- A comment on the PR (permanent, visible in PR timeline)
- A GitHub issue (with the `RagingbullMK` label, stays open until manually closed)
- A failed workflow run with step summary (logged in Actions history)

---

## File Pattern Reference

The `_MK` trigger catches any file matching the regex `(^|/)_MK|_MK[^/]` in its path.
This covers all current and future `_MKII-*` files automatically.

To add a new named file to protection (files that don't carry `_MK`), edit the `case`
block in `.github/workflows/ragingbull-mk.yml` step **"Detect core file changes"**.

---

*RagingbullMK — because rogue Sonnet meltdowns and snowball PRs stop here.*
