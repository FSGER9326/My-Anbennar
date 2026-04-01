// lease-store.js — Pure JS reference implementation (no build step)
// Works in any Node.js context with CommonJS
// Based on: skills/browser-lease-manager/SKILL.md

const fs = require('fs');
const path = require('path');
const os = require('os');
const { homedir } = os;

const LEASE_FILE = path.join(homedir(), '.openclaw', 'state', 'browser-leases.json');

function ensureDir() {
  const dir = path.dirname(LEASE_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function loadIndex() {
  ensureDir();
  if (!fs.existsSync(LEASE_FILE)) {
    return { leases: {}, index: {} };
  }
  try {
    return JSON.parse(fs.readFileSync(LEASE_FILE, 'utf-8'));
  } catch {
    return { leases: {}, index: {} };
  }
}

function saveIndex(idx) {
  ensureDir();
  fs.writeFileSync(LEASE_FILE, JSON.stringify(idx, null, 2), 'utf-8');
}

function makeKey(origin, account, profile, proxyId) {
  return [origin, account, profile, proxyId ?? ''].join(':');
}

function generateId() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

/**
 * Create a new lease. Retires any existing active lease for the same key.
 * @param {{ origin: string, account: string, profile: string, proxyId?: string, targetId: string, tabUrl?: string, metadata?: object }} opts
 * @returns {Lease}
 */
function createLease(opts) {
  const idx = loadIndex();
  const key = makeKey(opts.origin, opts.account, opts.profile, opts.proxyId);
  const now = Date.now();

  const existingId = idx.index[key];
  if (existingId && idx.leases[existingId]) {
    idx.leases[existingId].state = 'retired';
  }

  const lease = {
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
    metadata: opts.metadata ?? {},
  };

  idx.leases[lease.id] = lease;
  idx.index[key] = lease.id;
  saveIndex(idx);
  return lease;
}

/** @param {string} id @returns {Lease|null} */
function getLease(id) {
  const idx = loadIndex();
  return idx.leases[id] ?? null;
}

/** @returns {Lease[]} */
function listLeases(filter) {
  const idx = loadIndex();
  const all = Object.values(idx.leases);
  if (!filter?.state) return all;
  return all.filter(l => l.state === filter.state);
}

/**
 * @param {string} id
 * @param {Partial<Lease>} patch
 * @returns {Lease|null}
 */
function updateLease(id, patch) {
  const idx = loadIndex();
  const lease = idx.leases[id];
  if (!lease) return null;
  Object.assign(lease, patch);
  if (patch.lastHealthAt === undefined) lease.lastHealthAt = Date.now();
  saveIndex(idx);
  return lease;
}

/** @returns {Lease|null} */
function retireLease(id, reason) {
  const idx = loadIndex();
  const lease = idx.leases[id];
  return updateLease(id, {
    state: 'retired',
    metadata: { ...(lease?.metadata ?? {}), retiredReason: reason },
  });
}

/** @returns {Lease|null} */
function cooldownLease(id, durationMs = 30000) {
  return updateLease(id, { state: 'cooldown', cooldownUntil: Date.now() + durationMs });
}

/** @returns {Lease|null} */
function resumeLease(id) {
  const idx = loadIndex();
  const lease = idx.leases[id];
  if (!lease) return null;
  if (lease.state !== 'cooldown') return lease;
  if (lease.cooldownUntil && Date.now() < lease.cooldownUntil) return null;
  return updateLease(id, { state: 'active', cooldownUntil: undefined });
}

/** @returns {Lease|null} */
function releaseLease(id) {
  return updateLease(id, { state: 'retired' });
}

/**
 * Record a failure. Auto-retires if failureCount >= 3.
 * @returns {{ lease: Lease|null, circuitOpen: boolean }}
 */
function recordFailure(id, failureClass) {
  const idx = loadIndex();
  const lease = idx.leases[id];
  if (!lease) return { lease: null, circuitOpen: false };

  const newCount = lease.failureCount + 1;
  const patch = {
    failureCount: newCount,
    lastHealthAt: Date.now(),
    metadata: {
      ...(lease.metadata ?? {}),
      lastFailureClass: failureClass,
      lastFailureAt: Date.now(),
    },
  };

  if (newCount >= 3) {
    patch.state = 'retired';
  }

  Object.assign(lease, patch);
  saveIndex(idx);
  return { lease, circuitOpen: newCount >= 3 };
}

/** @returns {Lease|null} */
function recordSuccess(id) {
  return updateLease(id, { failureCount: 0, lastHealthAt: Date.now() });
}

/** @returns {Lease[]} */
function getLeasesByOrigin(origin) {
  return listLeases().filter(l => l.origin === origin);
}

/** @returns {string[]} */
function releaseAllByOrigin(origin) {
  const leases = getLeasesByOrigin(origin).filter(l => l.state !== 'retired');
  for (const l of leases) releaseLease(l.id);
  return leases.map(l => l.id);
}

module.exports = {
  createLease,
  getLease,
  listLeases,
  updateLease,
  retireLease,
  cooldownLease,
  resumeLease,
  releaseLease,
  recordFailure,
  recordSuccess,
  getLeasesByOrigin,
  releaseAllByOrigin,
};
