// Lease Store — CRUD + persistence for browser leases
// File: ~/.openclaw/state/browser-leases.json

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

export interface Lease {
  id: string;
  origin: string;
  account: string;
  profile: string;
  proxyId?: string;
  targetId: string;
  tabUrl: string;
  createdAt: number;
  lastHealthAt: number;
  failureCount: number;
  state: 'active' | 'cooldown' | 'retired';
  cooldownUntil?: number;
  metadata?: Record<string, unknown>;
}

export interface LeaseIndex {
  leases: Record<string, Lease>;
  // Fast lookup: origin:account:profile → leaseId
  index: Record<string, string>;
}

const LEASE_FILE = path.join(os.homedir(), '.openclaw', 'state', 'browser-leases.json');

function ensureDir(): void {
  const dir = path.dirname(LEASE_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function loadIndex(): LeaseIndex {
  ensureDir();
  if (!fs.existsSync(LEASE_FILE)) {
    return { leases: {}, index: {} };
  }
  try {
    return JSON.parse(fs.readFileSync(LEASE_FILE, 'utf-8')) as LeaseIndex;
  } catch {
    return { leases: {}, index: {} };
  }
}

function saveIndex(idx: LeaseIndex): void {
  ensureDir();
  fs.writeFileSync(LEASE_FILE, JSON.stringify(idx, null, 2), 'utf-8');
}

function makeKey(origin: string, account: string, profile: string, proxyId?: string): string {
  return [origin, account, profile, proxyId ?? ''].join(':');
}

function generateId(): string {
  // Simple UUID v4-ish
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

// ─── CRUD ────────────────────────────────────────────────────────────────────

/**
 * Create a new lease. Replaces any existing active lease for the same key.
 */
export function createLease(opts: {
  origin: string;
  account: string;
  profile: string;
  proxyId?: string;
  targetId: string;
  tabUrl?: string;
  metadata?: Record<string, unknown>;
}): Lease {
  const idx = loadIndex();
  const key = makeKey(opts.origin, opts.account, opts.profile, opts.proxyId);
  const now = Date.now();

  // Retire existing active lease for this key
  const existingId = idx.index[key];
  if (existingId && idx.leases[existingId]) {
    idx.leases[existingId].state = 'retired';
  }

  const lease: Lease = {
    id: generateId(),
    origin: opts.origin,
    account: opts.account,
    profile: opts.profile,
    proxyId: opts.proxyId,
    targetId: opts.targetId,
    tabUrl: opts.tabUrl ?? '',
    createdAt: now,
    lastHealthAt: now,
    failureCount: 0,
    state: 'active',
    metadata: opts.metadata,
  };

  idx.leases[lease.id] = lease;
  idx.index[key] = lease.id;
  saveIndex(idx);
  return lease;
}

/**
 * Get a lease by ID.
 */
export function getLease(id: string): Lease | null {
  const idx = loadIndex();
  return idx.leases[id] ?? null;
}

/**
 * Get active lease for a given origin+account+profile.
 */
export function getActiveLease(
  origin: string,
  account: string,
  profile: string,
  proxyId?: string
): Lease | null {
  const idx = loadIndex();
  const key = makeKey(origin, account, profile, proxyId);
  const id = idx.index[key];
  if (!id) return null;
  const lease = idx.leases[id];
  if (!lease || lease.state === 'retired') return null;
  return lease;
}

/**
 * List all leases (optionally filtered by state).
 */
export function listLeases(filter?: { state?: Lease['state'] }): Lease[] {
  const idx = loadIndex();
  const all = Object.values(idx.leases);
  if (!filter?.state) return all;
  return all.filter(l => l.state === filter.state);
}

/**
 * Update lease fields.
 */
export function updateLease(id: string, patch: Partial<Pick<Lease, 'targetId' | 'tabUrl' | 'lastHealthAt' | 'failureCount' | 'state' | 'cooldownUntil' | 'metadata'>>): Lease | null {
  const idx = loadIndex();
  const lease = idx.leases[id];
  if (!lease) return null;
  Object.assign(lease, patch);
  if (patch.lastHealthAt === undefined) {
    lease.lastHealthAt = Date.now();
  }
  saveIndex(idx);
  return lease;
}

/**
 * Retire a lease immediately (hard failure).
 */
export function retireLease(id: string, reason?: string): Lease | null {
  return updateLease(id, { state: 'retired', metadata: { ...loadIndex().leases[id]?.metadata, retiredReason: reason } });
}

/**
 * Put a lease into cooldown (transient failure).
 */
export function cooldownLease(id: string, durationMs: number = 30000): Lease | null {
  const until = Date.now() + durationMs;
  return updateLease(id, { state: 'cooldown', cooldownUntil: until });
}

/**
 * Resume a lease from cooldown (if cooldown has elapsed).
 */
export function resumeLease(id: string): Lease | null {
  const idx = loadIndex();
  const lease = idx.leases[id];
  if (!lease) return null;
  if (lease.state !== 'cooldown') return lease;
  if (lease.cooldownUntil && Date.now() < lease.cooldownUntil) {
    return null; // Still in cooldown
  }
  return updateLease(id, { state: 'active', cooldownUntil: undefined });
}

/**
 * Release a lease cleanly (graceful close).
 */
export function releaseLease(id: string): Lease | null {
  return updateLease(id, { state: 'retired' });
}

/**
 * Record a failure on a lease (increments failureCount).
 * If failureCount >= 3, auto-retires and returns { retired: true }.
 */
export function recordFailure(id: string, failureClass: string): { lease: Lease | null; circuitOpen: boolean } {
  const idx = loadIndex();
  const lease = idx.leases[id];
  if (!lease) return { lease: null, circuitOpen: false };

  const newCount = lease.failureCount + 1;
  const patch: Partial<Lease> = {
    failureCount: newCount,
    lastHealthAt: Date.now(),
    metadata: { ...lease.metadata, lastFailureClass: failureClass, lastFailureAt: Date.now() },
  };

  let circuitOpen = false;
  if (newCount >= 3) {
    patch.state = 'retired';
    circuitOpen = true;
  }

  Object.assign(lease, patch);
  saveIndex(idx);
  return { lease, circuitOpen };
}

/**
 * Record success on a lease (resets failure count).
 */
export function recordSuccess(id: string): Lease | null {
  return updateLease(id, { failureCount: 0, lastHealthAt: Date.now() });
}

/**
 * Get all leases for an origin.
 */
export function getLeasesByOrigin(origin: string): Lease[] {
  return listLeases().filter(l => l.origin === origin);
}

/**
 * Release all active leases for an origin.
 */
export function releaseAllByOrigin(origin: string): string[] {
  const leases = getLeasesByOrigin(origin).filter(l => l.state !== 'retired');
  const ids: string[] = [];
  for (const l of leases) {
    releaseLease(l.id);
    ids.push(l.id);
  }
  return ids;
}
