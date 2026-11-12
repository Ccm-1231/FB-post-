#!/usr/bin/env bash
# Usage: ./push_to_github.sh https://github.com/YOUR_USER/YOUR_REPO.git
set -e
[ -z "$1" ] && { echo "Usage: $0 <repo-url>"; exit 1; }
git init
git add .
git commit -m "Initial commit: Facebook poster app"
git branch -M main
git remote add origin "$1"
git push -u origin main
