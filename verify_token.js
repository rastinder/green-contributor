import axios from 'axios';
import { config } from 'dotenv';

config();

const token = process.env.GITHUB_TOKEN;

async function verifyToken() {
    try {
        // Configure axios with GitHub token
        const gh = axios.create({
            baseURL: 'https://api.github.com',
            headers: {
                'Authorization': `Bearer ${token.trim()}`,
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'token-verification'
            }
        });

        console.log('Token Analysis:');
        console.log('---------------');
        console.log(`Token prefix: ${token.substring(0, 4)}...`);
        console.log(`Token length: ${token.length} characters`);

        // Check basic authentication
        try {
            const user = await gh.get('/user');
            console.log('\n✓ Authentication successful');
            console.log(`Username: ${user.data.login}`);
            
            // Check token scopes
            const { headers } = await gh.get('/rate_limit');
            const scopes = headers['x-oauth-scopes'] || 'none';
            console.log('\nToken Scopes:', scopes);
            
            // Check specific required scopes
            const requiredScopes = ['repo', 'read:user', 'write:repo_hook'];
            const availableScopes = scopes.split(', ');
            
            console.log('\nRequired Scopes Check:');
            requiredScopes.forEach(scope => {
                const hasScope = availableScopes.some(s => s === scope || s.startsWith(`${scope}:`));
                console.log(`${hasScope ? '✓' : '✗'} ${scope}`);
            });

            // Test repository access
            const repoResponse = await gh.get(`/repos/${user.data.login}/green-contributor`);
            console.log('\nRepository Access:');
            console.log(`✓ Can access repository`);
            console.log(`Visibility: ${repoResponse.data.private ? 'Private' : 'Public'}`);

            return true;
        } catch (authError) {
            console.error('\n✗ Authentication failed');
            console.error('Error:', authError.response?.data?.message || authError.message);
            if (authError.response?.headers) {
                console.log('\nResponse Headers:');
                console.log(JSON.stringify(authError.response.headers, null, 2));
            }
            return false;
        }

    } catch (error) {
        console.error('\nGeneral Error:', error.message);
        if (error.response?.data) {
            console.error('Response Data:', error.response.data);
        }
        return false;
    }
}

verifyToken();