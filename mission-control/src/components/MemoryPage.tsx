"use client";

import { useState, useEffect, useCallback, useMemo } from "react";
import {
  Search,
  ChevronDown,
  ChevronRight,
  Pencil,
  Save,
  X,
  Brain,
  Calendar,
} from "lucide-react";

// --- Types ---

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

interface MemoryData {
  days: DayEntry[];
  longTerm: string;
  longTermUpdated: string | null;
  stats: {
    totalDays: number;
    totalEntries: number;
    oldestDate: string | null;
  };
}

// --- Markdown Renderer ---

function renderMarkdown(text: string): string {
  let html = text;

  // Code blocks (must come first to avoid processing content inside)
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
    const escaped = code
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
    return `<pre class="bg-gray-800/60 rounded-md p-3 my-2 overflow-x-auto text-sm font-mono text-gray-300 border border-gray-700/40"><code>${escaped}</code></pre>`;
  });

  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code class="bg-gray-800/60 px-1.5 py-0.5 rounded text-purple-300 text-sm font-mono">$1</code>');

  // Headers
  html = html.replace(/^### (.+)$/gm, '<h3 class="text-sm font-semibold text-gray-200 mt-4 mb-1">$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2 class="text-base font-bold text-gray-100 mt-5 mb-2">$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1 class="text-lg font-bold text-gray-100 mt-4 mb-2">$1</h1>');

  // Bold and italic
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-purple-400 hover:text-purple-300 underline underline-offset-2" target="_blank" rel="noopener">$1</a>');

  // Unordered lists
  html = html.replace(/^(?:- (.+)\n?)+/gm, (match) => {
    const items = match.trim().split("\n").map(line => {
      const content = line.replace(/^- /, "");
      return `<li class="text-gray-300 ml-4">${content}</li>`;
    }).join("");
    return `<ul class="list-disc list-inside my-1 space-y-0.5">${items}</ul>`;
  });

  // Ordered lists
  html = html.replace(/^(?:\d+\. (.+)\n?)+/gm, (match) => {
    const items = match.trim().split("\n").map(line => {
      const content = line.replace(/^\d+\. /, "");
      return `<li class="text-gray-300 ml-4">${content}</li>`;
    }).join("");
    return `<ol class="list-decimal list-inside my-1 space-y-0.5">${items}</ol>`;
  });

  // Paragraphs — wrap remaining non-html lines
  html = html.replace(/^(?!<[a-z/])(.+)$/gm, '<p class="text-gray-300 leading-relaxed my-1">$1</p>');

  // Collapse multiple blank lines
  html = html.replace(/\n{3,}/g, "\n\n");

  return html;
}

// --- Date Helpers ---

function formatDate(dateStr: string): string {
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function formatDayOfWeek(dateStr: string): string {
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("en-US", { weekday: "short" });
}

function getMonthKey(dateStr: string): string {
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("en-US", { month: "long", year: "numeric" });
}

function formatTimestamp(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }) + " " + d.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
}

function truncate(text: string, max: number): string {
  if (text.length <= max) return text;
  return text.slice(0, max).trim() + "…";
}

// --- Component ---

