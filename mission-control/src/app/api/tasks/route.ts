import { NextResponse } from "next/server";
import { readFile, writeFile } from "fs/promises";

const DATA_PATH = "C:\\Users\\User\\.openclaw\\workspace\\mission-control\\data\\tasks.json";

interface Task {
  id: string;
  title: string;
  description: string;
  status: "backlog" | "in-progress" | "review" | "done";
  priority: number;
  assignee: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

interface TaskData {
  tasks: Task[];
  lastId: number;
}

async function readTasks(): Promise<TaskData> {
  try {
    const raw = await readFile(DATA_PATH, "utf-8");
    return JSON.parse(raw);
  } catch {
    return { tasks: [], lastId: 0 };
  }
}

async function writeTasks(data: TaskData) {
  await writeFile(DATA_PATH, JSON.stringify(data, null, 2));
}

export async function GET() {
  const data = await readTasks();
  return NextResponse.json(data.tasks);
}

export async function POST(req: Request) {
  const body = await req.json();
  const data = await readTasks();
  const now = new Date().toISOString();

  const newTask: Task = {
    id: `task-${String(data.lastId + 1).padStart(3, "0")}`,
    title: body.title || "Untitled",
    description: body.description || "",
    status: "backlog",
    priority: body.priority || 3,
    assignee: body.assignee || "jordan",
    tags: body.tags || [],
    createdAt: now,
    updatedAt: now,
  };

  data.tasks.push(newTask);
  data.lastId += 1;
  await writeTasks(data);

  return NextResponse.json(newTask, { status: 201 });
}

export async function PATCH(req: Request) {
  const body = await req.json();
  const data = await readTasks();

  const idx = data.tasks.findIndex((t) => t.id === body.id);
  if (idx === -1) {
    return NextResponse.json({ error: "Task not found" }, { status: 404 });
  }

  data.tasks[idx] = {
    ...data.tasks[idx],
    ...body,
    updatedAt: new Date().toISOString(),
  };
  await writeTasks(data);

  return NextResponse.json(data.tasks[idx]);
}

export async function DELETE(req: Request) {
  const { searchParams } = new URL(req.url);
  const id = searchParams.get("id");
  if (!id) return NextResponse.json({ error: "id required" }, { status: 400 });

  const data = await readTasks();
  data.tasks = data.tasks.filter((t) => t.id !== id);
  await writeTasks(data);

  return NextResponse.json({ ok: true });
}
