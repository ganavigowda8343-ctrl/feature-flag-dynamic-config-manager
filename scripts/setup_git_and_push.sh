#!/usr/bin/env bash
set -e

REPO_NAME="feature-flag-dynamic-config-manager"
GITHUB_USER="ganavigowda8343-ctrl"
TARGET_DIR="/Users/macm2/.gemini/antigravity/scratch/feature-flag-manager"

echo "=========================================================="
echo " Setting up Git Repository for $GITHUB_USER"
echo "=========================================================="

cd "$TARGET_DIR"

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init -b main
    echo "Initialized git repository on branch main."
else
    git checkout -B main
fi

# Configure local git user if not globally set
git config user.name "Ganavi Gowda"
git config user.email "ganavigowda8343@users.noreply.github.com"

# Stage all files
git add .

# Commit
git commit -m "feat: Lab 1 Requirements Engineering & UML Use-Case Modelling for Feature Flag & Dynamic Config Manager" || echo "No new changes to commit."

# Set remote origin
REMOTE_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
if git remote | grep -q "origin"; then
    git remote set-url origin "$REMOTE_URL"
else
    git remote add origin "$REMOTE_URL"
fi

echo ""
echo "Repository prepared successfully!"
echo "Target Remote: $REMOTE_URL"
echo ""
echo "To push to GitHub, run:"
echo "  git push -u origin main"
echo ""
echo "Or if you have GitHub CLI authenticated:"
echo "  gh repo create ${GITHUB_USER}/${REPO_NAME} --public --source=. --remote=origin --push"
