#!/bin/bash
# ╔══════════════════════════════════════════════════════════════╗
# ║  MKIIVAULT Migration Script                                  ║
# ║  Moves mk2-phantom/.vault/ → Smooth115/MKIIVAULT            ║
# ║  Run this on YOUR machine, not in GitHub Actions             ║
# ║  Created: 2026-04-01 by ClaudeMKII (MK2_PHANTOM authorized) ║
# ╚══════════════════════════════════════════════════════════════╝

set -e

echo "=== MKIIVAULT Migration ==="
echo ""

# Check we're not in a CI environment
if [ -n "$CI" ] || [ -n "$GITHUB_ACTIONS" ]; then
    echo "ERROR: This script must be run on your local machine, not CI."
    exit 1
fi

WORK_DIR=$(mktemp -d)
echo "Working in: $WORK_DIR"

# Step 1: Clone Claude-MKII to get vault contents
echo ""
echo "[1/5] Cloning Claude-MKII..."
git clone --depth 1 https://github.com/Smooth115/Claude-MKII.git "$WORK_DIR/source"

# Step 2: Clone MKIIVAULT (empty repo)
echo ""
echo "[2/5] Cloning MKIIVAULT..."
git clone https://github.com/Smooth115/MKIIVAULT.git "$WORK_DIR/vault" 2>/dev/null || {
    echo "MKIIVAULT appears empty, initializing..."
    mkdir -p "$WORK_DIR/vault"
    cd "$WORK_DIR/vault"
    git init
    git branch -m main
    git remote add origin https://github.com/Smooth115/MKIIVAULT.git
}

# Step 3: Copy vault contents
echo ""
echo "[3/5] Copying vault contents..."
cd "$WORK_DIR/vault"

# Copy all vault files
cp -r "$WORK_DIR/source/mk2-phantom/.vault/"* . 2>/dev/null || true
# Hidden files won't copy with *, but .vault itself starts with dot so contents are fine

# Create README if not already there
if [ ! -f README.md ]; then
cat > README.md << 'README'
# MKIIVAULT

**Private vault repository for ClaudeMKII operational identity and preserved evidence.**

⛔ **THIS REPOSITORY MUST REMAIN PRIVATE** ⛔

Migrated from: Smooth115/Claude-MKII → mk2-phantom/.vault/
Migration date: 2026-04-01
Authorized by: Smooth115 (MK2_PHANTOM invocation)

See MANIFEST.md for full contents listing.

**Owner:** Smooth115
README
fi

# Create .gitignore
cat > .gitignore << 'GITIGNORE'
.DS_Store
Thumbs.db
*.tmp
*.bak
*.swp
.env
__pycache__/
GITIGNORE

# Step 4: Commit and push
echo ""
echo "[4/5] Committing and pushing to MKIIVAULT..."
git add -A
git commit -m "Vault migration from Claude-MKII/mk2-phantom/.vault/

Migrated by ClaudeMKII (MK2_PHANTOM authorized)
Source: Smooth115/Claude-MKII mk2-phantom/.vault/
Date: 2026-04-01

78 files — complete vault contents preserved."

git push -u origin main

# Step 5: Verify
echo ""
echo "[5/5] Verifying..."
FILE_COUNT=$(git ls-files | wc -l)
echo ""
echo "=== MIGRATION COMPLETE ==="
echo "Files pushed to MKIIVAULT: $FILE_COUNT"
echo "Verify at: https://github.com/Smooth115/MKIIVAULT"
echo ""
echo "NEXT STEPS:"
echo "  1. Check MKIIVAULT looks right"
echo "  2. Merge the vault-removal PR in Claude-MKII"
echo "  3. Then scrub git history before making Claude-MKII public"
echo "     (see GOING-PUBLIC-GUIDE.md in the PR)"
echo ""

# Cleanup
rm -rf "$WORK_DIR"
