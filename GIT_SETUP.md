# Git Setup Instructions

## Initial Setup

You've already committed your code locally. Now you need to connect to a GitHub repository.

## Option 1: Create New Repository on GitHub

1. **Go to GitHub and create a new repository:**
   - Visit https://github.com/new
   - Choose a repository name (e.g., `blockchain-fee-analyzer`)
   - Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (you already have these)
   - Click "Create repository"

2. **Add the remote and push:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## Option 2: Use Existing Repository

If you already have a repository on GitHub:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Option 3: Using SSH (if you have SSH keys set up)

```bash
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Troubleshooting

### "Permission denied" error
- Make sure you're authenticated: `gh auth login` (if using GitHub CLI)
- Or use Personal Access Token instead of password
- Check SSH keys if using SSH: `ssh -T git@github.com`

### "Repository not found" error
- Verify the repository name is correct
- Check that you have access to the repository
- Make sure the repository exists on GitHub

### "Branch main does not exist" error
- Your local branch is already `main` (good!)
- Just run: `git push -u origin main`

## Quick Commands Reference

```bash
# Check current remotes
git remote -v

# Add remote (replace with your repo URL)
git remote add origin https://github.com/USERNAME/REPO.git

# Check current branch
git branch

# Push to GitHub
git push -u origin main

# If you need to change remote URL
git remote set-url origin https://github.com/USERNAME/REPO.git
```

