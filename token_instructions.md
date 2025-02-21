# GitHub Token Setup Instructions

1. Go to GitHub.com and log in
2. Click your profile picture → Settings
3. Scroll down to "Developer settings" (bottom left)
4. Click "Personal access tokens" → "Tokens (classic)"
5. Click "Generate new token" → "Generate new token (classic)"

Required Scopes:
- [x] repo (Full control of repositories)
- [x] read:user (Read all user profile data)
- [x] write:repo_hook (Hooks management)

Note: The current token appears to be expired or invalid. After generating a new token:
1. Copy the new token
2. Replace the GITHUB_TOKEN value in .env file
3. Update the git remote URL with the new token

Example token format: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

Important: Make sure to copy the token immediately after generation as it won't be shown again.