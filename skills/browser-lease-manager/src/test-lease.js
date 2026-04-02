// test-lease.js — Smoke test for lease-store.js
// Run: node test-lease.js

const store = require('./lease-store.js');

const TEST_ORIGIN = 'chatgpt.com';
const TEST_ACCOUNT = 'test-user';
const TEST_PROFILE = 'openclaw';

function log(label, val) {
  console.log(`[TEST] ${label}:`, JSON.stringify(val, null, 2));
}

function assert(condition, msg) {
  if (!condition) {
    console.error(`❌ FAIL: ${msg}`);
    process.exit(1);
  }
  console.log(`✅ PASS: ${msg}`);
}

async function run() {
  console.log('\n=== Lease Store Smoke Tests ===\n');

  // 1. Create a lease
  const lease = store.createLease({
    origin: TEST_ORIGIN,
    account: TEST_ACCOUNT,
    profile: TEST_PROFILE,
    targetId: 'CDPSession-test-001',
    tabUrl: 'https://chatgpt.com/c/test',
  });
  log('createLease', { id: lease.id.slice(0, 8), origin: lease.origin, state: lease.state });
  assert(lease.state === 'active', 'New lease is active');
  assert(lease.failureCount === 0, 'New lease has 0 failures');
  assert(lease.origin === TEST_ORIGIN, 'Origin matches');

  // 2. Get the lease by ID
  const found = store.getLease(lease.id);
  assert(found !== null, 'getLease returns the lease');
  assert(found.id === lease.id, 'getLease returns correct lease');

  // 3. List all leases
  const all = store.listLeases();
  assert(all.length >= 1, 'listLeases returns at least 1 lease');
  assert(all.some(l => l.id === lease.id), 'listLeases includes our lease');

  // 4. List only active leases
  const active = store.listLeases({ state: 'active' });
  assert(active.some(l => l.id === lease.id), 'Active filter includes our lease');

  // 5. Record a failure (circuit not open yet)
  const { lease: afterFail1, circuitOpen: circ1 } = store.recordFailure(lease.id, 'soft_429');
  assert(circ1 === false, '1st failure: circuit not open');
  assert(afterFail1.failureCount === 1, 'failureCount = 1');
  assert(afterFail1.metadata.lastFailureClass === 'soft_429', 'Failure class recorded');

  // 6. Record a second failure (still not circuit break)
  const { circuitOpen: circ2 } = store.recordFailure(lease.id, 'soft_429');
  assert(circ2 === false, '2nd failure: circuit not open yet');
  assert(store.getLease(lease.id).failureCount === 2, 'failureCount = 2');

  // 7. Third failure → circuit break
  const { circuitOpen: circ3, lease: brokenLease } = store.recordFailure(lease.id, 'hard_block');
  assert(circ3 === true, '3rd failure: circuit OPEN');
  assert(brokenLease.state === 'retired', 'Lease is retired after circuit break');

  // 8. Retire doesn't change failure count on already retired
  store.retireLease(lease.id, 'test');
  const afterRetire = store.getLease(lease.id);
  assert(afterRetire.state === 'retired', 'Still retired after retireLease');

  // 9. Release by origin
  const lease2 = store.createLease({
    origin: 'claude.ai',
    account: TEST_ACCOUNT,
    profile: TEST_PROFILE,
    targetId: 'CDPSession-test-002',
    tabUrl: 'https://claude.ai/c/test',
  });
  assert(lease2.state === 'active', 'Second lease is active');

  const released = store.releaseAllByOrigin('claude.ai');
  assert(released.length === 1, 'releaseAllByOrigin returns released IDs');
  assert(store.getLease(lease2.id).state === 'retired', 'claude.ai lease is retired');

  // 10. Cooldown and resume
  const cooldownLease = store.createLease({
    origin: 'gemini.google.com',
    account: TEST_ACCOUNT,
    profile: TEST_PROFILE,
    targetId: 'CDPSession-test-003',
  });
  store.cooldownLease(cooldownLease.id, 1000); // 1 second cooldown
  assert(store.getLease(cooldownLease.id).state === 'cooldown', 'Lease is in cooldown');

  // Can't resume yet (cooldown hasn't elapsed)
  const tooEarly = store.resumeLease(cooldownLease.id);
  assert(tooEarly === null, 'Cannot resume before cooldown elapsed');

  // Wait for cooldown
  await new Promise(r => setTimeout(r, 1100));
  const resumed = store.resumeLease(cooldownLease.id);
  assert(resumed !== null, 'Resume works after cooldown elapsed');
  assert(resumed.state === 'active', 'Resumed lease is active again');

  // 11. Success resets failure count
  const successLease = store.createLease({
    origin: 'perplexity.ai',
    account: TEST_ACCOUNT,
    profile: TEST_PROFILE,
    targetId: 'CDPSession-test-004',
  });
  store.recordFailure(successLease.id, 'soft_429');
  store.recordFailure(successLease.id, 'stale_ref');
  assert(store.getLease(successLease.id).failureCount === 2, 'Two failures recorded');

  store.recordSuccess(successLease.id);
  assert(store.getLease(successLease.id).failureCount === 0, 'Success resets failureCount to 0');

  // Cleanup
  const cleanedUp = store.releaseAllByOrigin(TEST_ORIGIN);
  console.log(`\n🧹 Cleaned up ${cleanedUp.length} test lease(s) for ${TEST_ORIGIN}`);

  console.log('\n=== All Tests Passed ===\n');
}

run().catch(err => {
  console.error('❌ Test error:', err);
  process.exit(1);
});
