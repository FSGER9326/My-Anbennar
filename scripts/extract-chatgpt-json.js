const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.connectOverCDP('ws://127.0.0.1:18800/devtools/page/26DE04CD984BA2DAAEC92583940D2812');
  const page = browser.contexts()[0].pages()[0];
  
  // Get all text from the last assistant message
  const messages = await page.locator('[data-message-author-role="assistant"]').all();
  if (messages.length === 0) {
    console.log('NO_MESSAGES');
    await browser.close();
    process.exit(0);
  }
  
  const lastMsg = messages[messages.length - 1];
  const text = await lastMsg.textContent();
  
  // Try to extract JSON array from the text
  const jsonMatch = text.match(/\[\s*\{[\s\S]*\}\s*\]/);
  if (jsonMatch) {
    console.log(jsonMatch[0]);
  } else {
    // Just print the full text
    console.log('RAW_TEXT:' + text.substring(0, 2000));
  }
  
  await browser.close();
})();