export default function MemoryPage() {
  const [data, setData] = useState<MemoryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<"daily" | "longterm">("daily");
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set());
  const [editing, setEditing] = useState(false);
  const [editContent, setEditContent] = useState("");
  const [saving, setSaving] = useState(false);
  const [allContent, setAllContent] = useState<Record<string, string>>({});

  // Fetch memory data
  useEffect(() => {
    fetch("/api/memory")
      .then((r) => r.json())
      .then((d) => {
        setData(d);
        if (d.days.length > 0 && !selectedDate) {
          setSelectedDate(d.days[0].date);
        }
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  // Load all content for search
  useEffect(() => {
    if (!data) return;
    const contentMap: Record<string, string> = {};
    for (const day of data.days) {
      contentMap[day.date] = day.sections
        .map((s) => `${s.title}\n${s.content}`)
        .join("\n\n");
    }
    setAllContent(contentMap);
  }, [data]);

  // Filter days by search
  const filteredDays = useMemo(() => {
    if (!data) return [];
    if (!searchQuery.trim()) return data.days;
    const q = searchQuery.toLowerCase();
    return data.days.filter((day) => {
      if (day.date.includes(q)) return true;
      if (day.preview.toLowerCase().includes(q)) return true;
      const content = allContent[day.date] || "";
      return content.toLowerCase().includes(q);
    });
  }, [data, searchQuery, allContent]);

  // Group by month
  const groupedDays = useMemo(() => {
    const groups: { month: string; days: DayEntry[] }[] = [];
    let currentMonth = "";
    for (const day of filteredDays) {
      const mk = getMonthKey(day.date);
      if (mk !== currentMonth) {
        currentMonth = mk;
        groups.push({ month: mk, days: [] });
      }
      groups[groups.length - 1].days.push(day);
    }
    return groups;
  }, [filteredDays]);

  // Get selected day data
  const selectedDay = data?.days.find((d) => d.date === selectedDate);

  // Toggle section
  const toggleSection = useCallback((key: string) => {
    setExpandedSections((prev) => {
      const next = new Set(prev);
      if (next.has(key)) {
        next.delete(key);
      } else {
        next.add(key);
      }
      return next;
    });
  }, []);

  // Start editing
  const startEdit = useCallback(() => {
    if (tab === "longterm" && data) {
      setEditContent(data.longTerm);
    } else if (selectedDay) {
      const content = allContent[selectedDay.date] || "";
      setEditContent(content);
    }
    setEditing(true);
  }, [tab, data, selectedDay, allContent]);

  // Save edit
  const saveEdit = useCallback(async () => {
    setSaving(true);
    try {
      const body: Record<string, unknown> = {};
      if (tab === "longterm") {
        body.content = editContent;
        body.isLongTerm = true;
      } else {
        body.date = selectedDate;
        body.content = editContent;
      }

      await fetch("/api/memory", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      // Reload data
      const res = await fetch("/api/memory");
      const d = await res.json();
      setData(d);
      setEditing(false);
    } catch (e) {
      console.error("Save failed:", e);
    }
    setSaving(false);
  }, [tab, editContent, selectedDate]);

  // Expand/collapse all
  const [allExpanded, setAllExpanded] = useState(false);
  const toggleAllSections = useCallback(() => {
    if (!selectedDay) return;
    if (allExpanded) {
      setExpandedSections(new Set());
    } else {
      const keys = selectedDay.sections.map((_, i) => `${selectedDate}-${i}`);
      setExpandedSections(new Set(keys));
    }
    setAllExpanded(!allExpanded);
  }, [selectedDay, selectedDate, allExpanded]);

  // --- Render ---

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500 text-sm animate-pulse">Loading memory…</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500 text-sm">Failed to load memory data</div>
      </div>
    );
  }

  return (
    <div className="flex h-full">
      {/* Sidebar */}
      <div className="w-72 bg-gray-900 border-r border-gray-800/60 flex flex-col shrink-0">
        {/* Header */}
        <div className="px-4 py-3 border-b border-gray-800/60">
          <div className="flex items-center gap-2 mb-3">
            <Brain className="w-4 h-4 text-purple-400" />
            <span className="text-sm font-semibold text-gray-100">Memory</span>
            <span className="ml-auto text-[10px] text-gray-500 bg-gray-800/60 px-1.5 py-0.5 rounded">
              {data.stats.totalDays} days
            </span>
          </div>

          {/* Search */}
          <div className="relative">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-500" />
            <input
              type="text"
              placeholder="Search memory…"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-gray-800/50 border border-gray-700/40 rounded-md pl-8 pr-3 py-1.5 text-xs text-gray-200 placeholder:text-gray-600 focus:outline-none focus:border-purple-500/40 focus:ring-1 focus:ring-purple-500/20"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery("")}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300"
              >
                <X className="w-3 h-3" />
              </button>
            )}
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-gray-800/60">
          <button
            onClick={() => { setTab("daily"); setEditing(false); }}
            className={`flex-1 py-2 text-xs font-medium transition-theme ${
              tab === "daily"
                ? "text-purple-400 border-b-2 border-purple-400"
                : "text-gray-500 hover:text-gray-300"
            }`}
          >
            Daily
          </button>
          <button
            onClick={() => { setTab("longterm"); setEditing(false); }}
            className={`flex-1 py-2 text-xs font-medium transition-theme ${
              tab === "longterm"
                ? "text-purple-400 border-b-2 border-purple-400"
                : "text-gray-500 hover:text-gray-300"
            }`}
          >
            Long-term
          </button>
        </div>

        {/* Day list */}
        {tab === "daily" && (
          <div className="flex-1 overflow-y-auto">
            {searchQuery && (
              <div className="px-3 py-2 text-[10px] text-gray-500 uppercase tracking-wider">
                {filteredDays.length} result{filteredDays.length !== 1 ? "s" : ""}
              </div>
            )}
            {groupedDays.map((group) => (
              <div key={group.month}>
                <div className="px-3 py-2 text-[10px] text-gray-500 uppercase tracking-wider font-medium">
                  {group.month}
                </div>
                {group.days.map((day) => (
                  <button
                    key={day.date}
                    onClick={() => { setSelectedDate(day.date); setEditing(false); }}
                    className={`w-full text-left px-3 py-2 transition-theme ${
                      selectedDate === day.date
                        ? "bg-purple-500/10 border-l-2 border-purple-500 text-purple-300"
                        : "border-l-2 border-transparent hover:bg-gray-800/50 text-gray-400"
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-medium">{formatDate(day.date)}</span>
                      <span className="text-[10px] text-gray-600">{formatDayOfWeek(day.date)}</span>
                      <span className="ml-auto text-[10px] bg-gray-800/60 px-1.5 py-0.5 rounded text-gray-500">
                        {day.wordCount}w
                      </span>
                    </div>
                    <div className="text-[11px] text-gray-600 mt-0.5 truncate">
                      {truncate(day.preview.replace(/\n/g, " "), 55)}
                    </div>
                  </button>
                ))}
              </div>
            ))}
            {filteredDays.length === 0 && searchQuery && (
              <div className="px-3 py-6 text-center text-xs text-gray-600">
                No matching days found
              </div>
            )}
          </div>
        )}

        {/* Long-term info in sidebar */}
        {tab === "longterm" && (
          <div className="flex-1 overflow-y-auto px-3 py-4">
            <div className="flex items-center gap-2 mb-3">
              <Calendar className="w-3.5 h-3.5 text-gray-500" />
              <span className="text-xs text-gray-400">Long-term Memory</span>
            </div>
            {data.longTermUpdated && (
              <div className="text-[10px] text-gray-600 mb-2">
                Last updated: {formatTimestamp(data.longTermUpdated)}
              </div>
            )}
            <div className="text-[11px] text-gray-500">
              {data.longTerm ? `${countWordsSimple(data.longTerm)} words` : "Empty"}
            </div>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto">
        {tab === "daily" && selectedDay && (
          <div className="max-w-3xl mx-auto px-6 py-5">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
              <div>
                <h1 className="text-lg font-bold text-gray-100">
                  {formatDate(selectedDay.date)}
                </h1>
                <div className="flex items-center gap-3 mt-1">
                  <span className="text-xs text-gray-500">
                    {formatDayOfWeek(selectedDay.date)}
                  </span>
                  <span className="text-xs text-gray-600">·</span>
                  <span className="text-xs text-gray-500">
                    {selectedDay.wordCount} words
                  </span>
                  <span className="text-xs text-gray-600">·</span>
                  <span className="text-xs text-gray-500">
                    Updated {formatTimestamp(selectedDay.lastUpdated)}
                  </span>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={toggleAllSections}
                  className="text-xs text-gray-500 hover:text-gray-300 px-2 py-1 rounded hover:bg-gray-800/50 transition-theme"
                >
                  {allExpanded ? "Collapse all" : "Expand all"}
                </button>
                <button
                  onClick={editing ? () => setEditing(false) : startEdit}
                  className={`flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-md transition-theme ${
                    editing
                      ? "text-gray-400 hover:text-gray-200 hover:bg-gray-800/50"
                      : "text-purple-400 hover:text-purple-300 hover:bg-purple-500/10"
                  }`}
                >
                  {editing ? (
                    <>
                      <X className="w-3.5 h-3.5" />
                      Cancel
                    </>
                  ) : (
                    <>
                      <Pencil className="w-3.5 h-3.5" />
                      Edit
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Edit mode */}
            {editing ? (
              <div className="space-y-3">
                <textarea
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                  className="w-full h-[60vh] bg-gray-900 border border-gray-800/60 rounded-lg p-4 text-sm text-gray-200 font-mono leading-relaxed resize-none focus:outline-none focus:border-purple-500/40 focus:ring-1 focus:ring-purple-500/20"
                  spellCheck={false}
                />
                <button
                  onClick={saveEdit}
                  disabled={saving}
                  className="flex items-center gap-1.5 text-xs bg-purple-600 hover:bg-purple-500 text-white px-3 py-1.5 rounded-md transition-theme disabled:opacity-50"
                >
                  <Save className="w-3.5 h-3.5" />
                  {saving ? "Saving…" : "Save changes"}
                </button>
              </div>
            ) : (
              /* Sections */
              <div className="space-y-0">
                {selectedDay.sections.map((section, i) => {
                  const key = `${selectedDay.date}-${i}`;
                  const isExpanded = expandedSections.has(key);
                  return (
                    <div key={key} className="border-b border-gray-800/40 last:border-b-0">
                      <button
                        onClick={() => toggleSection(key)}
                        className="w-full flex items-center gap-2 py-3 text-left hover:text-gray-200 transition-theme group"
                      >
                        {isExpanded ? (
                          <ChevronDown className="w-4 h-4 text-gray-500 shrink-0" />
                        ) : (
                          <ChevronRight className="w-4 h-4 text-gray-500 shrink-0" />
                        )}
                        <span className="text-sm font-medium text-gray-200 flex-1">
                          {section.title}
                        </span>
                        <span className="text-[10px] text-gray-600 bg-gray-800/40 px-1.5 py-0.5 rounded">
                          {section.wordCount}w
                        </span>
                        {section.tags.length > 0 && (
                          <div className="flex gap-1">
                            {section.tags.slice(0, 3).map((tag) => (
                              <span
                                key={tag}
                                className="text-[10px] text-purple-400/70 bg-purple-500/10 px-1.5 py-0.5 rounded"
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        )}
                      </button>
                      {isExpanded && (
                        <div
                          className="pb-3 pl-6 prose-sm"
                          dangerouslySetInnerHTML={{
                            __html: renderMarkdown(section.content),
                          }}
                        />
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {tab === "longterm" && (
          <div className="max-w-3xl mx-auto px-6 py-5">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
              <div>
                <h1 className="text-lg font-bold text-gray-100">Long-term Memory</h1>
                <div className="flex items-center gap-3 mt-1">
                  <span className="text-xs text-gray-500">MEMORY.md</span>
                  {data.longTermUpdated && (
                    <>
                      <span className="text-xs text-gray-600">·</span>
                      <span className="text-xs text-gray-500">
                        Updated {formatTimestamp(data.longTermUpdated)}
                      </span>
                    </>
                  )}
                </div>
              </div>
              <button
                onClick={editing ? () => setEditing(false) : startEdit}
                className={`flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-md transition-theme ${
                  editing
                    ? "text-gray-400 hover:text-gray-200 hover:bg-gray-800/50"
                    : "text-purple-400 hover:text-purple-300 hover:bg-purple-500/10"
                }`}
              >
                {editing ? (
                  <>
                    <X className="w-3.5 h-3.5" />
                    Cancel
                  </>
                ) : (
                  <>
                    <Pencil className="w-3.5 h-3.5" />
                    Edit
                  </>
                )}
              </button>
            </div>

            {/* Edit mode */}
            {editing ? (
              <div className="space-y-3">
                <textarea
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                  className="w-full h-[60vh] bg-gray-900 border border-gray-800/60 rounded-lg p-4 text-sm text-gray-200 font-mono leading-relaxed resize-none focus:outline-none focus:border-purple-500/40 focus:ring-1 focus:ring-purple-500/20"
                  spellCheck={false}
                />
                <button
                  onClick={saveEdit}
                  disabled={saving}
                  className="flex items-center gap-1.5 text-xs bg-purple-600 hover:bg-purple-500 text-white px-3 py-1.5 rounded-md transition-theme disabled:opacity-50"
                >
                  <Save className="w-3.5 h-3.5" />
                  {saving ? "Saving…" : "Save changes"}
                </button>
              </div>
            ) : (
              /* Long-term content */
              <div
                className="prose-sm"
                dangerouslySetInnerHTML={{
                  __html: renderMarkdown(data.longTerm || "*No long-term memory yet.*"),
                }}
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// Simple word counter for sidebar display
function countWordsSimple(text: string): number {
  return text.trim().split(/\s+/).filter(Boolean).length;
}
