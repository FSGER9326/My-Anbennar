import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const MEMORY_DIR = "C:\\Users\\User\\.openclaw\\workspace\\memory";
const MEMORY_FILE = "C:\\Users\\User\\.openclaw\\workspace\\MEMORY.md";

interface Section {
  title: string;
  content: string;
  wordCount: number;
  tags: string[];
}

interface DayEntry {
  date: string;
  file: string;
  preview: string;
  sections: Section[];
  wordCount: number;
  lastUpdated: string;
}

function extractTags(content: string): string[] {
  const tags: string[] = [];
  const patterns = [
    /\b(urgent|important|blocked|done|fix|bug|todo|fixme|decision|note|learned|idea|problem|solution)\b/gi,
  ];
  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(content)) !== null) {
      const tag = match[1].toLowerCase();
      if (!tags.includes(tag)) tags.push(tag);
    }
  }
  return tags;
}

function countWords(text: string): number {
  return text.trim().split(/\s+/).filter(Boolean).length;
}

function parseSections(content: string): Section[] {
  const sections: Section[] = [];
  const lines = content.split("\n");
  let currentTitle = "";
  let currentContent: string[] = [];

  for (const line of lines) {
    const headerMatch = line.match(/^##\s+(.+)/);
    if (headerMatch) {
      if (currentTitle || currentContent.length > 0) {
        const raw = currentContent.join("\n").trim();
        sections.push({
          title: currentTitle || "Introduction",
          content: raw,
          wordCount: countWords(raw),
          tags: extractTags(raw),
        });
      }
      currentTitle = headerMatch[1].trim();
      currentContent = [];
    } else {
      currentContent.push(line);
    }
  }

  // Push last section
  if (currentTitle || currentContent.length > 0) {
    const raw = currentContent.join("\n").trim();
    sections.push({
      title: currentTitle || "Introduction",
      content: raw,
      wordCount: countWords(raw),
      tags: extractTags(raw),
    });
  }

  return sections;
}

function getTimestamp(filePath: string): string {
  try {
    const stats = fs.statSync(filePath);
    return stats.mtime.toISOString();
  } catch {
    return new Date().toISOString();
  }
}

export async function GET() {
  try {
    // Read daily files
    const files = fs.readdirSync(MEMORY_DIR).filter((f) => f.endsWith(".md")).sort().reverse();

    const days: DayEntry[] = files.map((file) => {
      const filePath = path.join(MEMORY_DIR, file);
      const content = fs.readFileSync(filePath, "utf-8");
      const date = file.replace(".md", "");
      const sections = parseSections(content);
      const preview = content
        .replace(/^#.*/, "")
        .replace(/##.*/g, "")
        .trim()
        .slice(0, 100);
      const wordCount = countWords(content);
      const lastUpdated = getTimestamp(filePath);

      return { date, file, preview, sections, wordCount, lastUpdated };
    });

    // Read long-term memory
    let longTerm = "";
    if (fs.existsSync(MEMORY_FILE)) {
      longTerm = fs.readFileSync(MEMORY_FILE, "utf-8");
    }
    const longTermUpdated = fs.existsSync(MEMORY_FILE)
      ? getTimestamp(MEMORY_FILE)
      : null;

    // Stats
    const totalEntries = days.reduce((sum, d) => sum + d.sections.length, 0);
    const oldestDate = days.length > 0 ? days[days.length - 1].date : null;

    return NextResponse.json({
      days,
      longTerm,
      longTermUpdated,
      stats: {
        totalDays: days.length,
        totalEntries,
        oldestDate,
      },
    });
  } catch (error) {
    console.error("Memory API error:", error);
    return NextResponse.json(
      { error: "Failed to read memory files" },
      { status: 500 }
    );
  }
}

export async function PUT(request: Request) {
  try {
    const body = await request.json();
    const { date, content, isLongTerm } = body;

    if (isLongTerm) {
      fs.writeFileSync(MEMORY_FILE, content, "utf-8");
      return NextResponse.json({ success: true });
    }

    if (!date) {
      return NextResponse.json(
        { error: "Date is required" },
        { status: 400 }
      );
    }

    const filePath = path.join(MEMORY_DIR, `${date}.md`);
    fs.writeFileSync(filePath, content, "utf-8");
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Memory write error:", error);
    return NextResponse.json(
      { error: "Failed to write memory file" },
      { status: 500 }
    );
  }
}
