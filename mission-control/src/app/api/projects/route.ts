import { NextResponse } from "next/server";
import { readFile, writeFile } from "fs/promises";
import path from "path";

const DATA_PATH = path.join(process.cwd(), "data", "projects.json");

export async function GET() {
  const data = await readFile(DATA_PATH, "utf-8");
  return NextResponse.json(JSON.parse(data));
}

export async function POST(request: Request) {
  const body = await request.json();
  const data = JSON.parse(await readFile(DATA_PATH, "utf-8"));

  const newProject = {
    id: `proj-${Date.now()}`,
    name: body.name || "New Project",
    description: body.description || "",
    status: "planning",
    progress: 0,
    color: body.color || "#8b5cf6",
    lastUpdated: new Date().toISOString(),
    milestones: body.milestones || [],
    tasks: [],
    planningNotes: [],
  };

  data.projects.push(newProject);
  await writeFile(DATA_PATH, JSON.stringify(data, null, 2));
  return NextResponse.json(newProject);
}
