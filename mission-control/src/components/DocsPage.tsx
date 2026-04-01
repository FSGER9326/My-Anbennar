"use client";

import { useState, useEffect, useCallback, useMemo } from "react";
import {
  Search,
  FileText,
  File,
  Code2,
  FileCode,
  ChevronDown,
  ChevronRight,
  X,
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  Edit3,
  Save,
  XCircle,
  Loader2,
} from "lucide-react";

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

interface CategoryInfo {
  name: string;
  count: number;
  color: string;
}

interface DocsResponse {
  docs: DocEntry[];
  categories: CategoryInfo[];
  stats: {
    totalDocs: number;
    totalSize: string;
    lastUpdated: string;
  };
}

type SortField = "name" | "date" | "size";
type SortDir = "asc" | "desc";

const CATEGORY_LABELS: Record<string, string> = {
  modding: "Modding",
  memory: "Memory",
  learnings: "Learnings",
  skills: "Skills",
  docs: "Docs",
  config: "Config",
};

function FileIcon({ type }: { type: string }) {
  switch (type) {
    case "markdown":
      return <FileText className="w-4 h-4 text-blue-400" />;
    case "text":
      return <File className="w-4 h-4 text-gray-400" />;
    case "yaml":
    case "json":
      return <Code2 className="w-4 h-4 text-green-400" />;
    case "html":
      return <FileCode className="w-4 h-4 text-orange-400" />;
    default:
      return <File className="w-4 h-4 text-gray-400" />;
  }
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function relativeTime(dateStr: string): string {
  const now = Date.now();
  const then = new Date(dateStr).getTime();
  const diffMs = now - then;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return "just now";
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 30) return `${diffDays}d ago`;
  return new Date(dateStr).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

// ── Simple markdown-to-HTML for preview ──────────────────────────────
function renderMarkdown(text: string): string {
  let html = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Code blocks
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
    return `<pre class="bg-gray-800 rounded p-3 my-3 text-sm overflow-x-auto"><code class="text-gray-300">${code.trim()}</code></pre>`;
  });

  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code class="bg-gray-800 px-1 py-0.5 rounded text-purple-300 text-sm">$1</code>');

  // Headers
  html = html.replace(/^### (.+)$/gm, '<h3 class="text-base font-semibold mt-5 mb-2 text-gray-200">$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2 class="text-lg font-bold mt-6 mb-2 text-gray-100">$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1 class="text-xl font-bold mt-4 mb-3 text-gray-100">$1</h1>');

  // Bold & italic
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-purple-400 hover:underline">$1</a>');

  // Unordered lists
  html = html.replace(/^- (.+)$/gm, '<li class="ml-4 list-disc text-gray-300">$1</li>');
  html = html.replace(/(<li[^>]*>.*<\/li>\n?)+/g, '<ul class="my-2 space-y-1">$&</ul>');

  // Paragraphs
  html = html.replace(/\n\n/g, '</p><p class="text-gray-300 my-2">');

  return `<p class="text-gray-300 my-2">${html}</p>`;
}

