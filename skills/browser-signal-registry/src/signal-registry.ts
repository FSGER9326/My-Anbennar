// Signal Registry — per-site completion signal definitions
// Source of truth for how to detect "done" on any given website

export type SignalType = 'network' | 'websocket' | 'dom' | 'predicate' | 'stable';

export interface NetworkSignal {
  type: 'network';
  /** URL pattern to match (url.includes()) */
  urlPattern: string;
  /** Expected HTTP status, e.g. 200 */
  status?: number;
  /** Timeout in ms (default: 60000) */
  timeout?: number;
}

export interface WebsocketSignal {
  type: 'websocket';
  /** Substring or pattern in frame payload */
  donePattern: string;
  /** Frame type that signals completion (default: 'close') */
  doneFrameType?: string;
}

export interface DomSignal {
  type: 'dom';
  /** CSS selector */
  selector: string;
  /** 'present' = element appears, 'hidden' = element disappears, 'enabled' = element enabled, 'disabled' = element disabled */
  state: 'present' | 'hidden' | 'enabled' | 'disabled';
  /** Timeout in ms (default: 30000) */
  timeout?: number;
}

export interface PredicateSignal {
  type: 'predicate';
  /** JS expression evaluated in page context. Return true when signal fires. */
  expression: string;
  /** Interval in ms for polling the expression (default: 2000) */
  interval?: number;
  /** Overall timeout in ms (default: 120000) */
  timeout?: number;
}

export interface StableSignal {
  type: 'stable';
  /** Milliseconds of no DOM mutations to consider stable (default: 1500) */
  duration?: number;
  /** Timeout in ms (default: 30000) */
  timeout?: number;
}

export type Signal =
  | NetworkSignal
  | WebsocketSignal
  | DomSignal
  | PredicateSignal
  | StableSignal;

// Per-site registry
export interface SiteSignals {
  /** Human-readable name */
  name: string;
  /** Homepage URL for reference */
  url: string;
  /** Completion signals — ALL must fire for completion */
  completionSignals: Signal[];
  /** Specific DOM micro-queries (falls back to generic) */
  microQueries?: {
    /** Selector for "still generating" indicator (e.g. stop button) */
    generatingIndicator?: string;
    /** Selector for "done, can regenerate" indicator */
    completeIndicator?: string;
    /** Selector for error state */
    errorSelector?: string;
    /** Selector for "can send next message" */
    canSendSelector?: string;
  };
  /** Known problematic selectors (avoid or handle carefully) */
  knownTraps?: string[];
}

export const SIGNAL_REGISTRY: Record<string, SiteSignals> = {

  'chatgpt.com': {
    name: 'ChatGPT',
    url: 'https://chatgpt.com',
    completionSignals: [
      {
        type: 'network',
        urlPattern: '/v1/chat/completions',
        status: 200,
        timeout: 90000,
      },
      {
        type: 'dom',
        selector: 'button[data-testid="stop-button"]',
        state: 'hidden',
        timeout: 120000,
      },
      {
        type: 'stable',
        duration: 1500,
        timeout: 30000,
      },
    ],
    microQueries: {
      generatingIndicator: 'button[data-testid="stop-button"]',
      completeIndicator: 'button[aria-label*="Regenerate"]',
      errorSelector: '[role="alert"], [data-testid="error-message"]',
      canSendSelector: 'button[data-testid="send-button"]',
    },
    knownTraps: [
      '[data-testid="stretching-anchor"]', // false-positive "generating" signal
    ],
  },

  'claude.ai': {
    name: 'Claude',
    url: 'https://claude.ai',
    completionSignals: [
      {
        type: 'network',
        urlPattern: '/api/chat/stream',
        timeout: 90000,
      },
      {
        type: 'dom',
        selector: '[data-testid="submit-button"]',
        state: 'enabled',
        timeout: 120000,
      },
      {
        type: 'stable',
        duration: 1500,
        timeout: 30000,
      },
    ],
    microQueries: {
      generatingIndicator: '[data-testid="thinking-indicator"]',
      completeIndicator: '[data-testid="submit-button"]:not([disabled])',
      errorSelector: '[role="alert"]',
      canSendSelector: '[data-testid="submit-button"]',
    },
  },

  'gemini.google.com': {
    name: 'Google Gemini',
    url: 'https://gemini.google.com',
    completionSignals: [
      {
        type: 'network',
        urlPattern: '/v1beta/models',
        status: 200,
        timeout: 60000,
      },
      {
        type: 'dom',
        selector: '[data-testid="thinking-indicator"]',
        state: 'hidden',
        timeout: 120000,
      },
      {
        type: 'stable',
        duration: 1500,
        timeout: 30000,
      },
    ],
    microQueries: {
      generatingIndicator: '[data-testid="thinking-indicator"]',
      completeIndicator: '[aria-label*="Regenerate"]',
      errorSelector: '[role="alert"]',
      canSendSelector: 'textarea[name="message"]',
    },
  },

  // Generic fallback for unknown sites
  '__generic__': {
    name: 'Generic HTTP App',
    url: '*',
    completionSignals: [
      {
        type: 'network',
        urlPattern: '',
        status: 200,
        timeout: 30000,
      },
      {
        type: 'stable',
        duration: 2000,
        timeout: 30000,
      },
    ],
  },
};

/**
 * Get signal config for a URL.
 * Falls back to __generic__ if no specific match.
 */
export function getSiteSignals(url: string): SiteSignals {
  for (const [domain, signals] of Object.entries(SIGNAL_REGISTRY)) {
    if (domain === '__generic__') continue;
    if (url.includes(domain)) {
      return signals;
    }
  }
  return SIGNAL_REGISTRY['__generic__'];
}

/**
 * Summarize a site's completion signals as a compact string.
 * Used for tool descriptions and prompts.
 */
export function summarizeSignals(site: SiteSignals): string {
  const parts = site.completionSignals.map(s => {
    switch (s.type) {
      case 'network': return `network(${s.urlPattern.split('/').pop() ?? '*'}, ${s.status ?? 'any'})`;
      case 'websocket': return `ws(${s.donePattern})`;
      case 'dom': return `dom(${s.state}:${s.selector.split('.').pop()?.split(']')[0] ?? '*'})`;
      case 'predicate': return `pred(${s.expression.slice(0, 30)}...)`;
      case 'stable': return `stable(${s.duration ?? 1500}ms)`;
    }
  });
  return parts.join(' + ');
}
