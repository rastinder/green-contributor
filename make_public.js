import axios from 'axios';
import { config } from 'dotenv';

config();

const token = process.env.GITHUB_TOKEN;
const username = process.env.GITHUB_USERNAME;
const repo = 'green-contributor';

async function makeRepositoryPublic() {
    try {
        const gh = axios.create({
            baseURL: 'https://api.github.com',
            headers: {
                'Authorization': `token ${token}`,
                'Accept': 'application/vnd.github.v3+json'
            }
        });

        // Update repository visibility to public
        const response = await gh.patch(`/repos/${username}/${repo}`, {
            private: false
        });

        console.log('\nRepository Update Status:');
        console.log('------------------------');
        console.log(`Name: ${response.data.name}`);
        console.log(`Visibility: ${response.data.private ? 'Private' : 'Public'}`);
        console.log(`URL: ${response.data.html_url}`);
        console.log('\nRepository is now public. Your contributions will be counted on your profile.');
        
    } catch (error) {
        console.error('Error updating repository:', error.response?.data || error.message);
    }
}

makeRepositoryPublic();