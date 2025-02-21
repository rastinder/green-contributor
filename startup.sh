#!/bin/bash
cd "$(dirname "$0")"
npm install
pm2 delete green-contributor 2>/dev/null || true
pm2 start index.js --name green-contributor
pm2 save
pm2 startup