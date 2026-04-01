"use client";

import { useEffect, useState, useCallback } from "react";
import { Clock, ChevronRight, CheckCircle2, Pause, AlertCircle } from "lucide-react";

interface CalendarEvent {
  id: string;
  name: string;
  schedule: string;
  nextRun: string;
  lastRun?: string;
  status: "active" | "paused" | "error";
  category: "modding" | "infrastructure" | "review" | "research";
  description: string;
  dayOfWeek?: number;
  hour?: number;
  type: "cron" | "background" | "milestone";
}

const categoryColors: Record<string, { bg: string; border: string; text: string; dot: string }> = {
  modding: {
    bg: "bg-blue-500/10",
    border: "border-blue-500/30",
    text: "text-blue-400",
    dot: "bg-blue-500",
  },
  infrastructure: {
    bg: "bg-green-500/10",
    border: "border-green-500/30",
    text: "text-green-400",
    dot: "bg-green-500",
  },
  review: {
    bg: "bg-yellow-500/10",
    border: "border-yellow-500/30",
    text: "text-yellow-400",
    dot: "bg-yellow-500",
  },
  research: {
    bg: "bg-purple-500/10",
    border: "border-purple-500/30",
    text: "text-purple-400",
    dot: "bg-purple-500",
  },
};

const statusIcon = {
  active: <CheckCircle2 className="w-3 h-3 text-green-500" />,
  paused: <Pause className="w-3 h-3 text-yellow-500" />,
  error: <AlertCircle className="w-3 h-3 text-red-500" />,
};

const dayNames = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function getMonday(d: Date): Date {
  const date = new Date(d);
  const day = date.getDay();
  const diff = date.getDate() - day + (day === 0 ? -6 : 1);
  date.setDate(diff);
  date.setHours(0, 0, 0, 0);
  return date;
}

function getDayIndex(eventDay: number): number {
  // eventDay: 0=Sun..6=Sat → column: 0=Mon..6=Sun
  return eventDay === 0 ? 6 : eventDay - 1;
}

