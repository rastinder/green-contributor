import { readFile, writeFile } from 'fs/promises';
import { execSync } from 'child_process';
import { config } from 'dotenv';

config();

async function migrateToken(newToken) {
    if (!newToken) {
        console.log('\nToken Migration Instructions:');
        console.log('---------------------------');
        console.log('1. Generate new token at: https://github.com/settings/tokens/new');
        console.log('2. Ensure these scopes are selected:');
        console.log('   - repo');
        console.log('   - read:user');
        console.log('   - write:repo_hook');
        console.log('3. Run this script with the new token:');
        console.log('   node migrate_token.js YOUR_NEW_TOKEN');
        return;
    }

    // Validate token format
    if (!newToken.startsWith('ghp_') || newToken.length !== 40) {
        console.error('\n❌ Invalid token format!');
        console.log('Token should:');
        console.log('- Start with "ghp_"');
        console.log('- Be exactly 40 characters long');
        return;
    }

    try {
        // Update .env file
        let envContent = await readFile('.env', 'utf8');
        envContent = envContent.replace(
            /GITHUB_TOKEN=.*/,
            `GITHUB_TOKEN=${newToken}`
        );
        await writeFile('.env', envContent);
        console.log('✓ Updated .env file');

        // Update git remote URL
        const remoteUrl = `https://${newToken}@github.com/rastinder/green-contributor.git`;
        execSync(`git remote set-url origin "${remoteUrl}"`);
        console.log('✓ Updated git remote URL');

        // Test the new token
        console.log('\nTesting new token...');
        const testCmd = 'node verify_token.js';
        execSync(testCmd, { stdio: 'inherit' });

    } catch (error) {
        console.error('\n❌ Error during migration:', error.message);
    }
}

// Get token from command line argument
const newToken = process.argv[2];
migrateToken(newToken);