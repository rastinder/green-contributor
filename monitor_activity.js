import axios from 'axios';
import { exec } from 'child_process';
import { config } from 'dotenv';
import { promisify } from 'util';

config();
const execAsync = promisify(exec);

const token = process.env.GITHUB_TOKEN;
const username = process.env.GITHUB_USERNAME;

async function checkStatus() {
    console.clear();
    const timestamp = new Date().toLocaleString();
    console.log(`\nStatus Check at ${timestamp}`);
    console.log('='.repeat(50));

    try {
        // Check PM2 Status
        console.log('\n1. PM2 Process Status:');
        console.log('-----------------');
        const { stdout: pm2Status } = await execAsync('pm2 status');
        console.log(pm2Status);

        // Configure GitHub API
        const gh = axios.create({
            baseURL: 'https://api.github.com',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/vnd.github.v3+json'
            }
        });

        // Check Recent Commits
        console.log('\n2. Recent Commits:');
        console.log('---------------');
        const { data: commits } = await gh.get(`/repos/${username}/green-contributor/commits`);
        commits.slice(0, 5).forEach(commit => {
            const date = new Date(commit.commit.author.date).toLocaleString();
            console.log(`${date}: ${commit.commit.message}`);
        });

        // Check Today's Contributions
        const query = `
        query {
            user(login: "${username}") {
                contributionsCollection {
                    contributionCalendar {
                        totalContributions
                        weeks {
                            contributionDays {
                                contributionCount
                                date
                            }
                        }
                    }
                }
            }
        }`;

        const graphqlResponse = await gh.post('https://api.github.com/graphql', { query });
        const today = new Date().toISOString().split('T')[0];
        const contributions = graphqlResponse.data.data.user.contributionsCollection.contributionCalendar;
        const todayContributions = contributions.weeks
            .flatMap(week => week.contributionDays)
            .find(day => day.date === today);

        console.log('\n3. Contribution Status:');
        console.log('--------------------');
        console.log(`Today's contributions: ${todayContributions?.contributionCount || 0}`);
        console.log(`Total contributions: ${contributions.totalContributions}`);

        // Check Active Code Generation
        console.log('\n4. Code Generation Status:');
        console.log('----------------------');
        const { stdout: codeContent } = await execAsync('type active_code.py');
        const functionCount = (codeContent.match(/def\s+\w+/g) || []).length;
        console.log(`Current Python functions: ${functionCount}`);
        
        // Check last modification time
        const { stdout: lastMod } = await execAsync('powershell -Command "(Get-Item active_code.py).LastWriteTime"');
        console.log(`Last code modification: ${lastMod.trim()}`);

        // Display next scheduled commit
        const { stdout: logs } = await execAsync('pm2 logs green-contributor --lines 1 --nostream');
        const scheduledMatch = logs.match(/Scheduled commit for (\d+:\d+)/);
        if (scheduledMatch) {
            console.log(`Next scheduled commit: ${scheduledMatch[1]}`);
        }

    } catch (error) {
        console.error('\nError:', error.response?.data || error.message);
    }

    console.log('\nNext check in 60 seconds...');
}

// Run initial check
checkStatus();

// Schedule checks every minute
setInterval(checkStatus, 60000);