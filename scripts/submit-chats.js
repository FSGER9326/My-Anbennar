const { chromium } = require('C:\\Users\\User\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\playwright-core');
const fs = require('fs');

const projectUrl = 'https://chatgpt.com/g/g-p-69cce3fc61e08191aa7d0f48ee2487ef-openclaw/project';

const prompts = [
  {
    name: 'Browser Bridge Deep Research v2',
    prompt: `I already did one Deep Research on "AI Agent Browser Bridge Improvements" and implemented: chatgpt-dom-driver.js (17 DOM micro-query functions using stable selectors like data-message-author-role, data-testid), a Playwright sidecar script (CDP + frameLocator for cross-origin iframe downloads), Core Memory (Letta-style blocks), and Session Handoff (ReSum-style).

Now I want to go deeper on browser automation reliability and speed. What are the BEST practices from production agent systems?

1) How do other AI agents (LangChain, CrewAI, AutoGPT, or OpenClaw users) handle browser automation reliably? What patterns reduce fragility?
2) What selector strategies have the lowest breakage rate for React SPAs like ChatGPT? ARIA roles? data-testid? Shadow DOM piercing? MutationObserver-based?
3) How do production systems detect "response complete" without polling? Event-driven patterns? MutationObserver? WebSocket hooks?
4) Optimal way to parallelize browser tasks — tab pooling, leasing, session state management?
5) MCP servers or browser automation tools that work WITH OpenClaw (not replace it) to offload browser work?
6) ChatGPT rate limit handling: detection, backoff strategies, rotation?
7) Page load optimization — can we pre-load ChatGPT and keep it warm? Service workers? Persistent browser profiles?

Find real code examples, GitHub repos, blog posts, and papers from people who've solved these. Focus on practical, implementable solutions that cost $0 extra.`,
    deepResearch: true,
    extendedThinking: false,
    waitMs: 900000
  },
  {
    name: 'Self-Optimization Extended Thinking',
    prompt: `I am Jordan, an AI agent running on OpenClaw. I have the same base model (GPT-4o class) throughout — I cannot switch to a better model. My job is to optimize MYSELF: increase efficiency, speed, and capability within my current model constraints.

Current architecture:
- OpenClaw platform on Windows (7.4GB RAM)
- Playwright-core 1.58.2 via CDP for browser automation
- Subagent system: spawn isolated sessions for parallel work
- Memory: Core Memory (CORE_MEMORY.md), Session Handoff, daily files, Obsidian vault, OpenViking KG
- Tools: browser tool (refs-based), exec, file read/write, web search
- ChatGPT bridge: Playwright sidecar script connects via CDP to use Deep Research, Extended Thinking

Current bottlenecks:
1. Each subagent spawn has cold-start overhead (reads ~5 context files from scratch)
2. Context windows get large → compaction loses information → agent starts blank
3. Subagent learning loop is manual — I have a Timeout Tuning Table but I manually apply it
4. Browser interactions take 15-30s per exchange (navigate → snapshot → parse → act)
5. No automatic quality feedback — I manually evaluate 10 dimensions after each subagent

Given these CONSTRAINTS (same model, no API cost increase, Windows 7.4GB RAM), optimize my efficiency:

1. CONTEXT COMPRESSION: How can I make each subagent session start faster? What's the minimum viable context? I currently load MEMORY.md + CORE_MEMORY.md + SESSION_HANDOFF.md + daily file. Can any of these be merged, condensed, or made optional based on task type?

2. PARALLEL OPTIMIZATION: I spawn subagents but don't truly parallelize. What's the optimal spawn strategy? When should I run serial vs parallel? How do I avoid token contention?

3. SELF-MODIFICATION: What can I modify about myself (prompts, parameters, spawn patterns) that doesn't require a model upgrade? What are the highest-leverage self-modifications for a fixed-model agent?

4. WORKFLOW AUTOMATION: What workflows should be fully automated (cron) vs on-demand vs manual? How do I build automatic quality gates that don't require human review?

Think deeply about each area. Propose specific, actionable changes I can implement this week with no extra cost. Include before/after metrics where possible.`,
    deepResearch: false,
    extendedThinking: true,
    waitMs: 300000
  }
];