export default function DocsPage() {
  const [docs, setDocs] = useState<DocEntry[]>([]);
  const [categories, setCategories] = useState<CategoryInfo[]>([]);
  const [stats, setStats] = useState({ totalDocs: 0, totalSize: "", lastUpdated: "" });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [search, setSearch] = useState("");
  const [activeCategory, setActiveCategory] = useState("all");
  const [sortField, setSortField] = useState<SortField>("date");
  const [sortDir, setSortDir] = useState<SortDir>("desc");
  const [collapsed, setCollapsed] = useState<Set<string>>(new Set());

  // Modal state
  const [selectedDoc, setSelectedDoc] = useState<DocEntry | null>(null);
  const [fullContent, setFullContent] = useState("");
  const [modalLoading, setModalLoading] = useState(false);
  const [editing, setEditing] = useState(false);
  const [editContent, setEditContent] = useState("");
  const [saving, setSaving] = useState(false);

  // Fetch docs
  const fetchDocs = useCallback(async () => {
    try {
      setLoading(true);
      const res = await fetch("/api/docs");
      if (!res.ok) throw new Error("Failed to fetch");
      const data: DocsResponse = await res.json();
      setDocs(data.docs);
      setCategories(data.categories);
      setStats(data.stats);
    } catch (e) {
      setError("Failed to load documents");
      console.error(e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDocs();
  }, [fetchDocs]);

  // Filter & sort
  const filtered = useMemo(() => {
    let result = docs;

    // Category filter
    if (activeCategory !== "all") {
      result = result.filter((d) => d.category === activeCategory);
    }

    // Search filter
    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(
        (d) =>
          d.name.toLowerCase().includes(q) ||
          d.path.toLowerCase().includes(q) ||
          d.preview.toLowerCase().includes(q)
      );
    }

    // Sort
    result = [...result].sort((a, b) => {
      let cmp = 0;
      switch (sortField) {
        case "name":
          cmp = a.name.localeCompare(b.name);
          break;
        case "date":
          cmp = a.lastModified.localeCompare(b.lastModified);
          break;
        case "size":
          cmp = a.size - b.size;
          break;
      }
      return sortDir === "asc" ? cmp : -cmp;
    });

    return result;
  }, [docs, activeCategory, search, sortField, sortDir]);

  // Group by folder
  const grouped = useMemo(() => {
    const groups = new Map<string, DocEntry[]>();
    for (const doc of filtered) {
      const folder = doc.folder;
      if (!groups.has(folder)) groups.set(folder, []);
      groups.get(folder)!.push(doc);
    }
    return groups;
  }, [filtered]);

  // Toggle sort
  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortField(field);
      setSortDir(field === "name" ? "asc" : "desc");
    }
  };

  // Toggle collapse
  const toggleCollapse = (folder: string) => {
    setCollapsed((prev) => {
      const next = new Set(prev);
      if (next.has(folder)) next.delete(folder);
      else next.add(folder);
      return next;
    });
  };

  // Open doc modal
  const openDoc = async (doc: DocEntry) => {
    setSelectedDoc(doc);
    setModalLoading(true);
    setEditing(false);
    try {
      // We'll fetch via the content from preview for now; the PUT endpoint can save
      // For full content, fetch the raw file from the workspace
      const res = await fetch(`/api/docs?file=${encodeURIComponent(doc.path)}`);
      // If the API doesn't support single-file, we'll use the preview
      if (res.ok) {
        const data = await res.json();
        setFullContent(data.content || doc.preview);
      } else {
        setFullContent(doc.preview);
      }
    } catch {
      setFullContent(doc.preview);
    } finally {
      setModalLoading(false);
    }
  };

  // Save edited doc
  const saveDoc = async () => {
    if (!selectedDoc) return;
    setSaving(true);
    try {
      const res = await fetch("/api/docs", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path: selectedDoc.path, content: editContent }),
      });
      if (res.ok) {
        setFullContent(editContent);
        setEditing(false);
        fetchDocs(); // Refresh
      }
    } catch {
      console.error("Save failed");
    } finally {
      setSaving(false);
    }
  };

  const startEdit = () => {
    setEditContent(fullContent);
    setEditing(true);
  };

  // Sort indicator helper
  const SortIcon = ({ field }: { field: SortField }) => {
    if (sortField !== field) return <ArrowUpDown className="w-3 h-3 opacity-30" />;
    return sortDir === "asc" ? (
      <ArrowUp className="w-3 h-3 text-purple-400" />
    ) : (
      <ArrowDown className="w-3 h-3 text-purple-400" />
    );
  };

  return (
    <div className="h-full flex flex-col">
      {/* ── Header ─────────────────────────────────────────── */}
      <div className="px-6 pt-5 pb-4 border-b border-gray-800/40">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-xl">📁</span>
          <h1 className="text-lg font-semibold text-gray-100">Documents</h1>
          <span className="text-xs bg-gray-800 text-gray-400 px-2 py-0.5 rounded-full">
            {stats.totalDocs} files
          </span>
          <span className="text-xs text-gray-600 ml-auto">
            {stats.totalSize} total · Updated {relativeTime(stats.lastUpdated)}
          </span>
        </div>

        {/* Search */}
        <div className="relative mb-3">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search documents by name, path, or content..."
            className="w-full bg-gray-900 border border-gray-700/50 rounded-lg pl-9 pr-9 py-2 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/20 transition"
          />
          {search && (
            <button
              onClick={() => setSearch("")}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Category filters */}
        <div className="flex items-center gap-1.5 flex-wrap">
          <button
            onClick={() => setActiveCategory("all")}
            className={`px-2.5 py-1 rounded-md text-xs font-medium transition ${
              activeCategory === "all"
                ? "bg-purple-500/15 text-purple-400 border border-purple-500/30"
                : "text-gray-400 hover:text-gray-200 border border-transparent hover:border-gray-700/50"
            }`}
          >
            All
          </button>
          {categories.map((cat) => (
            <button
              key={cat.name}
              onClick={() => setActiveCategory(cat.name)}
              className={`px-2.5 py-1 rounded-md text-xs font-medium transition ${
                activeCategory === cat.name
                  ? "border"
                  : "text-gray-400 hover:text-gray-200 border border-transparent hover:border-gray-700/50"
              }`}
              style={
                activeCategory === cat.name
                  ? {
                      backgroundColor: cat.color + "18",
                      color: cat.color,
                      borderColor: cat.color + "40",
                    }
                  : undefined
              }
            >
              {CATEGORY_LABELS[cat.name] || cat.name}
              <span className="ml-1 opacity-60">{cat.count}</span>
            </button>
          ))}
        </div>

        {/* Sort options */}
        <div className="flex items-center gap-2 mt-3 pt-3 border-t border-gray-800/30">
          <span className="text-[11px] text-gray-500 uppercase tracking-wider">Sort:</span>
          {([
            ["name", "Name"],
            ["date", "Date"],
            ["size", "Size"],
          ] as [SortField, string][]).map(([field, label]) => (
            <button
              key={field}
              onClick={() => handleSort(field)}
              className={`flex items-center gap-1 px-2 py-0.5 rounded text-xs transition ${
                sortField === field
                  ? "text-purple-400 bg-purple-500/10"
                  : "text-gray-500 hover:text-gray-300"
              }`}
            >
              {label}
              <SortIcon field={field} />
            </button>
          ))}
          <span className="text-[11px] text-gray-600 ml-auto">
            {search
              ? `${filtered.length} of ${docs.length} documents`
              : ""}
          </span>
        </div>
      </div>

      {/* ── Content ────────────────────────────────────────── */}
      <div className="flex-1 overflow-auto">
        {loading ? (
          <div className="flex items-center justify-center h-48">
            <Loader2 className="w-6 h-6 text-purple-400 animate-spin" />
          </div>
        ) : error ? (
          <div className="flex items-center justify-center h-48 text-gray-500">
            {error}
          </div>
        ) : filtered.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-48 text-gray-500">
            <FileText className="w-8 h-8 mb-2 opacity-30" />
            <span className="text-sm">No documents found</span>
            {search && (
              <button
                onClick={() => setSearch("")}
                className="text-xs text-purple-400 mt-1 hover:underline"
              >
                Clear search
              </button>
            )}
          </div>
        ) : (
          <div className="py-2">
            {Array.from(grouped.entries()).map(([folder, folderDocs]) => {
              const isCollapsed = collapsed.has(folder);
              return (
                <div key={folder} className="mb-1">
                  {/* Folder header */}
                  <button
                    onClick={() => toggleCollapse(folder)}
                    className="flex items-center gap-2 px-4 py-1.5 w-full text-left hover:bg-gray-800/20 transition"
                  >
                    {isCollapsed ? (
                      <ChevronRight className="w-3.5 h-3.5 text-gray-500" />
                    ) : (
                      <ChevronDown className="w-3.5 h-3.5 text-gray-500" />
                    )}
                    <span className="text-xs font-semibold text-gray-400 tracking-wide">
                      {folder}/
                    </span>
                    <span className="text-[10px] text-gray-600">
                      ({folderDocs.length} {folderDocs.length === 1 ? "file" : "files"})
                    </span>
                  </button>

                  {/* Doc rows */}
                  {!isCollapsed && (
                    <div>
                      {folderDocs.map((doc, i) => (
                        <button
                          key={doc.path}
                          onClick={() => openDoc(doc)}
                          className="w-full text-left px-4 py-2.5 flex items-center gap-3 border-b border-gray-800/40 hover:bg-gray-800/50 transition group"
                          style={{
                            backgroundColor: i % 2 === 0 ? "transparent" : "rgba(17,24,39,0.3)",
                          }}
                        >
                          <FileIcon type={doc.type} />
                          <span className="text-sm text-gray-200 font-medium min-w-[140px] group-hover:text-purple-300 transition">
                            {doc.name}
                          </span>
                          <span
                            className="text-[10px] px-1.5 py-0.5 rounded-full font-medium"
                            style={{
                              backgroundColor: (categories.find((c) => c.name === doc.category)?.color || "#6b7280") + "18",
                              color: categories.find((c) => c.name === doc.category)?.color || "#6b7280",
                            }}
                          >
                            {CATEGORY_LABELS[doc.category] || doc.category}
                          </span>
                          <span className="text-[11px] text-gray-600 min-w-[100px]">
                            {doc.path}
                          </span>
                          <span className="text-[11px] text-gray-500 ml-auto mr-4">
                            {formatSize(doc.size)}
                          </span>
                          <span className="text-[11px] text-gray-500 w-20 text-right">
                            {relativeTime(doc.lastModified)}
                          </span>
                        </button>
                      ))}
                      {/* Preview row for each doc */}
                      {folderDocs.map((doc) => (
                        <div
                          key={`preview-${doc.path}`}
                          className="px-4 py-1.5 border-b border-gray-800/20 text-[11px] text-gray-500 truncate"
                          style={{ paddingLeft: "44px" }}
                        >
                          {doc.preview}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* ── Modal ──────────────────────────────────────────── */}
      {selectedDoc && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="bg-gray-900 border border-gray-700/60 rounded-xl w-full max-w-3xl max-h-[85vh] flex flex-col shadow-2xl">
            {/* Modal header */}
            <div className="flex items-center gap-3 px-5 py-3.5 border-b border-gray-800/60">
              <FileIcon type={selectedDoc.type} />
              <div className="flex-1 min-w-0">
                <div className="text-sm font-semibold text-gray-100 truncate">
                  {selectedDoc.name}
                </div>
                <div className="text-[11px] text-gray-500 truncate">
                  {selectedDoc.path}
                </div>
              </div>
              <span className="text-[11px] text-gray-500 mr-2">
                {formatSize(selectedDoc.size)} · {relativeTime(selectedDoc.lastModified)}
              </span>
              <button
                onClick={() => {
                  setSelectedDoc(null);
                  setEditing(false);
                }}
                className="text-gray-500 hover:text-gray-300 transition p-1"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Modal body */}
            <div className="flex-1 overflow-auto p-5">
              {modalLoading ? (
                <div className="flex items-center justify-center h-32">
                  <Loader2 className="w-5 h-5 text-purple-400 animate-spin" />
                </div>
              ) : editing ? (
                <textarea
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                  className="w-full h-96 bg-gray-950 border border-gray-700/50 rounded-lg p-4 text-sm text-gray-200 font-mono resize-y focus:outline-none focus:border-purple-500/50"
                  spellCheck={false}
                />
              ) : (
                <div
                  className="prose prose-invert prose-sm max-w-none"
                  dangerouslySetInnerHTML={{ __html: renderMarkdown(fullContent) }}
                />
              )}
            </div>

            {/* Modal footer */}
            <div className="flex items-center justify-between px-5 py-3 border-t border-gray-800/60">
              <span className="text-[11px] text-gray-600">
                {editing ? "Editing mode" : "Click to preview · Markdown rendered"}
              </span>
              <div className="flex items-center gap-2">
                {editing ? (
                  <>
                    <button
                      onClick={() => setEditing(false)}
                      className="flex items-center gap-1 px-3 py-1.5 rounded-md text-xs text-gray-400 hover:text-gray-200 bg-gray-800 hover:bg-gray-700 transition"
                    >
                      <XCircle className="w-3.5 h-3.5" />
                      Cancel
                    </button>
                    <button
                      onClick={saveDoc}
                      disabled={saving}
                      className="flex items-center gap-1 px-3 py-1.5 rounded-md text-xs text-white bg-purple-600 hover:bg-purple-500 transition disabled:opacity-50"
                    >
                      {saving ? (
                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      ) : (
                        <Save className="w-3.5 h-3.5" />
                      )}
                      Save
                    </button>
                  </>
                ) : (
                  <button
                    onClick={startEdit}
                    className="flex items-center gap-1 px-3 py-1.5 rounded-md text-xs text-gray-400 hover:text-gray-200 bg-gray-800 hover:bg-gray-700 transition"
                  >
                    <Edit3 className="w-3.5 h-3.5" />
                    Edit
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
