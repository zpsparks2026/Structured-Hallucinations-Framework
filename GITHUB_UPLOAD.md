# GitHub Upload Instructions

## Quick Start (5 minutes)

### 1. Create GitHub Account (if needed)
- Go to https://github.com/signup
- Use your zpsparks@alaska.edu email
- Choose username (suggestion: "zpsparks" or "zachary-sparks")

### 2. Create New Repository
- Click "+" in top right → "New repository"
- Repository name: `structured-hallucinations-framework`
- Description: "Four-loop validation architecture for AI-assisted scientific discovery"
- Make it **Public** (so OpenAI can view it)
- **Do NOT** initialize with README (we already have one)
- Click "Create repository"

### 3. Upload Your Code
GitHub will show you commands. Use these instead:

```bash
# Navigate to your project folder
cd path/to/structured-hallucinations-framework

# Add GitHub as remote (replace YOUR-USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/structured-hallucinations-framework.git

# Push code to GitHub
git branch -M main
git push -u origin main
```

You'll be prompted for credentials:
- Username: your GitHub username
- Password: Use a **Personal Access Token** (not your GitHub password)

### 4. Create Personal Access Token (for password)
- Go to: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Note: "Upload from local machine"
- Select scopes: Check **repo** (full control)
- Click "Generate token"
- **COPY THE TOKEN** (you won't see it again)
- Use this token as your password when pushing

### 5. Verify Upload
- Go to https://github.com/YOUR-USERNAME/structured-hallucinations-framework
- You should see all your files
- README should display automatically

### 6. Update Your Resume
Replace the GitHub URL placeholder in your resume with:
```
https://github.com/YOUR-USERNAME/structured-hallucinations-framework
```

## Alternative: GitHub Desktop (Easier)
1. Download GitHub Desktop: https://desktop.github.com/
2. Sign in with your GitHub account
3. File → Add Local Repository → Select your folder
4. Publish repository
5. Done!

## What You'll Have

A professional GitHub repository showing:
- ✅ Complete working implementation
- ✅ Clear documentation
- ✅ Proper code structure
- ✅ MIT License
- ✅ Git commit history
- ✅ Professional README with diagrams

## Troubleshooting

**"Permission denied"**: Use Personal Access Token as password, not GitHub password

**"Repository already exists"**: Skip step 2, use existing repo URL

**"Fatal: not a git repository"**: Make sure you're in the correct folder

## Time Estimate
- If you have GitHub account: 3-5 minutes
- If creating new account: 8-10 minutes total

## Final Step
Once uploaded, add this to your resume in the RESEARCH section under "Structured Hallucinations":

**Add this line:**
"Implementation: github.com/YOUR-USERNAME/structured-hallucinations-framework"

Or in your cover letter, second paragraph, add:
"(implementation available at github.com/YOUR-USERNAME/structured-hallucinations-framework)"
