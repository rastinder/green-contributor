# Green Contributor

This tool automates GitHub contributions by making random commits throughout the day.

## Setup

1. Create a new private GitHub repository
2. Clone it to your local machine
3. Copy these files into the repository
4. Configure the .env file:
   - Set your GitHub token in GITHUB_TOKEN
   - Set your GitHub username in GITHUB_USERNAME
5. Install dependencies:
```bash
npm install
```
5. Initialize git and set remote:
```bash
git init
git remote add origin YOUR_REPO_URL
git branch -M main
```
6. Make initial commit:
```bash
git add .
git commit -m "Initial commit"
git push -u origin main
```
7. Run the tool:
```bash
npm start
```

## Running as a Background Process (Windows)

1. Install pm2 globally:
```bash
npm install -g pm2
```

2. Start the process:
```bash
pm2 start index.js
```

3. Make it start on boot:
```bash
pm2 startup
pm2 save
```

4. To check status:
```bash
pm2 status
```

Note: This tool is for educational purposes only. Use responsibly.