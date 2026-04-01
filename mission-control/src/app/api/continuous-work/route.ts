import { NextResponse } from "next/server";
import { readFile, writeFile } from "fs/promises";
import path from "path";

const STATE_PATH = path.join(process.cwd(), "data", "continuous-work.json");

export async function GET() {
  try {
    const data = JSON.parse(await readFile(STATE_PATH, "utf-8"));
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({ active: false, startedAt: null, tasksCompleted: 0, currentTask: null });
  }
}

export async function POST(request: Request) {
  const body = await request.json();
  const newState = {
    active: body.active,
    startedAt: body.active ? new Date().toISOString() : null,
    stoppedAt: body.active ? null : new Date().toISOString(),
    tasksCompleted: body.active ? 0 : (body.tasksCompleted || 0),
    currentTask: body.currentTask || null,
    lastActivity: new Date().toISOString(),
  };
  await writeFile(STATE_PATH, JSON.stringify(newState, null, 2));
  return NextResponse.json(newState);
}

export async function PATCH(request: Request) {
  let current: Record<string, unknown> = {};
  try {
    current = JSON.parse(await readFile(STATE_PATH, "utf-8"));
  } catch {}
  const body = await request.json();
  const updated = { ...current, ...body, lastActivity: new Date().toISOString() };
  await writeFile(STATE_PATH, JSON.stringify(updated, null, 2));
  return NextResponse.json(updated);
}
