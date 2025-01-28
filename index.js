import { simpleGit } from 'simple-git';
import schedule from 'node-schedule';
import { config } from 'dotenv';
import { readFile, writeFile } from 'fs/promises';
import { join } from 'path';

config();

const git = simpleGit({
    config: [
        `http.proxy=`,
        `https.proxy=`,
        `credential.helper=`,
        `user.name=Automated Contributor`,
        `user.email=automated@example.com`
    ]
});

// Configure git authentication with token
process.env.GIT_ASKPASS = 'echo';
process.env.GIT_TERMINAL_PROMPT = '0';
process.env.GH_TOKEN = process.env.GITHUB_TOKEN;

// Function to make random changes to a file
async function makeRandomChange() {
    const timestamp = new Date().toISOString();
    const content = `Last updated: ${timestamp}\nRandom number: ${Math.random()}`;
    
    try {
        await writeFile('data.txt', content);
        await git.add('.');
        await git.commit(`Update ${timestamp}`);
        await git.push('origin', 'main');
        console.log(`Successful commit at ${timestamp}`);
    } catch (error) {
        console.error('Error making commit:', error);
    }
}

// Schedule random commits throughout the day
function scheduleCommits() {
    // Make between 1-10 commits per day at random times
    const commitsToday = Math.floor(Math.random() * 10) + 1;
    
    for (let i = 0; i < commitsToday; i++) {
        const hour = Math.floor(Math.random() * 24);
        const minute = Math.floor(Math.random() * 60);
        
        schedule.scheduleJob(`${minute} ${hour} * * *`, makeRandomChange);
        console.log(`Scheduled commit for ${hour}:${minute}`);
    }
}

// Initial setup
async function init() {
    try {
        // Ensure we're in a git repository
        const isRepo = await git.checkIsRepo();
        if (!isRepo) {
            console.error('Not a git repository. Please initialize one first.');
            process.exit(1);
        }

        // Initialize data file if it doesn't exist
        await writeFile('data.txt', 'Initial commit');
        
        // Schedule daily commits
        scheduleCommits();
        
        // Reschedule commits every day at midnight
        schedule.scheduleJob('0 0 * * *', scheduleCommits);
        
        console.log('Green contributor initialized successfully!');
    } catch (error) {
        console.error('Initialization error:', error);
        process.exit(1);
    }
}

init();