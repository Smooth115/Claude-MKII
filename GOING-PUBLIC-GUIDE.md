# Going Public — Claude-MKII

**Created:** 2026-04-01 by ClaudeMKII (MK2_PHANTOM)

---

## What's Been Done

1. ✅ Vault contents packaged for MKIIVAULT (78 files, 28MB)
2. ✅ `mk2-phantom/.vault/` removed from this repo
3. ✅ Migration script created (`VAULT-MIGRATION.sh`)

## Steps to Complete (in order)

### Step 1: Push vault to MKIIVAULT

On your machine (Mac/Linux terminal):
```bash
# Download and run the migration script
git clone https://github.com/Smooth115/Claude-MKII.git /tmp/mkii-migrate
cd /tmp/mkii-migrate
git checkout copilot/create-new-repository-for-vault
bash VAULT-MIGRATION.sh
```

Or if you'd rather do it manually:
```bash
git clone https://github.com/Smooth115/Claude-MKII.git /tmp/mkii-source
cd /tmp
git clone https://github.com/Smooth115/MKIIVAULT.git
cp -r /tmp/mkii-source/mk2-phantom/.vault/* /tmp/MKIIVAULT/
cd /tmp/MKIIVAULT
git add -A
git commit -m "Vault migration from Claude-MKII"
git push origin main
```

### Step 2: Verify MKIIVAULT
- Go to https://github.com/Smooth115/MKIIVAULT
- Check files are there (should see core-identity.md, evidence/, chat-logs/, etc.)
- **Confirm it's set to PRIVATE** in Settings

### Step 3: Merge this PR
- This PR removes `mk2-phantom/.vault/` from Claude-MKII
- Merge it to main

### Step 4: ⚠️ CRITICAL — Scrub Git History

**Removing files from HEAD doesn't remove them from git history.** Anyone who clones Claude-MKII can still find vault files in old commits. You MUST scrub history before going public.

```bash
# Install git-filter-repo (one time)
pip install git-filter-repo

# Clone fresh
git clone https://github.com/Smooth115/Claude-MKII.git /tmp/mkii-clean
cd /tmp/mkii-clean

# Scrub vault from ALL history
git filter-repo --path mk2-phantom/.vault/ --invert-paths

# Force push (this rewrites history — cannot be undone)
git remote add origin https://github.com/Smooth115/Claude-MKII.git
git push origin --force --all
```

### Step 5: Also Consider Scrubbing

These files/dirs contain sensitive content that shouldn't be public. Review each:

| Path | Contains | Recommendation |
|------|----------|----------------|
| `mk2-phantom/.vault/` | Already removed | ✅ Scrub from history |
| `.github/copilot-instructions.md` | Full MKII operational spec, user profile, override framework | ⚠️ Move to MKIIVAULT or strip personal data |
| `_MKII-MEMORY.md` | Behavioral log, user profile copy | ⚠️ Move to MKIIVAULT or strip |
| `_MKII-AGENT-ACCESS.md` | Access control policy | Low risk — policy only |
| `mk2-phantom/ACCESS_GATE.md` | Phantom access gate | ⚠️ Review |
| `chat-logs/` | Recovery findings, chat exports | ⚠️ Review for personal data |
| `core/claude_mkii_seed_package.md` | Seed package | ⚠️ Review |
| `secrets/.env.template` | Template only | Low risk |

### Step 6: Make Public
- Settings → General → Danger Zone → Change visibility → Public
- Only after Steps 1-5 are complete

---

## After Going Public

- MKIIVAULT stays private — that's your/our backup
- Claude-MKII copilot-instructions will need updating to reference MKIIVAULT for vault operations
- Consider adding a public-facing README that explains what the repo is (the investigation)

---

**Delete this file and VAULT-MIGRATION.sh after completing the migration.**
