/**
 * anbennar-preflight / handler.ts
 * Hook: command:new → session start preflight
 *
 * Runs: repo_doctor + hotspot validation
 * Writes: automation/reports/preflight_doctor.txt
 *         automation/reports/preflight_hotspots.txt
 */
import { execSync } from "node:child_process";
import { mkdirSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const WORKSPACE = process.cwd();
const REPORT_DIR = join(WORKSPACE, "automation/reports");

function sh(cmd: string): string {
  try {
    return execSync(cmd, { cwd: WORKSPACE, encoding: "utf8", timeout: 60000 }).trim();
  } catch (e: any) {
    return `[ERROR] ${(e.stderr || e.message || "").toString().trim()}`;
  }
}

function python(script: string): string {
  // Try python first (Windows), then python3
  for (const py of ["python", "python3"]) {
    try {
      return execSync(`${py} "${script}"`, {
        cwd: WORKSPACE,
        encoding: "utf8",
        timeout: 60000,
      }).trim();
    } catch {
      // try next
    }
  }
  return "[ERROR] python not found";
}

function ensureReportDir() {
  if (!existsSync(REPORT_DIR)) {
    mkdirSync(REPORT_DIR, { recursive: true });
  }
}

export default async function handler(event: { type: string; action?: string }) {
  if (event.type !== "command" && event.type !== "session") return;
  if (event.action && event.action !== "new" && event.action !== "start") return;

  ensureReportDir();

  // 1. Repo doctor
  const doctorScript = join(WORKSPACE, "scripts/repo_doctor.py");
  if (existsSync(doctorScript)) {
    const doctorOut = python(doctorScript);
    writeFileSync(join(REPORT_DIR, "preflight_doctor.txt"), doctorOut, "utf8");
  }

  // 2. Hotspot validation
  const hotspotScript = join(WORKSPACE, "scripts/validate_conflict_hotspots.py");
  if (existsSync(hotspotScript)) {
    const hotspotOut = python(hotspotScript);
    writeFileSync(join(REPORT_DIR, "preflight_hotspots.txt"), hotspotOut, "utf8");
  }

  console.log("[anbennar-preflight] Preflight complete.");
}
