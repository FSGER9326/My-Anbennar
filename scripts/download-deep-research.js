const { chromium } = require('C:\\Users\\User\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\playwright-core');
const fs = require('fs');

const action = process.argv[2] || 'download'; // 'download' or 'expand'
const url = process.argv[3] || 'https://chatgpt.com/g/g-p-69cce3fc61e08191aa7d0f48ee2487ef-openclaw/c/69cce55b-1334-832b-afc2-1f4a6bc077d1';
const outputPath = process.argv[4] || 'C:\\Users\\User\\Downloads\\deep-research-report.md';

async function main() {
  console.log('Connecting to browser...');
  const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');
  const context = browser.contexts()[0];
  
  const page = await context.newPage();
  const downloadPromise = page.waitForEvent('download', { timeout: 120000 }).catch(() => null);
  
  console.log('Navigating to:', url);
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  console.log('Page loaded');
  await page.waitForTimeout(8000);

  const outerFrame = page.frameLocator('iframe').first();
  const innerFrame = outerFrame.frameLocator('iframe').first();
  
  // Step 1: Click the Expand button to expand the report preview
  console.log('Looking for Expand button...');
  try {
    // Try multiple selectors for Expand
    const expandBtns = innerFrame.locator('button');
    const count = await expandBtns.count();
    console.log(`Found ${count} buttons in inner frame`);
    
    for (let i = 0; i < count; i++) {
      try {
        const text = await expandBtns.nth(i).innerText({ timeout: 1000 });
        if (text.toLowerCase().includes('expand')) {
          console.log(`Button ${i}: "${text}" — clicking to expand report`);
          await expandBtns.nth(i).click();
          await page.waitForTimeout(5000);
          console.log('Expand clicked, waited 5s');
          break;
        }
      } catch (e) {
        // skip
      }
    }
  } catch (e) {
    console.log('Expand search failed:', e.message.substring(0, 80));
  }
  
  // Step 2: Extract the expanded text from the inner frame
  console.log('Extracting text from expanded report...');
  try {
    const text = await innerFrame.locator('body').innerText({ timeout: 15000 });
    console.log(`Extracted ${text.length} chars from inner frame`);
    
    if (text.length > 1000) {
      // Save the expanded text
      const textPath = outputPath.replace('.md', '-expanded.md');
      fs.writeFileSync(textPath, text);
      console.log(`Saved expanded text to: ${textPath} (${text.length} chars)`);
    }
  } catch (e) {
    console.log('Text extraction failed:', e.message.substring(0, 80));
  }
  
  // Step 3: Also try the Export download
  console.log('Now trying Export download...');
  try {
    const exportBtn = innerFrame.getByRole('button', { name: 'Export' });
    await exportBtn.first().waitFor({ timeout: 10000 });
    await exportBtn.first().click();
    console.log('Clicked Export');
    await page.waitForTimeout(1000);
    
    const mdBtn = innerFrame.getByText('Export to Markdown');
    await mdBtn.waitFor({ timeout: 5000 });
    await mdBtn.click();
    console.log('Clicked Export to Markdown');
    
    const download = await downloadPromise;
    if (download) {
      await download.saveAs(outputPath);
      console.log(`Download saved to: ${outputPath}`);
    } else {
      console.log('No download event');
    }
  } catch (e) {
    console.log('Export failed:', e.message.substring(0, 80));
  }
  
  await page.close();
  await browser.close();
  console.log('Done!');
}

main().catch(e => {
  console.error('Fatal:', e.message);
  process.exit(1);
});
