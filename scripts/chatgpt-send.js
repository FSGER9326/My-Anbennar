/**
 * chatgpt-send.js — Send a prompt to an EXISTING ChatGPT conversation via Playwright CDP
 * 
 * Usage: node chatgpt-send.js <chatUrl> <promptFileOrText> [--wait=120]
 * 
 * Works with existing conversations (non-project pages are more reliable).
 * 
 * Based on today's learnings:
 * - Use load, not networkidle
 * - Wait 8s for hydration
 * - Use contenteditable div for input, not textarea
 * - Press Enter to send (more reliable than clicking send button)
 */

const { chromium } = require('C:\\Users\\User\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\playwright-core');
const fs = require('fs');

const url = process.argv[2];
let promptText = process.argv[3];
const waitSec = parseInt((process.argv.find(a => a.startsWith('--wait=')) || '--wait=120').split('=')[1]);

// If prompt is a file path, read it
if (promptText && fs.existsSync(promptText)) {
  promptText = fs.readFileSync(promptText, 'utf8');
}

async function main() {
  if (!url || !promptText) {
    console.log('Usage: node chatgpt-send.js <chatUrl> <promptText|promptFile> [--wait=120]');
    process.exit(1);
  }

  console.log('Connecting to browser...');
  const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');
  const context = browser.contexts()[0];
  const page = await context.newPage();
  
  console.log('Navigating to:', url);
  await page.goto(url, { waitUntil: 'load', timeout: 30000 });
  console.log('Page loaded, waiting 8s for hydration...');
  await page.waitForTimeout(8000);

  // Fill prompt using clipboard paste (most reliable for ProseMirror)
  console.log('Filling prompt via clipboard...');
  const textarea = page.locator('textarea#prompt-textarea').first();
  await textarea.waitFor({ timeout: 15000, state: 'visible' });
  await textarea.click();
  await page.waitForTimeout(300);
  
  // Use page.evaluate to set clipboard and paste
  await page.evaluate((text) => {
    // Find the contenteditable div and focus it
    const el = document.querySelector('div[contenteditable="true"]') || 
               document.querySelector('.ProseMirror');
    if (el) {
      el.focus();
      // Use execCommand for paste simulation which ProseMirror detects
      document.execCommand('insertText', false, text);
    }
  }, promptText);
  await page.waitForTimeout(1000);
  
  // Check if send button is now active
  const sendReady = await page.evaluate(() => {
    const btn = document.querySelector('button[data-testid="send-button"]');
    const state = btn ? { disabled: btn.disabled, label: btn.getAttribute('aria-label') } : null;
    const el = document.querySelector('div[contenteditable="true"]');
    const textLen = el ? el.innerText.length : 0;
    return { sendBtn: state, inputLength: textLen };
  });
  console.log('Input state:', JSON.stringify(sendReady));

  // Click send button
  const sendClicked = await page.evaluate(() => {
    const btn = document.querySelector('button[data-testid="send-button"]') ||
                document.querySelector('button[aria-label*="Send"]');
    if (btn && !btn.disabled) { btn.click(); return true; }
    return false;
  });
  
  if (sendClicked) {
    console.log('Sent via button click');
  } else {
    // Fallback: try typing a few chars to trigger React state, then Ctrl+Enter
    await page.keyboard.press('Control+Enter');
    console.log('Sent via Ctrl+Enter');
  }

  // Wait for response complete
  console.log('Waiting for response (up to ' + waitSec + 's)...');
  
  // First check: is the response in an iframe (Deep Research chat)?
  const frameCount = page.frames().length;
  console.log('Frames detected: ' + frameCount);
  
  // Poll for Regenerate button (response complete indicator)
  const startTime = Date.now();
  const timeoutMs = waitSec * 1000;
  let complete = false;
  
  while (Date.now() - startTime < timeoutMs) {
    await page.waitForTimeout(5000); // Check every 5s
    
    const state = await page.evaluate(() => {
      const stopBtn = document.querySelector('button[data-testid="stop-button"]');
      const regenBtn = document.querySelector('button[aria-label*="Regenerate"]');
      const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
      const lastText = msgs.length > 0 
        ? (msgs[msgs.length-1].querySelector('.markdown')?.innerText || msgs[msgs.length-1].innerText || '').trim()
        : '';
      return {
        generating: Boolean(stopBtn),
        complete: Boolean(regenBtn),
        msgCount: msgs.length,
        lastTextLength: lastText.length,
        lastTextPreview: lastText.substring(0, 100)
      };
    });
    
    const elapsed = Math.round((Date.now() - startTime) / 1000);
    console.log(`[${elapsed}s] msgs=${state.msgCount} len=${state.lastTextLength} gen=${state.generating} done=${state.complete}`);
    
    if (state.complete) {
      complete = true;
      break;
    }
  }
  
  if (!complete) {
    console.log('Timeout! Extracting whatever we have...');
  }
  
  // Extract full response — try main page first, then iframes
  let fullText = await page.evaluate(() => {
    const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
    if (msgs.length === 0) return '';
    const last = msgs[msgs.length - 1];
    return (last.querySelector('.markdown')?.innerText || last.innerText || '').trim();
  });
  
  // If no text in main page, try iframes
  if (!fullText) {
    console.log('No text in main page, checking iframes...');
    const frames = page.frames();
    for (let i = 1; i < frames.length; i++) { // skip main frame
      try {
        const frameText = await frames[i].evaluate(() => {
          const body = document.body;
          return body ? body.innerText : '';
        });
        if (frameText && frameText.length > 200) {
          fullText = frameText;
          console.log('Found text in frame ' + i + ' (' + frameText.length + ' chars)');
          break;
        }
      } catch (e) {
        // cross-origin frame, skip
      }
    }
  }
  
  // Save output
  const outputPath = 'C:\\Users\\User\\Downloads\\deep-research-' + Date.now() + '.md';
  fs.writeFileSync(outputPath, fullText);
  console.log('Saved ' + fullText.length + ' chars to ' + outputPath);
  
  // Get chat URL for future reference
  const chatUrl = page.url();
  console.log('Chat URL: ' + chatUrl);
  
  await page.close();
  await browser.close();
}

main().catch(e => {
  console.error('Fatal:', e.message);
  process.exit(1);
});
