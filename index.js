import { spawn } from 'child_process';
import schedule from 'node-schedule';
import { config } from 'dotenv';
import simpleGit from 'simple-git';

config();
const git = simpleGit();

// Schedule random commits throughout the day
schedule.scheduleJob('*/30 * * * *', async () => {
  try {
    // Run Python script to generate files
    // Execute Python directly with console output
    const scriptPath = process.cwd() + '/file_operations.py';
    console.log('Executing Python script:', scriptPath);
    
    const python = spawn('python', [scriptPath], {
      env: { ...process.env, PYTHONPATH: process.cwd() },
      cwd: process.cwd(),
      stdio: 'pipe'
    });

    // Handle process events
    python.on('error', (err) => {
      console.error('Failed to start Python process:', err);
    });
    
    python.stdout.on('data', (data) => {
        console.log('Python output:', data.toString());
    });
    
    python.stderr.on('data', (data) => {
        console.error('Python error:', data.toString());
    });
    
    python.on('close', async (code) => {
      if (code === 0) {
        // Git operations
        await git.add('.');
        await git.commit('Update generated files');
        await git.push('origin', 'main');
        console.log('Successfully pushed changes');
      } else {
        console.error('Python script failed');
      }
    });
  } catch (error) {
    console.error('Error:', error);
  }
});

console.log('GitHub contribution automation started');