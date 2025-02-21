import { simpleGit } from 'simple-git';
import { writeFile } from 'fs/promises';
import { config } from 'dotenv';
import axios from 'axios';

config();

const git = simpleGit();
const token = process.env.GITHUB_TOKEN;
const username = process.env.GITHUB_USERNAME;

async function testContribution() {
    try {
        // Make a test commit
        const timestamp = new Date().toISOString();
        const testFile = 'test_contribution.txt';
        await writeFile(testFile, `Test contribution at ${timestamp}`);
        
        // Commit and push
        await git.add(testFile);
        await git.commit(`test: verify contribution counting at ${timestamp}`);
        await git.push('origin', 'main');
        
        console.log('✓ Test commit pushed successfully');
        
        // Wait a moment for GitHub to process
        console.log('Waiting for GitHub to process...');
        await new Promise(resolve => setTimeout(resolve, 5000));
        
        // Check contribution count
        const gh = axios.create({
            baseURL: 'https://api.github.com',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/vnd.github.v3+json'
            }
        });

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

        const response = await gh.post('https://api.github.com/graphql', { query });
        const today = new Date().toISOString().split('T')[0];
        const contributions = response.data.data.user.contributionsCollection.contributionCalendar;
        const todayContributions = contributions.weeks
            .flatMap(week => week.contributionDays)
            .find(day => day.date === today);

        console.log('\nContribution Check:');
        console.log('------------------');
        console.log(`Today's contributions: ${todayContributions.contributionCount}`);
        console.log(`Total contributions: ${contributions.totalContributions}`);
        
        if (todayContributions.contributionCount > 0) {
            console.log('\n✓ Contributions are being counted successfully!');
        } else {
            console.log('\n⚠ No contributions detected. This might take a few minutes to update.');
        }

    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }
}

testContribution();