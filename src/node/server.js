// server.js
const path = require('path')
const { spawn } = require('child_process')

const pythonProcess = spawn('python', [path.join(__dirname, '..', 'python', 'sip_client.py')])

pythonProcess.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`)
})

pythonProcess.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`)
})

pythonProcess.on('close', (code) => {
  console.log(`Python process exited with code ${code}`)
})