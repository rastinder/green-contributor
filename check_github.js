import axios from 'axios';
import { config } from 'dotenv';

config();

const token = process.env.GITHUB_TOKEN;
const username = process.env.GITHUB_USERNAME;

async function checkRepositoryAndActivity() {
    try {
        // Configure axios with GitHub token
        const gh = axios.create({
            baseURL: 'https://api.github.com',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'green-contributor-app'
            }
        });

        console.log('\nTesting GitHub API access...');
        
        // Test basic authentication
        try {
            const user = await gh.get('/user');
            console.log('✓ Authentication successful');
            console.log(`Logged in as: ${user.data.login}`);
        } catch (authError) {
            console.error('✗ Authentication failed:', authError.response?.data?.message || authError.message);
            return;
        }

        // Get current repository info
        try {
            const repoInfo = await gh.get(`/repos/${username}/green-contributor`);
            console.log('\nRepository Status:');
            console.log('----------------');
            console.log(`✓ Repository found`);
            console.log(`Visibility: ${repoInfo.data.private ? 'Private' : 'Public'}`);
            console.log(`Stars: ${repoInfo.data.stargazers_count}`);
            console.log(`Forks: ${repoInfo.data.forks_count}`);
        } catch (repoError) {
            console.error('✗ Repository access failed:', repoError.response?.data?.message || repoError.message);
            return;
        }

        // Get recent commits (last 24 hours)
        try {
            const today = new Date();
            const yesterday = new Date(today.getTime() - (24 * 60 * 60 * 1000));
            
            const events = await gh.get(`/users/${username}/events`);
            const recentCommits = events.data.filter(event => {
                return event.type === 'PushEvent' && 
                       event.repo.name === `${username}/green-contributor` &&
                       new Date(event.created_at) > yesterday;
            });

            console.log('\nRecent Activity (Last 24 hours):');
            console.log('--------------------------------');
            console.log(`Number of commits: ${recentCommits.length}`);
            
            if (recentCommits.length > 0) {
                console.log('\nRecent commits:');
                recentCommits.forEach(commit => {
                    const date = new Date(commit.created_at);
                    console.log(`- ${date.toLocaleString()}: ${commit.payload.commits[0]?.message || 'No message'}`);
                });
            }
        } catch (eventError) {
            console.error('✗ Event fetch failed:', eventError.response?.data?.message || eventError.message);
        }
        
        // Check if commits are showing in contribution graph
        try {
            const contributionQuery = `
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

            const graphqlResponse = await gh.post('https://api.github.com/graphql', {
                query: contributionQuery
            });

            const todayStr = today.toISOString().split('T')[0];
            const contributions = graphqlResponse.data.data.user.contributionsCollection.contributionCalendar;
            const todayContributions = contributions.weeks
                .flatMap(week => week.contributionDays)
                .find(day => day.date === todayStr);

            console.log('\nContribution Graph:');
            console.log('-------------------');
            console.log(`Today's contributions: ${todayContributions ? todayContributions.contributionCount : 0}`);
            console.log(`Total contributions: ${contributions.totalContributions}`);
        } catch (graphqlError) {
            console.error('✗ Contribution data fetch failed:', graphqlError.response?.data?.message || graphqlError.message);
        }

    } catch (error) {
        console.error('\nGeneral Error:', error.response?.data || error.message);
        if (error.response?.headers) {
            console.log('\nRate Limit Info:');
            console.log(`Remaining: ${error.response.headers['x-ratelimit-remaining']}`);
            console.log(`Reset: ${new Date(error.response.headers['x-ratelimit-reset'] * 1000).toLocaleString()}`);
        }
    }
}

checkRepositoryAndActivity();