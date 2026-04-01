const { chromium } = require('C:\\Users\\User\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\playwright-core');
const fs = require('fs');

const url = process.argv[2];
let promptText = process.argv[3];
const waitSec = parseInt((process.argv.find(a => a.startsWith('--wait=')) || '--wait=900').split('=')[1]);

if (promptText && fs.existsSync(promptText)) {
  promptText = fs.readFileSync(promptText, 'utf8');
}

async function main() {
  if (!url || !promptText) { console.log('Usage: node chatgpt-send-v2.js <url> <prompt|file> [--wait=900]'); process.exit(1); }

  console.log('Connecting...');
  const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('chatgpt'));
  if (!page) { console.log('No ChatGPT page found. Navigate manually first.'); process.exit(1); }
  
  // Optionally navigate to a different URL
  if (url && !page.url().includes(url.split('?')[0].split('#')[0].replace('https://chatgpt.com', ''))) {
    console.log('Navigating to target URL:', url);
    await page.goto(url, { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(8000);
  }
  
  console.log('On page:', page.url());

  // Focus the contenteditable div (ProseMirror editor)
  // The textarea#prompt-textarea is hidden — the real input is the contenteditable div
  console.log('Looking for input...');
  const inputFound = await page.evaluate(() => {
    const el = document.querySelector('div[contenteditable="true"]') ||
               document.querySelector('.ProseMirror');
    if (el) {
      el.focus();
      el.click();
      return 'found: ' + el.className.substring(0, 50);
    }
    // Fallback: check for any visible textarea
    const ta = document.querySelector('textarea');
    if (ta) { ta.focus(); ta.click(); return 'textarea fallback'; }
    return 'no input found';
  });
  console.log('Input:', inputFound);
  await page.waitForTimeout(500);
  
  // Clear existing text
  await page.keyboard.press('Control+a');
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(300);
  
  // Type the prompt using keyboard typing (most compatible with ProseMirror)
  console.log('Typing prompt (' + promptText.length + ' chars)...');
  // Type via clipboard paste (fast and reliable)
  await page.evaluate((text) => {
    navigator.clipboard.writeText(text);
  }, promptText);
  await page.keyboard.press('Control+v');
  await page.waitForTimeout(1000);
  
  // Check if paste worked
  let textLen = await page.evaluate(() => {
    const el = document.querySelector('div[contenteditable="true"]');
    return el ? el.innerText.length : 0;
  });
  console.log('After paste, input length:', textLen);
  
  // If paste didn't work, use execCommand
  if (textLen < 100) {
    console.log('Paste failed, trying execCommand insertText...');
    await page.evaluate((text) => {
      const el = document.querySelector('div[contenteditable="true"]');
      if (el) {
        el.focus();
        document.execCommand('insertText', false, text);
      }
    }, promptText);
    await page.waitForTimeout(1000);
    textLen = await page.evaluate(() => {
      const el = document.querySelector('div[contenteditable="true"]');
      return el ? el.innerText.length : 0;
    });
    console.log('After insertText, input length:', textLen);
  }
  
  // If still no text, use type (slow but reliable)
  if (textLen < 100) {
    console.log('insertText failed, typing character by character...');
    // Type a short sample to trigger React state
    await page.keyboard.type(promptText.substring(0, 500), { delay: 1 });
    await page.waitForTimeout(500);
    textLen = await page.evaluate(() => {
      const el = document.querySelector('div[contenteditable="true"]');
      return el ? el.innerText.length : 0;
    });
    console.log('After keyboard.type (500 chars), input length:', textLen);
  }
  await page.waitForTimeout(1000);
  
  // Check state before sending
  const state1 = await page.evaluate(() => {
    const el = document.querySelector('div[contenteditable="true"]');
    const btn = document.querySelector('button[data-testid="send-button"]');
    return {
      inputLen: el ? el.innerText.length : 0,
      sendExists: !!btn,
      sendDisabled: btn ? btn.disabled : null,
      sendLabel: btn ? btn.getAttribute('aria-label') : null
    };
  });
  console.log('Pre-send state:', JSON.stringify(state1));

  // Click send button using Playwright's native click (not evaluate)
  // Playwright's click dispatches proper mouse events that React detects
  console.log('Clicking send...');
  try {
    await page.locator('button[data-testid="send-button"]').first().click({ timeout: 5000 });
    console.log('Clicked send button via Playwright locators');
  } catch (e) {
    console.log('data-testid failed, trying aria-label...');
    try {
      await page.locator('button[aria-label*="Send"]').first().click({ timeout: 5000 });
      console.log('Clicked send via aria-label');
    } catch (e2) {
      console.log('Aria-label also failed. Trying keyboard...');
      await page.keyboard.press('Control+Enter');
    }
  }

  // Wait for response
  console.log('Waiting for response (up to ' + waitSec + 's)...');
  const startTime = Date.now();
  const timeoutMs = waitSec * 1000;
  let responseText = '';
  
  while (Date.now() - startTime < timeoutMs) {
    await page.waitForTimeout(10000);
    
    const state = await page.evaluate(() => {
      // Main page messages
      const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
      const stopBtn = document.querySelector('button[data-testid="stop-button"]');
      const regenBtn = document.querySelector('button[aria-label*="Regenerate"]');
      const last = msgs[msgs.length - 1];
      const mainLen = last ? (last.querySelector('.markdown')?.innerText || last.innerText || '').length : 0;
      
      // Check for response indicator in main page
      const hasResponse = msgs.length > 0 || mainLen > 0;
      
      // Also check for "Get a detailed report" or Deep Research status
      const drStatus = document.body.innerText.match(/(?:Get a detailed|Research completed|research completed|searches)/i);
      
      return {
        msgCount: msgs.length,
        generating: !!stopBtn,
        complete: !!regenBtn,
        lastLen: mainLen,
        hasResponse,
        drStatus: drStatus ? drStatus[0] : null
      };
    });
    
    // Also check frames for Deep Research content
    const frameCount = page.frames().length;
    let frameText = '';
    if (frameCount > 1 && !state.hasResponse) {
      for (let i = 1; i < page.frames().length; i++) {
        try {
          const text = await page.frames[i].evaluate(() => {
            const main = document.querySelector('main') || document.querySelector('[role="main"]');
            return main ? main.innerText : (document.body ? document.body.innerText : '');
          });
          if (text.length > frameText.length) frameText = text;
        } catch(e) {}
      }
    }
    
    // Merge frame text into state
    if (frameText.length > state.lastLen) {
      state.lastLen = frameText.length;
      state.fromFrame = true;
      // Check for completion indicators in frame
      if (frameText.includes('Export') || frameText.includes('Copy contents')) {
        state.complete = true;
      }
    }
    
    const elapsed = Math.round((Date.now() - startTime) / 1000);
    console.log(`[${Math.floor(elapsed/60)}m${elapsed%60}s] msgs=${state.msgCount} gen=${state.generating} done=${state.complete} len=${state.lastLen}`);
    
    if (state.complete) {
      // Extract final text
      responseText = await page.evaluate(() => {
        const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
        const last = msgs[msgs.length - 1];
        return last ? (last.querySelector('.markdown')?.innerText || last.innerText || '').trim() : '';
      });
      break;
    }
  }

  if (!responseText || responseText === 'NO RESPONSE FOUND') {
    console.log('Trying iframe extraction...');
    for (let i = 1; i < page.frames().length; i++) {
      try {
        const text = await page.frames[i].evaluate(() => {
          const main = document.querySelector('main') || document.querySelector('[role="main"]');
          return main ? main.innerText.trim() : (document.body ? document.body.innerText.trim() : '');
        });
        if (text.length > 200) {
          responseText = text;
          console.log('Got text from frame ' + i + ': ' + text.length + ' chars');
          break;
        }
      } catch(e) {}
    }
  }
  
  if (!responseText) {
    responseText = 'NO RESPONSE FOUND';
  }

  const outputPath = 'C:\\Users\\User\\Downloads\\chatgpt-response-' + Date.now() + '.md';
  fs.writeFileSync(outputPath, responseText);
  console.log(`Saved ${responseText.length} chars to ${outputPath}`);
  console.log('Chat URL:', page.url());
  
  await browser.close();
}

main().catch(e => { console.error('Fatal:', e.message); process.exit(1); });
