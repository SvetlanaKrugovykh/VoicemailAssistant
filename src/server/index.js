// index.js
const fs = require('fs');
const path = require('path');
require('dotenv').config();


const promptsCatalog = process.env.PROMPTS_CATALOG || './voice_messages';

(async () => {
  try {
    const { UserAgent } = await import('sip.js');

    const config = {
      uri: process.env.SIP_URI,
      authorizationUser: process.env.SIP_AUTHORIZATION_USER,
      password: process.env.SIP_PASSWORD,
    };

    const ua = new UserAgent(config);

    ua.on('invite', handleCall);

    function handleCall(session) {
      const callerNumber = session.request.from.uri.user;
      console.log('Incoming call from:', callerNumber);

      // Answer the call
      session.accept({
        media: {
          constraints: {
            audio: true,
            video: false
          },
        },
      });

      session.on('accepted', () => {
        console.log('Call accepted, playing greeting message...');
        const greetingFilePath = path.join(promptsCatalog, 'greeting.wav');

        fs.access(greetingFilePath, fs.constants.F_OK, (err) => {
          if (err) {
            console.error('File not found:', greetingFilePath);
          } else {
            session.play(greetingFilePath);
          }
        });
      });

      // Record the message
      session.on('message', (request) => {
        console.log('Message received:', request.body);

        // Save the message to a file
        const filename = 'message.wav';
        fs.writeFile(filename, request.body, (err) => {
          if (err) {
            console.error('Error saving message:', err);
          } else {
            console.log('Message saved to', filename);
          }
        });
      });

      // Hang up after recording
      session.on('bye', () => {
        console.log('Call ended.');
        session.bye();
      });
    }

    ua.start();
  } catch (error) {
    console.error('Error:', error);
  }
})();
