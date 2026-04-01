import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const WORKSPACE = "C:\\Users\\User\\.openclaw\\workspace";

interface DocEntry {
  path: string;
  name: string;
  category: string;
  type: string;
  size: number;
  lastModified: string;
  preview: string;
  folder: string;
}

interface Category {
  name: string;
  count: number;
  color: string;
}

const CATEGORY_COLORS: Record<string, string> = {
  modding: "#8b5cf6",
  memory: "#3b82f6",
  learnings: "#f59e0b",
  skills: "#10b981",
  docs: "#6366f1",
  config: "#64748b",
};

function detectCategory(filePath: string): string {
  const lower = filePath.replace(/\\/g, "/").toLowerCase();
  if (lower.includes("design/lanes") || lower.includes("verne")) return "modding";
  if (lower.includes("/memory/") || lower === "memory") return "memory";
  if (lower.includes("/.learnings/") || lower.includes("/learnings/")) return "learnings";
  if (lower.includes("/skills/")) return "skills";
  if (lower.includes("/docs/")) return "docs";
  return "config";
}

function getFileType(fileName: string): string {
  const ext = path.extname(fileName).toLowerCase();
  if (ext === ".md") return "markdown";
  if (ext === ".txt") return "text";
  if (ext === ".yml" || ext === ".yaml") return "yaml";
  if (ext === ".json") return "json";
  if (ext === ".html") return "html";
  return "other";
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function getPreview(content: string): string {
  return content
    .replace(/^#+\s+/gm, "")
    .replace(/[*_`~\[\]]/g, "")
    .replace(/\r?\n+/g, " ")
    .trim()
    .slice(0, 150);
}

function scanDir(
  dirPath: string,
  relativePrefix: string,
  extensions: string[]
): DocEntry[] {
  const entries: DocEntry[] = [];
  if (!fs.existsSync(dirPath)) return entries;

  try {
    const items = fs.readdirSync(dirPath);
    for (const item of items) {
      const fullPath = path.join(dirPath, item);
      const relativePath = relativePrefix ? `${relativePrefix}/${item}` : item;

      try {
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
          // Skip hidden dirs and node_modules
          if (item.startsWith(".") || item === "node_modules") continue;
          entries.push(...scanDir(fullPath, relativePath, extensions));
        } else {
          const ext = path.extname(item).toLowerCase();
          if (extensions.includes(ext)) {
            const content = fs.readFileSync(fullPath, "utf-8");
            entries.push({
              path: relativePath.replace(/\\/g, "/"),
              name: item.replace(/\.[^.]+$/, ""),
              category: detectCategory(relativePath),
              type: getFileType(item),
              size: stat.size,
              lastModified: stat.mtime.toISOString(),
              preview: getPreview(content),
              folder: relativePrefix || "root",
            });
          }
        }
      } catch {
        // Skip inaccessible files
      }
    }
  } catch {
    // Skip inaccessible directories
  }

  return entries;
}

export async function GET(request: Request) {
  try {
    // Support single-file content fetch: /api/docs?file=docs/foo.md
    const { searchParams } = new URL(request.url);
    const fileParam = searchParams.get("file");
    if (fileParam) {
      const resolved = path.resolve(WORKSPACE, fileParam);
      if (!resolved.startsWith(WORKSPACE)) {
        return NextResponse.json({ error: "Access denied" }, { status: 403 });
      }
      if (!fs.existsSync(resolved)) {
        return NextResponse.json({ error: "File not found" }, { status: 404 });
      }
      const content = fs.readFileSync(resolved, "utf-8");
      return NextResponse.json({ content, path: fileParam });
    }

    const extensions = [".md", ".txt", ".yml", ".yaml", ".json", ".html"];
    const docs: DocEntry[] = [];

    // 1. Root-level markdown files
    const rootMdFiles = ["AGENTS.md", "SOUL.md", "USER.md", "MEMORY.md", "TOOLS.md", "IDENTITY.md", "HEARTBEAT.md"];
    for (const file of rootMdFiles) {
      const fullPath = path.join(WORKSPACE, file);
      if (fs.existsSync(fullPath)) {
        try {
          const stat = fs.statSync(fullPath);
          const content = fs.readFileSync(fullPath, "utf-8");
          docs.push({
            path: file,
            name: file.replace(".md", ""),
            category: "config",
            type: "markdown",
            size: stat.size,
            lastModified: stat.mtime.toISOString(),
            preview: getPreview(content),
            folder: "root",
          });
        } catch { /* skip */ }
      }
    }

    // 2. Also scan for any other .md at root we might have missed
    try {
      const rootItems = fs.readdirSync(WORKSPACE);
      for (const item of rootItems) {
        if (rootMdFiles.includes(item)) continue;
        const ext = path.extname(item).toLowerCase();
        if (ext !== ".md" && ext !== ".txt" && ext !== ".yml" && ext !== ".yaml") continue;
        const stat = fs.statSync(path.join(WORKSPACE, item));
        if (stat.isFile()) {
          const content = fs.readFileSync(path.join(WORKSPACE, item), "utf-8");
          docs.push({
            path: item,
            name: item.replace(/\.[^.]+$/, ""),
            category: "config",
            type: getFileType(item),
            size: stat.size,
            lastModified: stat.mtime.toISOString(),
            preview: getPreview(content),
            folder: "root",
          });
        }
      }
    } catch { /* skip */ }

    // 3. docs/ directory
    docs.push(...scanDir(path.join(WORKSPACE, "docs"), "docs", extensions));

    // 4. memory/ directory
    docs.push(...scanDir(path.join(WORKSPACE, "memory"), "memory", [".md"]));

    // 5. .learnings/ directory
    docs.push(...scanDir(path.join(WORKSPACE, ".learnings"), ".learnings", extensions));

    // 6. skills/*/SKILL.md files
    const skillsDir = path.join(WORKSPACE, "skills");
    if (fs.existsSync(skillsDir)) {
      try {
        const skillDirs = fs.readdirSync(skillsDir);
        for (const skillDir of skillDirs) {
          const skillMdPath = path.join(skillsDir, skillDir, "SKILL.md");
          if (fs.existsSync(skillMdPath)) {
            try {
              const stat = fs.statSync(skillMdPath);
              const content = fs.readFileSync(skillMdPath, "utf-8");
              docs.push({
                path: `skills/${skillDir}/SKILL.md`,
                name: skillDir,
                category: "skills",
                type: "markdown",
                size: stat.size,
                lastModified: stat.mtime.toISOString(),
                preview: getPreview(content),
                folder: `skills/${skillDir}`,
              });
            } catch { /* skip */ }
          }
        }
      } catch { /* skip */ }
    }

    // Deduplicate by path
    const seen = new Set<string>();
    const unique = docs.filter((d) => {
      if (seen.has(d.path)) return false;
      seen.add(d.path);
      return true;
    });

    // Build category stats
    const categoryMap = new Map<string, number>();
    for (const doc of unique) {
      categoryMap.set(doc.category, (categoryMap.get(doc.category) || 0) + 1);
    }

    const categories: Category[] = Array.from(categoryMap.entries())
      .map(([name, count]) => ({
        name,
        count,
        color: CATEGORY_COLORS[name] || "#6b7280",
      }))
      .sort((a, b) => b.count - a.count);

    const totalSize = unique.reduce((sum, d) => sum + d.size, 0);
    const latestModified = unique.reduce(
      (latest, d) => (d.lastModified > latest ? d.lastModified : latest),
      ""
    );

    return NextResponse.json({
      docs: unique.sort((a, b) => b.lastModified.localeCompare(a.lastModified)),
      categories,
      stats: {
        totalDocs: unique.length,
        totalSize: formatSize(totalSize),
        lastUpdated: latestModified,
      },
    });
  } catch (error) {
    console.error("Docs API error:", error);
    return NextResponse.json(
      { error: "Failed to read workspace documents" },
      { status: 500 }
    );
  }
}

export async function PUT(request: Request) {
  try {
    const body = await request.json();
    const { path: filePath, content } = body;

    if (!filePath || content === undefined) {
      return NextResponse.json(
        { error: "path and content are required" },
        { status: 400 }
      );
    }

    // Resolve full path — only allow within workspace
    const resolved = path.resolve(WORKSPACE, filePath);
    if (!resolved.startsWith(WORKSPACE)) {
      return NextResponse.json(
        { error: "Access denied" },
        { status: 403 }
      );
    }

    const dir = path.dirname(resolved);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(resolved, content, "utf-8");
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Docs write error:", error);
    return NextResponse.json(
      { error: "Failed to write document" },
      { status: 500 }
    );
  }
}
