import { simpleGit } from 'simple-git';
import schedule from 'node-schedule';
import { config } from 'dotenv';
import { readFile, writeFile } from 'fs/promises';
import { join } from 'path';
import { spawn } from 'child_process';

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

const PYTHON_FILE = 'active_code.py';

// Initialize the active code file if it doesn't exist
async function initializeActiveCode() {
    try {
        await readFile(PYTHON_FILE);
    } catch {
        await writeFile(PYTHON_FILE, '# Active Python Code\n\n');
    }
}

// Function to run Python script and get output
async function getPythonOutput(scriptPath, functionName) {
    return new Promise((resolve, reject) => {
        const process = spawn('python', ['-c', `
import ${scriptPath.replace('.py', '')}
print(${scriptPath.replace('.py', '')}.${functionName}())
        `]);
        
        let output = '';
        process.stdout.on('data', (data) => {
            output += data.toString();
        });
        
        process.stderr.on('data', (data) => {
            console.error(`Python Error: ${data}`);
        });
        
        process.on('close', (code) => {
            if (code === 0) {
                resolve(output.trim());
            } else {
                reject(`Python process exited with code ${code}`);
            }
        });
    });
}

// Function to make random changes to code file
async function makeRandomChange() {
    const timestamp = new Date().toISOString();
    
    try {
        // Get current content of active code file
        const currentContent = await readFile(PYTHON_FILE, 'utf8');
        
        // Randomly decide to either add or remove code
        const shouldAdd = Math.random() > 0.5;
        
        let newContent;
        let commitMessage;
        
        if (shouldAdd) {
            // Get a random code snippet
            const snippet = await getPythonOutput('code_snippets', 'get_random_snippet');
            newContent = currentContent + '\n\n' + snippet;
            commitMessage = `feat: Add new function at ${timestamp}`;
        } else if (currentContent.trim() !== '') {
            // Remove a random existing function if file is not empty
            const lines = currentContent.split('\n');
            const functions = [];
            let currentFunc = [];
            
            // Find all function blocks
            for (const line of lines) {
                if (line.startsWith('def ')) {
                    if (currentFunc.length > 0) {
                        functions.push(currentFunc.join('\n'));
                        currentFunc = [];
                    }
                    currentFunc.push(line);
                } else if (currentFunc.length > 0) {
                    currentFunc.push(line);
                }
            }
            if (currentFunc.length > 0) {
                functions.push(currentFunc.join('\n'));
            }
            
            if (functions.length > 0) {
                // Remove a random function
                const indexToRemove = Math.floor(Math.random() * functions.length);
                functions.splice(indexToRemove, 1);
                newContent = functions.join('\n\n');
                commitMessage = `refactor: Remove function at ${timestamp}`;
            } else {
                // If no functions to remove, add one instead
                const snippet = await getPythonOutput('code_snippets', 'get_random_snippet');
                newContent = currentContent + '\n\n' + snippet;
                commitMessage = `feat: Add new function at ${timestamp}`;
            }
        } else {
            // If file is empty, definitely add code
            const snippet = await getPythonOutput('code_snippets', 'get_random_snippet');
            newContent = '# Active Python Code\n\n' + snippet;
            commitMessage = `feat: Add initial function at ${timestamp}`;
        }
        
        // Write the new content
        await writeFile(PYTHON_FILE, newContent);
        
        // Commit and push changes
        await git.add('.');
        await git.commit(commitMessage);
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

        // Initialize active code file
        await initializeActiveCode();
        
        // Make initial commit to test everything works
        await makeRandomChange();
        
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