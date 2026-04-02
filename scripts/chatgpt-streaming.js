// Extract ChatGPT response via CDP
const net = require('net');

async function getLastAssistantMessage() {
  const wsUrl = 'ws://127.0.0.1:18800/devtools/page/26DE04CD984BA2DAAEC92583940D2812';
  
  return new Promise((resolve, reject) => {
    const http = require('http');
    
    // Use Chrome DevTools Protocol via WebSocket
    const WebSocket = require('ws');
    const ws = new WebSocket(wsUrl);
    
    let messageBuffer = '';
    
    ws.on('open', () => {
      // Enable Page domain
      ws.send(JSON.stringify({ id: 1, method: 'Page.enable' }));
      ws.send(JSON.stringify({ id: 2, method: 'Runtime.enable' }));
    });
    
    ws.on('message', (data) => {
      const msg = JSON.parse(data.toString());
      if (msg.method === 'Runtime.consoleAPICalled') {
        const text = msg.params.args.map(a => a.value || '').join(' ');
        if (text.includes('A33_') || text.startsWith('[')) {
          messageBuffer += text + '\n';
        }
      }
    });
    
    ws.on('error', reject);
    
    setTimeout(() => {
      ws.close();
      resolve(messageBuffer || 'NO_CONTENT');
    }, 10000);
  });
}

getLastAssistantMessage().then(console.log).catch(console.error);
