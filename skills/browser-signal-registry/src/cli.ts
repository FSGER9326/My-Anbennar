// CLI runtime for signal-registry
// Provides: openclaw signal list, openclaw signal show <site>

import { SIGNAL_REGISTRY, getSiteSignals, summarizeSignals } from './signal-registry.js';

export function registerSignalCli(program: any) {
  const signal = program
    .command('signal')
    .description('Query the browser completion signal registry');

  signal
    .command('list')
    .description('List all registered sites and their completion signals')
    .action(async () => {
      const entries = Object.entries(SIGNAL_REGISTRY)
        .filter(([k]) => k !== '__generic__');

      console.log('\n🗺️  Signal Registry — Registered Sites\n');
      for (const [domain, site] of entries) {
        const summary = summarizeSignals(site);
        console.log(`  ${domain.padEnd(25)} ${site.name}`);
        console.log(`    → ${summary}\n`);
      }
      console.log(`  __generic__                  Generic HTTP App (fallback)`);
      console.log(`    → network(200) + stable(2000ms)\n`);
    });

  signal
    .command('show')
    .description('Show completion signals for a site')
    .argument('<site>', 'Site domain (e.g. chatgpt.com) or URL')
    .action(async (site: string) => {
      const signals = getSiteSignals(site.startsWith('http') ? site : site);
      console.log(`\n🗺️  Signals for: ${signals.name} (${site})\n`);
      console.log(`  URL: ${signals.url}\n`);

      for (const sig of signals.completionSignals) {
        if (sig.type === 'network') {
          console.log(`  📡 network`);
          console.log(`     URL pattern: ${sig.urlPattern}`);
          console.log(`     Status: ${sig.status ?? 'any'}`);
          console.log(`     Timeout: ${sig.timeout ?? 60000}ms`);
        } else if (sig.type === 'websocket') {
          console.log(`  🔌 websocket`);
          console.log(`     Done pattern: ${sig.donePattern}`);
          console.log(`     Done frame type: ${sig.doneFrameType ?? 'close'}`);
        } else if (sig.type === 'dom') {
          console.log(`  🖥️  dom`);
          console.log(`     Selector: ${sig.selector}`);
          console.log(`     State: ${sig.state}`);
          console.log(`     Timeout: ${sig.timeout ?? 30000}ms`);
        } else if (sig.type === 'predicate') {
          console.log(`  ⚙️  predicate`);
          console.log(`     Expression: ${sig.expression}`);
          console.log(`     Interval: ${sig.interval ?? 2000}ms`);
          console.log(`     Timeout: ${sig.timeout ?? 120000}ms`);
        } else if (sig.type === 'stable') {
          console.log(`  ⏸️  stable`);
          console.log(`     Duration: ${sig.duration ?? 1500}ms`);
          console.log(`     Timeout: ${sig.timeout ?? 30000}ms`);
        }
        console.log('');
      }

      if (signals.microQueries) {
        console.log('  🔍 Micro-queries:');
        const mq = signals.microQueries;
        if (mq.generatingIndicator) console.log(`    generating: ${mq.generatingIndicator}`);
        if (mq.completeIndicator) console.log(`    complete: ${mq.completeIndicator}`);
        if (mq.errorSelector) console.log(`    error: ${mq.errorSelector}`);
        if (mq.canSendSelector) console.log(`    canSend: ${mq.canSendSelector}`);
        console.log('');
      }

      if (signals.knownTraps?.length) {
        console.log('  ⚠️  Known traps:');
        for (const t of signals.knownTraps) {
          console.log(`    ${t}`);
        }
        console.log('');
      }
    });

  signal
    .command('check')
    .description('Check if a URL matches any registered site')
    .argument('<url>', 'URL to check')
    .action(async (url: string) => {
      const signals = getSiteSignals(url);
      if (signals.name === 'Generic HTTP App') {
        console.log(`\n⚠️  No specific signal registry for: ${url}`);
        console.log('    Using generic fallback.\n');
      } else {
        console.log(`\n✅ Matched: ${signals.name}`);
        console.log(`   Pattern: ${summarizeSignals(signals)}\n`);
      }
    });
}
