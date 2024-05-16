// server.js
const path = require('path');

const { fork } = require('child_process');

const childProcess = fork(path.join(__dirname, 'index.js'));

childProcess.on('close', (code) => {
  console.log(`Child process exited with code ${code}`);
});
