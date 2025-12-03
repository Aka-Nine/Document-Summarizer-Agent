#!/bin/bash
set -euo pipefail

echo "WARNING: This script rewrites git history to remove sensitive files. Read the comments before running."

echo "Files to remove: config/.env"

echo "Install git-filter-repo first (https://github.com/newren/git-filter-repo)."
echo "Example usage (will rewrite history and require force-push):"
cat <<'EOF'
git clone --mirror <your-repo-url> repo.git
cd repo.git
git filter-repo --path config/.env --invert-paths
git push --force --tags origin 'refs/heads/*'
EOF

echo "Alternatively, use BFG (https://rtyley.github.io/bfg-repo-cleaner/) for simpler patterns."

echo "Do NOT run this unless you understand the consequences and have backups. Coordinate with collaborators."
