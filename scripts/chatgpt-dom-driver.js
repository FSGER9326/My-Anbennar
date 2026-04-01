/**
 * ChatGPT DOM Driver — Micro-query functions for ChatGPT web UI
 * 
 * Replaces full-page snapshots with targeted JS evaluation calls.
 * Each function returns structured data instead of requiring a full DOM parse.
 * 
 * Usage via OpenClaw browser tool:
 *   browser act kind=evaluate fn={() => { ... }}
 * 
 * Stable selectors grounded in real ChatGPT automation implementations:
 * - [data-message-author-role="assistant"] — assistant messages
 * - .markdown — response content container
 * - button[data-testid="stop-button"] — generating indicator
 * - button[data-testid="send-button"] — send button
 * - textarea#prompt-textarea — input field
 * - button[aria-label*="Regenerate"] — completion indicator
 * - [data-testid^="conversation-turn-"] — conversation turns
 * - [role="alert"], [data-testid="error-message"] — error banners
 */

// ── Minimum Viable DOM Selector Set ──
// From chrome-ai-bridge (proven stable across ChatGPT UI changes):
// - root: main / [role="main"]
// - composer: #prompt-textarea / textarea[data-testid="prompt-textarea"]
// - send: button[data-testid="send-button"]
// - stop: button[data-testid="stop-button"]
// - assistant: [data-message-author-role="assistant"]
// - markdown: .markdown

// ── State queries ──

/** Check if ChatGPT is still generating a response */
function isGenerating() {
  const stopBtn = 
    document.querySelector('button[data-testid="stop-button"]') ||
    document.querySelector('button[aria-label*="Stop"]') ||
    document.querySelector('button[aria-label*="Stop generating"]');
  return Boolean(stopBtn);
}

/** Check if response is complete (Regenerate button visible) */
function isComplete() {
  const regenBtn = 
    document.querySelector('button[aria-label*="Regenerate"]') ||
    document.querySelector('button[data-testid="regenerate-button"]');
  return Boolean(regenBtn);
}

/** Check for error state */
function getError() {
  const err = document.querySelector('[role="alert"]') ||
              document.querySelector('[data-testid="error-message"]');
  return err ? err.innerText.trim() : null;
}

/** Check if send button is enabled (input ready) */
function canSend() {
  const btn = document.querySelector('button[data-testid="send-button"]');
  return btn ? !btn.disabled : false;
}

// ── Content extraction ──

/** Get last assistant message text (cleaned markdown) */
function getLastAssistantText() {
  const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
  const last = msgs[msgs.length - 1];
  if (!last) return '';
  const md = last.querySelector('.markdown');
  return (md || last).innerText.trim();
}

/** Get last assistant message as HTML */
function getLastAssistantHTML() {
  const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
  const last = msgs[msgs.length - 1];
  if (!last) return '';
  const md = last.querySelector('.markdown');
  return (md || last).innerHTML;
}

/** Get all assistant messages as array */
function getAllAssistantTexts() {
  const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
  return Array.from(msgs).map(m => {
    const md = m.querySelector('.markdown');
    return (md || m).innerText.trim();
  });
}

/** Get current user input text */
function getInputText() {
  const ta = document.querySelector('textarea#prompt-textarea');
  return ta ? ta.value : '';
}

/** Get conversation turn count */
function getTurnCount() {
  const turns = document.querySelectorAll('[data-testid^="conversation-turn-"]');
  return turns.length;
}

// ── UI state ──

/** Get comprehensive UI state in one call */
function getUIState() {
  return {
    generating: isGenerating(),
    complete: isComplete(),
    canSend: canSend(),
    error: getError(),
    turnCount: getTurnCount(),
    inputLength: (document.querySelector('textarea#prompt-textarea')?.value || '').length,
    assistantCount: document.querySelectorAll('[data-message-author-role="assistant"]').length
  };
}

// ── Actions (use with evaluate) ──

/** Set input text (does NOT send) */
function setInput(text) {
  const ta = document.querySelector('textarea#prompt-textarea');
  if (!ta) return false;
  // React needs synthetic event for state update
  const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
  nativeInputValueSetter.call(ta, text);
  ta.dispatchEvent(new Event('input', { bubbles: true }));
  return true;
}

/** Click send button */
function clickSend() {
  const btn = document.querySelector('button[data-testid="send-button"]');
  if (btn && !btn.disabled) { btn.click(); return true; }
  return false;
}

/** Set input and send */
function sendMessage(text) {
  return setInput(text) && clickSend();
}

/** Click regenerate button */
function clickRegenerate() {
  const btn = document.querySelector('button[aria-label*="Regenerate"]');
  if (btn) { btn.click(); return true; }
  return false;
}

/** Get conversation turn count (for DOM trimming) */
function getTurnCount() {
  const turns = document.querySelectorAll('[data-testid^="conversation-turn-"]');
  return turns.length;
}

/** Trim old conversation turns from DOM (prevent UI bloat) — keep only last N */
function trimDom(keepTurns = 10) {
  const turns = Array.from(document.querySelectorAll('[data-testid^="conversation-turn-"]'));
  const extra = turns.length - keepTurns;
  if (extra > 0) {
    for (let i = 0; i < extra; i++) turns[i].remove();
  }
  return { before: turns.length, after: Math.min(turns.length, keepTurns), removed: Math.max(0, extra) };
}

/** Get last assistant message as structured object */
function getLastAssistantStructured() {
  const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
  const last = msgs[msgs.length - 1];
  if (!last) return null;
  const md = last.querySelector('.markdown');
  return {
    text: (md || last).innerText.trim(),
    html: (md || last).innerHTML,
    msgIndex: msgs.length
  };
}

// Export for Node.js (Playwright sidecar usage)
if (typeof module !== 'undefined') {
  module.exports = {
    isGenerating, isComplete, getError, canSend,
    getLastAssistantText, getLastAssistantHTML, getAllAssistantTexts,
    getInputText, getTurnCount, getUIState,
    setInput, clickSend, sendMessage, clickRegenerate,
    trimDom, getLastAssistantStructured
  };
}