export default function CalendarPage() {
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<CalendarEvent | null>(null);
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const res = await fetch("/api/calendar");
        const data = await res.json();
        setEvents(data);
      } catch {
        // silently fail
      } finally {
        setLoading(false);
      }
    };
    fetchEvents();
    const interval = setInterval(fetchEvents, 60000);
    return () => clearInterval(interval);
  }, []);

  // Live clock
  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  const monday = getMonday(now);

  // Build the 7 day headers with dates
  const weekDays = Array.from({ length: 7 }, (_, i) => {
    const d = new Date(monday);
    d.setDate(monday.getDate() + i);
    return d;
  });

  // Separate cron jobs (with dayOfWeek) from background/interval tasks
  const cronEvents = events.filter((e) => e.type === "cron" && e.dayOfWeek !== undefined && e.dayOfWeek > 0);
  const bgEvents = events.filter((e) => e.type === "background");
  const intervalEvents = events.filter((e) => e.type === "cron" && (e.dayOfWeek === undefined || e.dayOfWeek === 0) && !e.schedule.includes("Heartbeat"));

  // Current day column index (Mon=0..Sun=6)
  const currentDayIdx = now.getDay() === 0 ? 6 : now.getDay() - 1;

  // Current hour for the time indicator position
  const currentHour = now.getHours() + now.getMinutes() / 60;

  // Place cron events into their day columns
  const eventsByDay: CalendarEvent[][] = Array.from({ length: 7 }, () => []);
  for (const event of cronEvents) {
    if (event.dayOfWeek !== undefined && event.dayOfWeek > 0) {
      const idx = getDayIndex(event.dayOfWeek);
      eventsByDay[idx].push(event);
    }
  }

  const handleMoveForward = useCallback(async (event: CalendarEvent) => {
    // Move a review item to in-progress (simulate by marking active)
    setSelected({ ...event, status: "active" });
  }, []);

  return (
    <div className="p-6 max-w-[1200px]">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-lg font-semibold text-gray-100">Calendar</h1>
          <p className="text-xs text-gray-500 mt-0.5">
            Week of {monday.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-3 text-[10px] text-gray-500">
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-blue-500" /> modding</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-green-500" /> infrastructure</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-yellow-500" /> review</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-purple-500" /> research</span>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-gray-500 text-sm animate-pulse">Loading calendar...</div>
      ) : (
        <div className="space-y-6">
          {/* Weekly Grid */}
          <div className="border border-gray-800/60 rounded-xl overflow-hidden">
            {/* Day headers */}
            <div className="grid grid-cols-7 border-b border-gray-800/60">
              {weekDays.map((day, i) => {
                const isToday = day.toDateString() === now.toDateString();
                return (
                  <div
                    key={i}
                    className={`px-3 py-2.5 text-center border-r border-gray-800/40 last:border-r-0 ${
                      isToday ? "bg-purple-500/5" : ""
                    }`}
                  >
                    <div className="text-[10px] uppercase text-gray-500">{dayNames[i]}</div>
                    <div className={`text-lg font-semibold mt-0.5 ${
                      isToday ? "text-purple-400" : "text-gray-300"
                    }`}>
                      {day.getDate()}
                    </div>
                    {isToday && (
                      <div className="text-[10px] text-purple-500 mt-0.5 font-medium">Today</div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Day columns with events */}
            <div className="grid grid-cols-7 min-h-[260px] relative">
              {/* Current time indicator */}
              <div
                className="absolute top-0 bottom-0 z-10 pointer-events-none"
                style={{
                  left: `${(currentDayIdx / 7) * 100 + (1 / 7) * 100 * (currentHour / 24)}%`,
                  width: "2px",
                }}
              >
                <div className="w-2 h-2 -ml-[3px] rounded-full bg-red-500 relative -top-1" />
                <div className="w-full h-full bg-red-500/20" />
              </div>

              {Array.from({ length: 7 }, (_, i) => (
                <div
                  key={i}
                  className={`border-r border-gray-800/40 last:border-r-0 px-2 py-2 space-y-1.5 ${
                    i === currentDayIdx ? "bg-purple-500/[0.02]" : ""
                  }`}
                >
                  {eventsByDay[i].map((event) => {
                    const colors = categoryColors[event.category] || categoryColors.infrastructure;
                    return (
                      <button
                        key={event.id}
                        onClick={() => setSelected(event)}
                        className={`w-full text-left px-2.5 py-2 rounded-lg border ${colors.border} ${colors.bg} hover:brightness-125 transition-all group`}
                      >
                        <div className="flex items-center gap-1.5">
                          <div className={`w-1.5 h-1.5 rounded-full ${colors.dot} shrink-0`} />
                          <span className={`text-xs font-medium ${colors.text} truncate`}>
                            {event.name}
                          </span>
                        </div>
                        <div className="text-[10px] text-gray-500 mt-0.5 truncate">
                          {event.schedule}
                        </div>
                      </button>
                    );
                  })}
                </div>
              ))}
            </div>
          </div>

          {/* Bottom sections: Background Queue + Interval Jobs */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* Background Task Queue */}
            <div className="bg-gray-900/50 border border-gray-800/60 rounded-xl p-4">
              <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">
                Background Queue
              </h3>
              <div className="space-y-1.5">
                {bgEvents.map((event) => {
                  const colors = categoryColors[event.category] || categoryColors.modding;
                  return (
                    <button
                      key={event.id}
                      onClick={() => setSelected(event)}
                      className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-800/40 transition-colors text-left"
                    >
                      <div className={`w-1.5 h-1.5 rounded-full ${colors.dot} shrink-0`} />
                      <div className="flex-1 min-w-0">
                        <div className="text-sm text-gray-300 truncate">{event.name}</div>
                        <div className="text-[10px] text-gray-500">{event.schedule}</div>
                      </div>
                      <span className={`text-[10px] px-1.5 py-0.5 rounded ${
                        event.status === "active" ? "bg-green-500/10 text-green-500" : "bg-yellow-500/10 text-yellow-500"
                      }`}>
                        {event.status === "active" ? "ready" : "paused"}
                      </span>
                      <ChevronRight className="w-3 h-3 text-gray-600" />
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Interval / Recurring Jobs */}
            <div className="bg-gray-900/50 border border-gray-800/60 rounded-xl p-4">
              <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">
                Recurring & Interval
              </h3>
              <div className="space-y-1.5">
                {intervalEvents.map((event) => {
                  const colors = categoryColors[event.category] || categoryColors.infrastructure;
                  return (
                    <button
                      key={event.id}
                      onClick={() => setSelected(event)}
                      className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-800/40 transition-colors text-left"
                    >
                      <div className={`w-1.5 h-1.5 rounded-full ${colors.dot} shrink-0`} />
                      <div className="flex-1 min-w-0">
                        <div className="text-sm text-gray-300 truncate">{event.name}</div>
                        <div className="text-[10px] text-gray-500">{event.schedule}</div>
                      </div>
                      {statusIcon[event.status]}
                      <ChevronRight className="w-3 h-3 text-gray-600" />
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Detail Panel */}
      {selected && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            onClick={() => setSelected(null)}
          />
          <div className="relative w-full max-w-sm bg-gray-900 border border-gray-700 rounded-xl shadow-2xl p-5 mx-4">
            <div className="flex items-start justify-between mb-3">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <div className={`w-2 h-2 rounded-full ${
                    categoryColors[selected.category]?.dot || "bg-gray-500"
                  }`} />
                  <span className={`text-[10px] uppercase font-medium ${
                    categoryColors[selected.category]?.text || "text-gray-400"
                  }`}>
                    {selected.category}
                  </span>
                  <span className="text-[10px] text-gray-600">·</span>
                  <span className="text-[10px] text-gray-500">{selected.type}</span>
                </div>
                <h3 className="text-base font-semibold text-gray-100">{selected.name}</h3>
              </div>
              {statusIcon[selected.status]}
            </div>

            <p className="text-sm text-gray-400 mb-4">{selected.description}</p>

            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-gray-500">Schedule</span>
                <span className="text-gray-300 font-mono">{selected.schedule}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Next run</span>
                <span className="text-gray-300">{selected.nextRun}</span>
              </div>
              {selected.lastRun && (
                <div className="flex justify-between">
                  <span className="text-gray-500">Last run</span>
                  <span className="text-gray-300">{selected.lastRun}</span>
                </div>
              )}
              <div className="flex justify-between">
                <span className="text-gray-500">Status</span>
                <span className={`font-medium ${
                  selected.status === "active" ? "text-green-400" : "text-yellow-400"
                }`}>
                  {selected.status}
                </span>
              </div>
            </div>

            {/* Actions */}
            <div className="flex justify-end gap-2 mt-5">
              <button
                onClick={() => setSelected(null)}
                className="px-3 py-1.5 text-sm text-gray-400 hover:text-gray-200 transition-colors"
              >
                Close
              </button>
              {selected.category === "review" && (
                <button
                  onClick={() => {
                    handleMoveForward(selected);
                    setSelected(null);
                  }}
                  className="px-4 py-1.5 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg transition-colors"
                >
                  Confirm → In Progress
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
