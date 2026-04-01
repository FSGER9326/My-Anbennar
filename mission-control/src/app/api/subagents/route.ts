import { NextResponse } from "next/server";
import { readFile } from "fs/promises";

export const dynamic = "force-dynamic";

interface Trial {
  name: string;
  score: number;
  dimensions: Record<string, number>;
  scope: string;
  lesson: string;
  status: "completed" | "failed" | "running";
}

export async function GET() {
  try {
    const content = await readFile(
      "C:\\Users\\User\\.openclaw\\workspace\\docs\\subagent-patterns.md",
      "utf-8"
    );

    const trials: Trial[] = [];
    const trialSections = content.split(/^### Trial \d/m).slice(1);

    for (const section of trialSections) {
      const nameMatch = section.match(/^—?\s*(.+?)\n/);
      const scoreMatch = section.match(/Score:\s*(\d)\/5/);
      const dimensions: Record<string, number> = {};

      const dimStr = section.match(/\((.+?)\)/);
      if (dimStr) {
        const parts = dimStr[1].split(",");
        for (const part of parts) {
          const kv = part.trim().match(/(\w[\w\s-]*?):\s*(\d)/);
          if (kv) dimensions[kv[1].trim()] = parseInt(kv[2]);
        }
      }

      const scopeMatch = section.match(/Scope:\s*(\w+)\s*(—|-)\s*(.+?)(?:\n|$)/);
      const lessonMatch = section.match(/Lesson:\s*(.+?)(?:\n|$)/);

      const score = scoreMatch ? parseInt(scoreMatch[1]) : 0;
      let status: Trial["status"] = "completed";
      if (section.includes("timed out") || section.includes("failed")) status = "failed";
      if (section.includes("in progress") || section.includes("running")) status = "running";

      if (scoreMatch) {
        trials.push({
          name: nameMatch?.[1].trim() || "Unknown",
          score,
          dimensions,
          scope: scopeMatch?.[3] || scopeMatch?.[1] || "",
          lesson: lessonMatch?.[1].trim() || "",
          status,
        });
      }
    }

    return NextResponse.json(trials);
  } catch {
    return NextResponse.json([]);
  }
}
