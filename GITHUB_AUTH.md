# 🔐 GitHub Authentication - Quick Guide

## Step 1: Create Personal Access Token

I've opened the GitHub tokens page in your browser. If it didn't open, go to:
**https://github.com/settings/tokens**

1. Click **"Generate new token"** → **"Generate new token (classic)"**
2. **Name**: `iosmvp-push` (or any name you like)
3. **Expiration**: Choose your preference (90 days, 1 year, or no expiration)
4. **Select scopes**: Check ✅ **`repo`** (this gives full repository access)
5. Click **"Generate token"** at the bottom
6. **⚠️ IMPORTANT**: Copy the token immediately! It looks like `ghp_xxxxxxxxxxxxxxxxxxxx`
   - You won't be able to see it again!

## Step 2: Push to GitHub

Once you have your token, run:

```bash
cd /Users/deeshapathak/Desktop/iosmvp
git push origin main
```

When prompted:
- **Username**: Enter your GitHub username (e.g., `deeshapathak`)
- **Password**: Paste the token you just copied (NOT your GitHub password)

The credential helper will save this for future pushes.

## Alternative: Use SSH (One-time setup)

If you prefer SSH:

1. **Check if you have SSH keys**:
   ```bash
   ls -la ~/.ssh/id_rsa.pub
   ```

2. **If no key exists, generate one**:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter to accept defaults
   ```

3. **Add key to GitHub**:
   ```bash
   cat ~/.ssh/id_rsa.pub
   # Copy the output
   ```
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste the key and save

4. **Switch remote to SSH**:
   ```bash
   git remote set-url origin git@github.com:deeshapathak/iosmvp.git
   git push origin main
   ```

## Troubleshooting

**"Authentication failed"**
- Make sure you're using the token, not your password
- Check that the `repo` scope is selected
- Token might have expired - generate a new one

**"Permission denied"**
- Verify you have write access to the repository
- Check that the token has `repo` scope

**Want to use GitHub CLI instead?**
```bash
# Install GitHub CLI (requires Homebrew)
brew install gh

# Authenticate
gh auth login

# Then push
git push origin main
```

