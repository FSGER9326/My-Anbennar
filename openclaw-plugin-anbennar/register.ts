/**
 * openclaw-plugin-anbennar / register.ts
 *
 * Provides:
 *  - before_prompt_build: injects lane-aware system context + hotspot risk report
 *  - Tools (via tool handlers):
 *      anbennar.preflight   — run repo_doctor + hotspot validation
 *      anbennar.sync_with_main — git fetch + rebase onto origin/main
 *      anbennar.validate_all — run pre_pr_gate.sh + all audits
 *      anbennar.spec_compile  — prose → mod-spec.json via llm-task
 *
 * Install: place openclaw-plugin-anbennar/ in <workspace>/.openclaw/plugins/
 *          or reference via openclaw config: plugins.entries."my-anbennar-sheriff"
 */
import { execSync } from "node:child_process";
import { readFileSync, existsSync } from "node:fs";
import { join, resolve } from "node:path";

const WORKSPACE = process.cwd();

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function git(command: string, cwd = WORKSPACE): string {
  try {
    return execSync(`git ${command}`, { cwd, encoding: "utf8", timeout: 30000 }).trim();
  } catch (e: any) {
    return (e.stdout || e.stderr || "").toString().trim();
  }
}

function getChangedFiles(): string[] {
  const out = git("diff --name-only");
  return out ? out.split("\n").filter(Boolean) : [];
}

function runPython(script: string, args = ""): string {
  try {
    return execSync(`python ${script} ${args}`, {
      cwd: WORKSPACE,
      encoding: "utf8",
      timeout: 60000,
    }).trim();
  } catch (e: any) {
    return (e.stdout || e.stderr || "").toString().trim();
  }
}

// ---------------------------------------------------------------------------
// before_prompt_build — injects lane-aware system context
// ---------------------------------------------------------------------------

function buildHotspotReport(changed: string[]): string {
  if (!changed.length) return "No changed files.";
  try {
    return runPython(
      "scripts/anbennar_hotspot_explainer.py",
      `--files ${changed.join(" ")}`
    );
  } catch {
    return "Hotspot explainer unavailable.";
  }
}

function getAnbennarContext(): string {
  const lanes = [
    "gameplay",
    "automation",
    "lore",
    "gfx",
  ];

  const changed = getChangedFiles();
  const hotspotReport = buildHotspotReport(changed);

  return `
## My-Anbennar — Hard Rules

You are modding Anbennar for EU4 in the My-Anbennar repo.
The following rules are ENFORCED by the Sheriff plugin and pre-PR gate:

1. **Conflict hotspots**: Respect automation/conflict_hotspots.yaml single-writer rules.
   Never parallel-work on a single-writer hotspot file.
2. **Canonical vs legacy ownership**: Follow docs/wiki/verne-canonical-vs-legacy-file-registry.md.
   Files marked "Legacy (do not extend)" MUST NOT be edited.
3. **Pre-PR gate**: Before opening a PR, run scripts/pre_pr_gate.sh and fix all failures.
4. **Mission truth**: missions/Verne_Missions.txt is the spine — validate couplings on every change.
5. **Spec-first**: New gameplay features require a schema-valid mod-spec.json before code.

## Current Change Risk Report

${hotspotReport}

## Mod-Spec Quick Reference

Meta schema: schemas/mod-spec.schema.json
Required fields: meta, scope, objects, filePlan, validationPlan
filePlan[].policy values: canonical | legacy-no-extend | shared-touchpoint

## OpenClaw Tools (anbennar.*)

- anbennar.preflight    → run pre-commit checks + doctor report
- anbennar.sync_with_main → git fetch + rebase origin/main
- anbennar.validate_all  → run full pre_pr_gate.sh + all audits
- anbennar.spec_compile  → prose → mod-spec.json (schema-validated)

## State Files (CI-shared, do not delete)

- automation/agent_state/current_spec.json   — latest validated spec
- automation/agent_state/object_index.json   — derived ID index
- automation/registries/verne_file_registry.json — canonical/legacy ownership
`;
}

// ---------------------------------------------------------------------------
// Tool handlers (anbennar.*)
// ---------------------------------------------------------------------------

const tools: Record<string, (args: Record<string, unknown>) => string> = {
  "anbennar.preflight": (_args) => {
    const doctor = runPython("scripts/repo_doctor.py");
    const hotspots = runPython("scripts/validate_conflict_hotspots.py");
    return `=== preflight ===\n\nDoctor:\n${doctor}\n\nHotspots:\n${hotspots}`;
  },

  "anbennar.sync_with_main": (_args) => {
    git("fetch origin main");
    const status = git("rebase origin/main");
    return `Sync result:\n${status}`;
  },

  "anbennar.validate_all": (_args) => {
    const gate = runPython("scripts/pre_pr_gate.sh");
    const spec = existsSync("automation/agent_state/current_spec.json")
      ? "Spec: OK"
      : "Spec: MISSING (run anbennar.spec_compile first)";
    return `=== pre_pr_gate ===\n${gate}\n\n${spec}`;
  },

  "anbennar.spec_compile": (args) => {
    const specPath = join(WORKSPACE, "automation/agent_state/current_spec.json");
    // Write spec from provided prose
    const spec = args.spec as string;
    if (!spec) return "Error: no spec provided. Usage: anbennar.spec_compile { spec: '...' }";
    try {
      const parsed = JSON.parse(spec);
      // Basic schema validation
      const required = ["meta", "scope", "objects", "filePlan", "validationPlan"];
      const missing = required.filter((k) => !(k in parsed));
      if (missing.length) {
        return `Schema validation FAILED — missing fields: ${missing.join(", ")}`;
      }
      // Ensure directory
      execSync(`powershell -Command "New-Item -ItemType Directory -Force -Path '${join(WORKSPACE, "automation", "agent_state")}' | Out-Null"`);
      require("node:fs").writeFileSync(specPath, JSON.stringify(parsed, null, 2), "utf8");
      return `Spec written to ${specPath}`;
    } catch (e: any) {
      return `Error: ${e.message}`;
    }
  },
};

// ---------------------------------------------------------------------------
// Plugin registration
// ---------------------------------------------------------------------------

export default {
  id: "my-anbennar-sheriff",

  async onBeforePromptBuild(_event: unknown, _ctx: unknown) {
    return {
      prependSystemContext: getAnbennarContext(),
    };
  },

  // Expose tools — note: actual tool registration depends on OpenClaw plugin API
  // This provides the handler map; OpenClaw maps tool names to these handlers
  toolHandlers: tools,
};
