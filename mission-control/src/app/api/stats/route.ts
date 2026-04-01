import { NextResponse } from "next/server";
import { readFile, readdir } from "fs/promises";
import { join } from "path";

export const dynamic = "force-dynamic";

export async function GET() {
  // Task stats
  let totalTasks = 0;
  let doneTasks = 0;
  let backlogTasks = 0;
  let inProgressTasks = 0;
  let reviewTasks = 0;

  try {
    const taskData = await readFile(
      "C:\\Users\\User\\.openclaw\\workspace\\mission-control\\data\\tasks.json",
      "utf-8"
    );
    const parsed = JSON.parse(taskData);
    totalTasks = parsed.tasks.length;
    doneTasks = parsed.tasks.filter((t: { status: string }) => t.status === "done").length;
    backlogTasks = parsed.tasks.filter((t: { status: string }) => t.status === "backlog").length;
    inProgressTasks = parsed.tasks.filter((t: { status: string }) => t.status === "in-progress").length;
    reviewTasks = parsed.tasks.filter((t: { status: string }) => t.status === "review").length;
  } catch {
    // no file
  }

  // Learnings count
  let learningsCount = 0;
  try {
    const content = await readFile(
      "C:\\Users\\User\\.openclaw\\.learnings\\LEARNINGS.md",
      "utf-8"
    );
    learningsCount = (content.match(/^## \[/gm) || []).length;
  } catch {}

  // Skills count
  let skillsCount = 0;
  try {
    const skillsDir = "C:\\Users\\User\\.openclaw\\workspace\\skills";
    const dirs = await readdir(skillsDir, { withFileTypes: true });
    skillsCount = dirs.filter((d) => d.isDirectory()).length;
  } catch {}

  // Trials count
  let trialsCount = 0;
  try {
    const content = await readFile(
      "C:\\Users\\User\\.openclaw\\workspace\\docs\\subagent-patterns.md",
      "utf-8"
    );
    trialsCount = (content.match(/^### Trial \d/m) || []).length;
  } catch {}

  // Memory files
  let memoryFiles = 0;
  try {
    const memDir = "C:\\Users\\User\\.openclaw\\workspace\\memory";
    const files = await readdir(memDir);
    memoryFiles = files.length;
  } catch {}

  // Workspace docs
  let docFiles = 0;
  try {
    const docsDir = "C:\\Users\\User\\.openclaw\\workspace\\docs";
    const files = await readdir(docsDir);
    docFiles = files.length;
  } catch {}

  return NextResponse.json({
    tasks: {
      total: totalTasks,
      done: doneTasks,
      backlog: backlogTasks,
      inProgress: inProgressTasks,
      review: reviewTasks,
      completionRate: totalTasks > 0 ? Math.round((doneTasks / totalTasks) * 100) : 0,
    },
    learnings: learningsCount,
    skills: skillsCount,
    trials: trialsCount,
    memoryFiles,
    docFiles,
    uptime: process.uptime(),
    memory: {
      rss: Math.round(process.memoryUsage().rss / 1024 / 1024),
      heapUsed: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
      heapTotal: Math.round(process.memoryUsage().heapTotal / 1024 / 1024),
    },
    model: "openrouter/xiaomi/mimo-v2-omni",
    host: "DESKTOP-FOASM6G",
    channel: "webchat",
    timezone: "Europe/Berlin",
  });
}