async function submitChat(context, promptData, index) {
  console.log(`\n=== Submitting Chat ${index + 1}: ${promptData.name} ===`);
  const page = await context.newPage();
  
  // Navigate to project to get a new chat
  await page.goto(projectUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(5000);
  
  // Navigate directly — simple URL, not project URL (which is too heavy)
  await page.goto('https://chatgpt.com/', { waitUntil: 'load', timeout: 30000 });
  await page.waitForTimeout(8000);
  console.log('ChatGPT loaded');
  
  // Fill prompt — ChatGPT uses ProseMirror contenteditable, not a regular textarea
  // The visible input is a div[contenteditable="true"] inside #prompt-textarea
  const inputSelector = 'div[contenteditable="true"][id*="prompt"], div[contenteditable="true"][data-testid*="prompt"], div.ProseMirror';
  await page.waitForSelector(inputSelector, { timeout: 15000, state: 'visible' });
  await page.evaluate((text) => {
    const el = document.querySelector('div[contenteditable="true"][id*="prompt"]') || 
               document.querySelector('div[contenteditable="true"]') ||
               document.querySelector('.ProseMirror');
    if (!el) throw new Error('No contenteditable found');
    el.focus();
    // Set inner text
    el.textContent = text;
    // Dispatch input event for React
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }, promptData.prompt);
  console.log('Prompt filled');
  await page.waitForTimeout(500);
  
  // Enable Deep Research if requested
  if (promptData.deepResearch) {
    console.log('Enabling Deep Research...');
    // Look for any button/link with "deep research" text in the composer area
    const drBtns = await page.$$('button, [role="button"]');
    for (const btn of drBtns) {
      const text = await btn.textContent().catch(() => '');
      if (text.toLowerCase().includes('deep research')) {
        console.log('Found DR button:', text.trim().substring(0, 50));
        if (!text.includes('remove')) {
          await btn.click();
          await page.waitForTimeout(1000);
          console.log('Deep Research enabled');
        } else {
          console.log('Deep Research already enabled');
        }
        break;
      }
    }
  }
  
  // Enable Extended Thinking if requested
  if (promptData.extendedThinking) {
    console.log('Enabling Extended Thinking...');
    const etBtns = await page.$$('button, [role="button"]');
    for (const btn of etBtns) {
      const text = await btn.textContent().catch(() => '');
      if (text.toLowerCase().includes('extended thinking')) {
        console.log('Found ET button:', text.trim().substring(0, 50));
        if (!text.includes('remove')) {
          await btn.click();
          await page.waitForTimeout(1000);
          console.log('Extended Thinking enabled');
        } else {
          console.log('Extended Thinking already enabled');
        }
        break;
      }
    }
  }
  
  // Send
  console.log('Sending prompt...');
  await page.waitForTimeout(500);
  // Try multiple send button selectors
  const sendBtn = page.locator('button[data-testid="send-button"], button[aria-label*="Send"], button[aria-label*="send"]');
  const sendCount = await sendBtn.count();
  console.log(`Found ${sendCount} send buttons`);
  if (sendCount > 0) {
    await sendBtn.first().click();
  } else {
    // Fallback: press Enter
    await page.keyboard.press('Enter');
  }
  console.log(`Chat ${index + 1} sent! Waiting for response...`);
  
  // Wait for response complete
  try {
    await page.waitForSelector('button[aria-label*="Regenerate"], button[data-testid="regenerate-button"]', { timeout: promptData.waitMs });
    console.log(`Chat ${index + 1}: Response complete!`);
  } catch (e) {
    console.log(`Chat ${index + 1}: Timeout after ${promptData.waitMs/1000}s — response may still be generating`);
  }
  
  // Extract response
  const lastText = await page.evaluate(() => {
    const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
    const last = msgs[msgs.length - 1];
    if (!last) return '';
    const md = last.querySelector('.markdown');
    return (md || last).innerText;
  });
  
  // Save response
  const outputPath = `C:\\Users\\User\\Downloads\\deep-research-v2-${index + 1}.md`;
  fs.writeFileSync(outputPath, `# ${promptData.name}\n\n${lastText}`);
  console.log(`Chat ${index + 1}: Saved ${lastText.length} chars to ${outputPath}`);
  
  // Get the chat URL for future reference
  const chatUrl = page.url();
  console.log(`Chat ${index + 1}: URL = ${chatUrl}`);
  
  await page.close();
  return { url: chatUrl, outputPath, length: lastText.length };
}

async function main() {
  console.log('Connecting to browser...');
  const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');
  const context = browser.contexts()[0];
  
  const results = [];
  for (let i = 0; i < prompts.length; i++) {
    const result = await submitChat(context, prompts[i], i);
    results.push(result);
  }
  
  console.log('\n=== ALL CHATS SUBMITTED ===');
  results.forEach((r, i) => {
    console.log(`Chat ${i+1}: ${r.url}`);
    console.log(`  Output: ${r.outputPath} (${r.length} chars)`);
  });
  
  // Don't close browser — it's shared with OpenClaw
  await browser.close();
}

main().catch(e => {
  console.error('Fatal:', e.message);
  process.exit(1);
});
