/**
 * ChatGPT Bridge — Submit prompts to ChatGPT via Playwright CDP connection
 * 
 * Usage: node chatgpt-bridge.js <url> <prompt> [--deep-research] [--extended-thinking] [--wait-ms=120000]
 * 
 * Examples:
 *   node chatgpt-bridge.js "https://chatgpt.com/g/g-p-69cce3fc61e08191aa7d0f48ee2487ef-openclaw/c/NEW" "Hello"
 *   node chatgpt-bridge.js "https://chatgpt.com/g/g-p-69cb9f6f4efc819188e90b492c235334-modding/c/NEW" "Research this" --deep-research --wait-ms=900000
 *   node chatgpt-bridge.js "https://chatgpt.com/g/g-p-69cce3fc61e08191aa7d0f48ee2487ef-openclaw/c/NEW" "Analyze" --extended-thinking --wait-ms=300000
 */

const { chromium } = require('C:\\Users\\User\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\playwright-core');

const url = process.argv[2];
const prompt = process.argv[3];
const useDeepResearch = process.argv.includes('--deep-research');
const useExtendedThinking = process.argv.includes('--extended-thinking');
const waitMs = parseInt(process.argv.find(a => a.startsWith('--wait-ms='))?.split('=')[1] || '120000');

async function main() {
  if (!url || !prompt) {
    console.log('Usage: node chatgpt-bridge.js <url> <prompt> [--deep-research] [--extended-thinking] [--wait-ms=N]');
    process.exit(1);
  }

  console.log('Connecting to browser...');
  const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');
  const context = browser.contexts()[0];
  const page = await context.newPage();
  
  console.log('Navigating to:', url);
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  console.log('Page loaded');
  await page.waitForTimeout(3000);

  // Find the prompt textarea in the main page
  const promptTextarea = page.locator('textarea#prompt-textarea');
  await promptTextarea.waitFor({ timeout: 15000 });
  console.log('Found prompt textarea');

  // Fill in the prompt
  await promptTextarea.fill(prompt);
  await page.waitForTimeout(500);

  // Check if we need to enable Deep Research
  if (useDeepResearch) {
    console.log('Looking for Deep Research toggle...');
    // Deep Research is in a toolbar area — look for it
    const drToggle = page.getByRole('button', { name: /deep.?research/i });
    const drCount = await drToggle.count();
    console.log(`Found ${drCount} Deep Research buttons`);
    if (drCount > 0) {
      // Check if it's already enabled (button text says "Deep research, click to remove")
      const firstBtn = drToggle.first();
      const btnText = await firstBtn.textContent().catch(() => '');
      console.log('DR button text:', btnText);
      if (!btnText.toLowerCase().includes('remove')) {
        await firstBtn.click();
        console.log('Enabled Deep Research');
        await page.waitForTimeout(500);
      } else {
        console.log('Deep Research already enabled');
      }
    }
  }

  // Check if we need to enable Extended Thinking  
  if (useExtendedThinking) {
    console.log('Looking for Extended Thinking toggle...');
    const etToggle = page.getByRole('button', { name: /extended.?thinking/i });
    const etCount = await etToggle.count();
    console.log(`Found ${etCount} Extended Thinking buttons`);
    if (etCount > 0) {
      const firstBtn = etToggle.first();
      const btnText = await firstBtn.textContent().catch(() => '');
      if (!btnText.toLowerCase().includes('remove')) {
        await firstBtn.click();
        console.log('Enabled Extended Thinking');
        await page.waitForTimeout(500);
      } else {
        console.log('Extended Thinking already enabled');
      }
    }
  }

  // Send the message
  console.log('Sending prompt...');
  const sendBtn = page.getByRole('button', { name: /send/i });
  await sendBtn.first().click();
  console.log('Prompt sent!');

  // Wait for response to complete
  console.log(`Waiting up to ${waitMs/1000}s for response...`);
  
  // Strategy: wait for Regenerate button to appear (= response complete)
  try {
    await page.waitForSelector('button[aria-label*="Regenerate"], button[data-testid="regenerate-button"]', { timeout: waitMs });
    console.log('Response complete (Regenerate button detected)');
  } catch (e) {
    console.log('Timeout waiting for Regenerate. Checking current state...');
  }
  
  // Extract the last assistant message
  const lastText = await page.evaluate(() => {
    const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
    const last = msgs[msgs.length - 1];
    if (!last) return '';
    const md = last.querySelector('.markdown');
    return (md || last).innerText;
  });

  console.log('RESPONSE_LENGTH:', lastText.length);
  console.log('RESPONSE_START:', lastText.substring(0, 500));
  console.log('---RESPONSE_SEPARATOR---');
  console.log(lastText);
  
  await page.close();
  await browser.close();
  console.log('Done!');
}

main().catch(e => {
  console.error('Fatal:', e.message);
  process.exit(1);
});
