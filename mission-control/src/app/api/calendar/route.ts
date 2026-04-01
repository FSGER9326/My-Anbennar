import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

interface CalendarEvent {
  id: string;
  name: string;
  schedule: string;
  nextRun: string;
  lastRun?: string;
  status: "active" | "paused" | "error";
  category: "modding" | "infrastructure" | "review" | "research";
  description: string;
  dayOfWeek?: number; // 0=Sun..6=Sat, computed
  hour?: number;
  type: "cron" | "background" | "milestone";
}

function dayOfWeek(dateStr: string): number {
  // Parse "Wed 10:00", "Mon/Wed/Fri 2AM", etc
  const days: Record<string, number> = {
    sun: 0, mon: 1, tue: 2, wed: 3, thu: 4, fri: 5, sat: 6,
  };
  const lower = dateStr.toLowerCase();
  for (const [name, num] of Object.entries(days)) {
    if (lower.includes(name)) return num;
  }
  return -1;
}

function parseHour(schedule: string): number {
  const match = schedule.match(/(\d{1,2})(?::(\d{2}))?\s*(am|pm)?/i);
  if (!match) return -1;
  let hour = parseInt(match[1]);
  const ampm = match[3]?.toLowerCase();
  if (ampm === "pm" && hour < 12) hour += 12;
  if (ampm === "am" && hour === 12) hour = 0;
  return hour;
}

function computeNextRun(schedule: string, now: Date): string {
  const dow = dayOfWeek(schedule);
  const hour = parseHour(schedule);

  if (dow === -1) {
    // Recurring interval or heartbeat-driven
    if (schedule.includes("30 min")) {
      const next = new Date(now.getTime() + 30 * 60 * 1000);
      return next.toLocaleString("de-DE", { timeZone: "Europe/Berlin" });
    }
    if (schedule.includes("2-4x") || schedule.includes("Heartbeat")) {
      return "Heartbeat-driven";
    }
    if (schedule.includes("6h")) {
      const next = new Date(now.getTime() + 6 * 60 * 60 * 1000);
      return next.toLocaleString("de-DE", { timeZone: "Europe/Berlin" });
    }
    if (schedule.includes("daily")) {
      const next = new Date(now);
      next.setDate(next.getDate() + 1);
      return next.toLocaleString("de-DE", { timeZone: "Europe/Berlin" });
    }
  }

  if (dow !== -1 && hour !== -1) {
    // Find next occurrence of this day+hour
    const next = new Date(now);
    next.setHours(hour, 0, 0, 0);
    let diff = dow - now.getDay();
    if (diff < 0 || (diff === 0 && next <= now)) diff += 7;
    next.setDate(next.getDate() + diff);
    return next.toLocaleString("de-DE", { timeZone: "Europe/Berlin" });
  }

  return "Unknown";
}

export async function GET() {
  const now = new Date();

  const events: CalendarEvent[] = [
    {
      id: "cal-001",
      name: "Health Monitor",
      schedule: "Every 30 min",
      nextRun: computeNextRun("Every 30 min", now),
      status: "active",
      category: "infrastructure",
      description: "Gateway status, task audit, channel health, log scan",
      type: "cron",
    },
    {
      id: "cal-002",
      name: "QA Compliance Scan",
      schedule: "Mon/Wed/Fri 2:00 AM",
      nextRun: computeNextRun("Wed 2:00 AM", now),
      lastRun: "Never",
      status: "paused",
      category: "modding",
      description: "Check S01–S08 compliance on all lane design files",
      dayOfWeek: 1, // Mon
      hour: 2,
      type: "cron",
    },
    {
      id: "cal-003",
      name: "Anbennar Upstream Sync",
      schedule: "Wed + Sun 10:00 AM",
      nextRun: computeNextRun("Wed 10:00 AM", now),
      lastRun: "2026-03-31 10:00",
      status: "active",
      category: "modding",
      description: "Check Anbennar upstream for new commits since last sync",
      type: "cron",
    },
    {
      id: "cal-004",
      name: "Mod Inspiration Scout",
      schedule: "Mon + Thu 8:00 PM",
      nextRun: computeNextRun("Thu 20:00", now),
      lastRun: "2026-03-31 20:00",
      status: "active",
      category: "research",
      description: "Research mod inspiration from Paradox forums, Steam Workshop",
      type: "cron",
    },
    {
      id: "cal-005",
      name: "Lane Review",
      schedule: "Monday 8:00 AM",
      nextRun: computeNextRun("Mon 8:00 AM", now),
      status: "active",
      category: "review",
      description: "Weekly lane design review — check for divergence, missing content",
      type: "cron",
    },
    {
      id: "cal-006",
      name: "Config Audit",
      schedule: "Tuesday 8:00 PM",
      nextRun: computeNextRun("Tue 20:00", now),
      status: "active",
      category: "infrastructure",
      description: "Review OpenClaw config, plugin status, memory index health",
      type: "cron",
    },
    {
      id: "cal-007",
      name: "Daily Memory Review",
      schedule: "2–4x/day (heartbeat-driven)",
      nextRun: "Heartbeat-driven",
      status: "active",
      category: "infrastructure",
      description: "Read recent daily files, promote to MEMORY.md, update .learnings/",
      type: "cron",
    },
    // Background worker queued tasks
    {
      id: "bg-001",
      name: "Write modifier definitions",
      schedule: "Queued — P1 background",
      nextRun: "When idle",
      status: "active",
      category: "modding",
      description: "Create verne_overhaul_modifiers.txt — blocks QA and localisation",
      type: "background",
    },
    {
      id: "bg-002",
      name: "Write localisation skeleton",
      schedule: "Queued — P1 background",
      nextRun: "When idle (after modifiers)",
      status: "active",
      category: "modding",
      description: "Create base localisation file for all Verne overhaul content",
      type: "background",
    },
    {
      id: "bg-003",
      name: "QA compliance scan (8 files)",
      schedule: "Queued — P2 background",
      nextRun: "When idle",
      status: "paused",
      category: "review",
      description: "Full S01–S08 compliance check on all lane design files",
      type: "background",
    },
    {
      id: "bg-004",
      name: "Generate GFX assets",
      schedule: "Queued — P2 background",
      nextRun: "When idle",
      status: "active",
      category: "modding",
      description: "Create remaining 11 mission icon assets via DALL-E",
      type: "background",
    },
    {
      id: "bg-005",
      name: "Review & consolidate learnings",
      schedule: "Queued — P3 background",
      nextRun: "When idle",
      status: "active",
      category: "infrastructure",
      description: "Promote important .learnings/ entries to MEMORY.md",
      type: "background",
    },
  ];

  return NextResponse.json(events);
}
