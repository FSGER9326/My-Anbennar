import { NextResponse } from "next/server";
import { readdir, readFile } from "fs/promises";
import { join } from "path";

export const dynamic = "force-dynamic";

export async function GET() {
  // Count learnings
  let learningsCount = 0;
  try {
    const content = await readFile(
      "C:\\Users\\User\\.openclaw\\.learnings\\LEARNINGS.md",
      "utf-8"
    );
    learningsCount = (content.match(/^## \[/gm) || []).length;
  } catch {
    // no file
  }

  // Count skills
  let skillsCount = 0;
  try {
    const skillsDir = "C:\\Users\\User\\.openclaw\\workspace\\skills";
    const dirs = await readdir(skillsDir, { withFileTypes: true });
    skillsCount = dirs.filter((d) => d.isDirectory()).length;
  } catch {
    // no dir
  }

  // Count memory files
  let memoryFiles = 0;
  try {
    const memDir = "C:\\Users\\User\\.openclaw\\workspace\\memory";
    const files = await readdir(memDir);
    memoryFiles = files.length;
  } catch {
    // no dir
  }

  // Read workspace files count
  let workspaceFiles = 0;
  try {
    const docsDir = "C:\\Users\\User\\.openclaw\\workspace\\docs";
    const files = await readdir(docsDir);
    workspaceFiles = files.length;
  } catch {
    // no dir
  }

  // Read task counts
  let totalTasks = 0;
  let doneTasks = 0;
  try {
    const taskData = await readFile(
      "C:\\Users\\User\\.openclaw\\workspace\\mission-control\\data\\tasks.json",
      "utf-8"
    );
    const parsed = JSON.parse(taskData);
    totalTasks = parsed.tasks.length;
    doneTasks = parsed.tasks.filter((t: { status: string }) => t.status === "done").length;
  } catch {
    // no file
  }

  return NextResponse.json({
    name: "Jordan",
    status: "idle",
    model: "openrouter/xiaomi/mimo-v2-omni",
    channel: "webchat",
    sessionStart: new Date().toISOString(),
    timezone: "Europe/Berlin",
    host: "DESKTOP-FOASM6G",
    uptime: process.uptime(),
    memory: {
      rss: process.memoryUsage().rss,
      heapUsed: process.memoryUsage().heapUsed,
      heapTotal: process.memoryUsage().heapTotal,
    },
    stats: {
      learningsCount,
      skillsCount,
      memoryFiles,
      workspaceFiles,
      totalTasks,
      doneTasks,
    },
    recentDecisions: [
      "Designed Linear-style mission control dashboard",
      "Switched from card dashboard to kanban board layout",
      "Set up local JSON task database from background-worker.md",
      "Integrated self-enhancement architecture with background worker",
      "Established layered memory indexing (Tier 1/2/3)",
    ],
  });
}
