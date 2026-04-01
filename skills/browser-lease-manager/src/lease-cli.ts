// CLI runtime for browser-lease-manager
// openclaw lease list | show <id> | release <id> | break <id> | status | acquire

import {
  Lease,
  listLeases,
  getLease,
  releaseLease,
  retireLease,
  getActiveLease,
  getLeasesByOrigin,
  releaseAllByOrigin,
  createLease,
  resumeLease,
} from './lease-store.js';

function formatAge(ms: number): string {
  const s = Math.floor((Date.now() - ms) / 1000);
  if (s < 60) return `${s}s ago`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  return `${h}h ago`;
}

function formatLease(lease: Lease, verbose = false): string {
  const age = formatAge(lease.createdAt);
  const health = formatAge(lease.lastHealthAt);
  const stateColor = lease.state === 'active' ? '🟢' : lease.state === 'cooldown' ? '🟡' : '🔴';
  const failStr = lease.failureCount > 0 ? ` ⚠️ ${lease.failureCount}f` : '';

  if (!verbose) {
    return `${stateColor} ${lease.id.slice(0, 8)}  ${lease.origin}  ${lease.state}  (${health})  target=${lease.targetId.slice(0, 12)}`;
  }

  return [
    `  ID:       ${lease.id}`,
    `  Origin:   ${lease.origin}`,
    `  Account:  ${lease.account}`,
    `  Profile:  ${lease.profile}`,
    lease.proxyId ? `  Proxy:    ${lease.proxyId}` : null,
    `  Target:   ${lease.targetId}`,
    `  URL:      ${lease.tabUrl || '(empty)'}`,
    `  Created:  ${new Date(lease.createdAt).toISOString()} (${age})`,
    `  Healthy:  ${health}`,
    `  State:    ${stateColor} ${lease.state}${failStr}`,
    lease.cooldownUntil ? `  Cooldown: until ${new Date(lease.cooldownUntil).toISOString()}` : null,
    lease.metadata?.retiredReason ? `  Reason:   ${lease.metadata.retiredReason}` : null,
  ].filter(Boolean).join('\n');
}

