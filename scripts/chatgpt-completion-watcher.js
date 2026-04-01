/**
 * chatgpt-completion-watcher.js — Event-driven ChatGPT response completion detector
 * 
 * Based on Deep Research report (3) + (4) findings:
 * - MutationObserver + Promise pattern (no DOM polling)
 * - Multi-indicator done: stop button gone + send enabled + content stable
 * - Fallback: send button disabled attribute watch
 * 
 * Usage via Playwright (connect to existing CDP browser):
 *   const answer = await waitForCompletion(page, 300000);
 * 
 * Can also be injected via OpenClaw evaluate() as a standalone script.
 */

const { chromium } = require('C:\\Users\\User\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\playwright-core');

/**
 * Wait for ChatGPT response completion using MutationObserver (event-driven, no polling)
 * 
 * Stable selector set from chrome-ai-bridge:
 * - stop: button[data-testid="stop-button"], button[aria-label*="Stop"]
 * - send: button[data-testid="send-button"], button[aria-label*="Send"]
 * - assistant: [data-message-author-role="assistant"]
 * - markdown: .markdown
 * - root: main, [role="main"]
 * 
 * @param {Page} page - Playwright page object
 * @param {number} timeoutMs - Max wait time (default: 5 minutes)
 * @returns {Promise<string>} - Last assistant message text
 */
async function waitForCompletion(page, timeoutMs = 300000) {
  return await page.evaluate(({ timeoutMs }) => {
    const SEL = {
      stop: [
        'button[data-testid="stop-button"]',
        'button[aria-label*="Stop"]',
        'button[aria-label*="Stop generating"]',
      ],
      send: [
        'button[data-testid="send-button"]',
        '#composer-submit-button',
        'button[aria-label*="Send"]',
      ],
      assistant: ['[data-message-author-role="assistant"]'],
      markdown: ['.markdown'],
      alert: ['[role="alert"]', '[data-testid="error-message"]'],
    };

    const qAny = (sels) => sels.map((s) => document.querySelector(s)).find(Boolean);
    const root = qAny(SEL.root || ['main', '[role="main"]']) || document.body;

    const getLastAssistantText = () => {
      const nodes = Array.from(root.querySelectorAll(SEL.assistant[0]));
      const last = nodes[nodes.length - 1];
      if (!last) return '';
      const md = last.querySelector(SEL.markdown[0]);
      return (md?.innerText || last.innerText || '').trim();
    };

    const isGenerating = () => Boolean(qAny(SEL.stop));
    const sendEnabled = () => {
      const btn = qAny(SEL.send);
      return btn ? !btn.disabled : true;
    };

    // Multi-indicator done: not generating AND send enabled
    const isDone = () => !isGenerating() && sendEnabled();

    let stableTicks = 0;
    let lastText = getLastAssistantText();

    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        obs.disconnect();
        reject(new Error(`Timeout after ${timeoutMs}ms waiting for completion`));
      }, timeoutMs);

      const obs = new MutationObserver(() => {
        // Check for error banners
        const err = qAny(SEL.alert);
        if (err) {
          clearTimeout(timer);
          obs.disconnect();
          reject(new Error(`ChatGPT error banner: ${err.textContent?.trim()}`));
          return;
        }

        // Track content changes
        const now = getLastAssistantText();
        if (now && now !== lastText) {
          lastText = now;
          stableTicks = 0;
        } else {
          stableTicks += 1;
        }

        // Require "done" + 3 consecutive stable ticks (content not changing)
        if (isDone() && stableTicks >= 3 && lastText) {
          clearTimeout(timer);
          obs.disconnect();
          resolve(lastText);
        }
      });

      obs.observe(root, {
        subtree: true,
        childList: true,
        characterData: true,
        attributes: true,
      });
    });
  }, { timeoutMs });
}

/**
 * Minimal send button watcher — resolves when button becomes enabled
 * (proven approach from GreasyFork ChatGPT userscripts)
 */
async function waitSendEnabled(page, timeoutMs = 30000) {
  return await page.evaluate(({ timeoutMs }) => {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        obs.disconnect();
        reject(new Error('Send button never re-enabled'));
      }, timeoutMs);

      const sendBtn = document.querySelector('button[data-testid="send-button"], button[aria-label*="Send"], #composer-submit-button');
      if (!sendBtn) { clearTimeout(timer); reject(new Error('Send button not found')); return; }

      const obs = new MutationObserver(() => {
        if (!sendBtn.disabled) {
          clearTimeout(timer);
          obs.disconnect();
          resolve(true);
        }
      });

      obs.observe(sendBtn, { attributes: true, attributeFilter: ['disabled'] });
    });
  }, { timeoutMs });
}

/**
 * Micro-extraction — get current page state in one evaluate call
 * Use this INSTEAD of full snapshots for reading response content
 */
async function getPageState(page) {
  return await page.evaluate(() => {
    const q = (sel) => document.querySelector(sel);
    const root = q('main') || q('[role="main"]') || document.body;
    
    const msgs = Array.from(root.querySelectorAll('[data-message-author-role="assistant"]'));
    const last = msgs[msgs.length - 1];
    const md = last?.querySelector?.('.markdown');
    
    return {
      generating: Boolean(q('button[data-testid="stop-button"]')),
      sendEnabled: q('button[data-testid="send-button"]') 
        ? !q('button[data-testid="send-button"]').disabled 
        : null,
      lastText: (md?.innerText || last?.innerText || '').trim(),
      msgCount: msgs.length,
      error: q('[role="alert"]')?.innerText?.trim() || null,
    };
  });
}

/**
 * DOM trimmer — keep only last N turns to prevent UI bloat in long tabs
 * Based on ChatGPT AutoCleaner pattern from Deep Research
 */
async function trimDom(page, keepTurns = 10) {
  return await page.evaluate((keep) => {
    const turns = Array.from(document.querySelectorAll('[data-testid^="conversation-turn-"]'));
    const extra = turns.length - keep;
    if (extra > 0) {
      for (let i = 0; i < extra; i++) turns[i].remove();
    }
    return { before: turns.length, after: Math.min(turns.length, keep), removed: Math.max(0, extra) };
  }, keepTurns);
}

// Export for use in other scripts
if (typeof module !== 'undefined') {
  module.exports = { waitForCompletion, waitSendEnabled, getPageState, trimDom };
}

// Standalone test
if (require.main === module) {
  (async () => {
    const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');
    const pages = browser.contexts()[0].pages();
    const page = pages.find(p => p.url().includes('chatgpt'));
    if (!page) { console.log('No ChatGPT page found'); process.exit(1); }
    
    console.log('Page state:', await getPageState(page));
    console.log('DOM trimmed:', await trimDom(page, 10));
    
    await browser.close();
  })();
}
