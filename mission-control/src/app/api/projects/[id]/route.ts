import { NextResponse } from "next/server";
import { readFile, writeFile } from "fs/promises";
import path from "path";

const DATA_PATH = path.join(process.cwd(), "data", "projects.json");

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const data = JSON.parse(await readFile(DATA_PATH, "utf-8"));
  const project = data.projects.find((p: { id: string }) => p.id === id);
  if (!project) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  return NextResponse.json(project);
}

export async function PATCH(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const body = await request.json();
  const data = JSON.parse(await readFile(DATA_PATH, "utf-8"));
  const idx = data.projects.findIndex((p: { id: string }) => p.id === id);
  if (idx === -1) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  data.projects[idx] = { ...data.projects[idx], ...body, lastUpdated: new Date().toISOString() };
  await writeFile(DATA_PATH, JSON.stringify(data, null, 2));
  return NextResponse.json(data.projects[idx]);
}

export async function DELETE(
  _request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const data = JSON.parse(await readFile(DATA_PATH, "utf-8"));
  data.projects = data.projects.filter((p: { id: string }) => p.id !== id);
  await writeFile(DATA_PATH, JSON.stringify(data, null, 2));
  return NextResponse.json({ ok: true });
}