export function registerLeaseCli(program: any) {
  const lease = program
    .command('lease')
    .description('Manage browser tab leases (hot-tab lifecycle, failure tracking)');

  // openclaw lease list
  lease
    .command('list')
    .description('List all browser leases')
    .option('--state <state>', 'Filter by state: active, cooldown, retired')
    .option('--verbose', 'Show full lease details')
    .action(async (opts: { state?: string; verbose?: boolean }) => {
      const leases = opts.state
        ? listLeases({ state: opts.state as Lease['state'] })
        : listLeases();

      if (leases.length === 0) {
        console.log('\n📭 No leases found.\n');
        return;
      }

      console.log(`\n🗂️  Browser Leases (${leases.length})\n`);
      for (const l of leases) {
        console.log(formatLease(l, opts.verbose));
      }
      console.log('');
    });

  // openclaw lease show <id>
  lease
    .command('show')
    .description('Show detailed info for a lease')
    .argument('<id>', 'Lease ID (or prefix)')
    .action(async (id: string) => {
      // Try exact match first, then prefix
      let l = getLease(id);
      if (!l) {
        const all = listLeases();
        l = all.find(lease => lease.id.startsWith(id)) ?? null;
      }

      if (!l) {
        console.log(`\n❌ Lease not found: ${id}\n`);
        return;
      }

      console.log(`\n${formatLease(l, true)}\n`);
    });

  // openclaw lease status
  lease
    .command('status')
    .description('Quick health summary of active leases')
    .action(async () => {
      const active = listLeases({ state: 'active' });
      const cooldown = listLeases({ state: 'cooldown' });
      const retired = listLeases({ state: 'retired' });

      console.log('\n🏥 Lease Health Summary\n');
      console.log(`  🟢 Active:   ${active.length}`);
      console.log(`  🟡 Cooldown: ${cooldown.length}`);
      console.log(`  🔴 Retired:  ${retired.length}`);

      if (active.length > 0) {
        console.log('\n  Active leases:\n');
        for (const l of active) {
          const failStr = l.failureCount > 0 ? ` ⚠️ ${l.failureCount} failures` : '';
          console.log(`    ${l.origin} (${l.account}) — ${l.tabUrl?.slice(0, 50) ?? '(no url)'}${failStr}`);
        }
      }

      if (cooldown.length > 0) {
        console.log('\n  Cooldown leases:\n');
        for (const l of cooldown) {
          const until = l.cooldownUntil ? new Date(l.cooldownUntil).toISOString() : '?';
          console.log(`    ${l.origin} — until ${until}`);
        }
      }

      console.log('');
    });

  // openclaw lease release <id>
  lease
    .command('release')
    .description('Release a lease cleanly (graceful close)')
    .argument('<id>', 'Lease ID (or prefix)')
    .action(async (id: string) => {
      let l = getLease(id);
      if (!l) {
        const all = listLeases();
        l = all.find(lease => lease.id.startsWith(id)) ?? null;
      }

      if (!l) {
        console.log(`\n❌ Lease not found: ${id}\n`);
        return;
      }

      releaseLease(l.id);
      console.log(`\n✅ Released lease: ${l.id} (${l.origin})\n`);
    });

  // openclaw lease break <id>
  lease
    .command('break')
    .description('Break a lease immediately (hard failure — no graceful close)')
    .argument('<id>', 'Lease ID (or prefix)')
    .option('--reason <reason>', 'Reason for breaking')
    .action(async (id: string, opts: { reason?: string }) => {
      let l = getLease(id);
      if (!l) {
        const all = listLeases();
        l = all.find(lease => lease.id.startsWith(id)) ?? null;
      }

      if (!l) {
        console.log(`\n❌ Lease not found: ${id}\n`);
        return;
      }

      retireLease(l.id, opts.reason ?? 'manual-break');
      console.log(`\n🔴 Broken lease: ${l.id} (${l.origin})\n`);
    });

  // openclaw lease acquire
  lease
    .command('acquire')
    .description('Acquire a new lease (opens a new browser tab)')
    .requiredOption('--origin <origin>', 'Site origin (e.g. chatgpt.com)')
    .option('--account <account>', 'Account name', 'primary')
    .option('--profile <profile>', 'Browser profile', 'openclaw')
    .option('--url <url>', 'Initial URL')
    .action(async (opts: { origin: string; account: string; profile: string; url?: string }) => {
      // Open a new browser tab for this origin
      // This requires the browser tool — we can't do it from CLI directly
      // Instead, we just create a pending lease and instruct the user
      const l = createLease({
        origin: opts.origin,
        account: opts.account,
        profile: opts.profile,
        targetId: '<pending — open tab manually>',
        tabUrl: opts.url,
      });
      console.log(`\n✅ Lease created (pending tab): ${l.id}`);
      console.log(`   Origin:  ${l.origin}`);
      console.log(`   Account: ${l.account}`);
      console.log(`   Profile: ${l.profile}`);
      console.log(`\n   To complete: open ${opts.url ?? `https://${opts.origin}`} in browser, then run:`);
      console.log(`   openclaw lease set-target ${l.id} --targetId <targetId>\n`);
    });

  // openclaw lease set-target <id>
  lease
    .command('set-target')
    .description('Set the targetId for a pending lease')
    .argument('<id>', 'Lease ID')
    .requiredOption('--targetId <targetId>', 'Browser tab targetId')
    .option('--url <url>', 'Current tab URL')
    .action(async (id: string, opts: { targetId: string; url?: string }) => {
      const l = getLease(id);
      if (!l) {
        console.log(`\n❌ Lease not found: ${id}\n`);
        return;
      }
      // We don't have an updateLease for targetId directly, use createLease to update
      // For now just report
      console.log(`\n⚠️  Set-target not implemented via CLI — update via plugin hook\n`);
      console.log(`   Lease ${id}: targetId = ${opts.targetId}\n`);
    });

  // openclaw lease release-origin <origin>
  lease
    .command('release-origin')
    .description('Release all leases for an origin')
    .argument('<origin>', 'Site origin (e.g. chatgpt.com)')
    .action(async (origin: string) => {
      const ids = releaseAllByOrigin(origin);
      if (ids.length === 0) {
        console.log(`\n📭 No active leases for: ${origin}\n`);
        return;
      }
      console.log(`\n✅ Released ${ids.length} lease(s) for: ${origin}\n`);
    });

  // openclaw lease resume <id>
  lease
    .command('resume')
    .description('Resume a lease from cooldown (if cooldown has elapsed)')
    .argument('<id>', 'Lease ID (or prefix)')
    .action(async (id: string) => {
      let l = getLease(id);
      if (!l) {
        const all = listLeases();
        l = all.find(lease => lease.id.startsWith(id)) ?? null;
      }

      if (!l) {
        console.log(`\n❌ Lease not found: ${id}\n`);
        return;
      }

      if (l.state !== 'cooldown') {
        console.log(`\n⚠️  Lease is not in cooldown: ${l.state}\n`);
        return;
      }

      const resumed = resumeLease(l.id);
      if (!resumed) {
        console.log(`\n⏳ Cooldown not yet elapsed for: ${l.id}\n`);
        return;
      }

      console.log(`\n✅ Resumed lease: ${l.id} (${l.origin})\n`);
    });
}
