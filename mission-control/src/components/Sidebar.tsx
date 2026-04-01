"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useCallback } from "react";
import {
  LayoutDashboard,
  Bot,
  Users,
  BarChart3,
  CalendarDays,
  FolderKanban,
  Settings,
  Brain,
  FileText,
} from "lucide-react";

interface NavItem {
  id: string;
  href: string;
  label: string;
  icon: React.ElementType;
  children?: NavItem[];
}

const defaultNav: NavItem[] = [
  { id: "overview", href: "/", label: "Overview", icon: LayoutDashboard },
  { id: "memory", href: "/memory", label: "Memory", icon: Brain },
  { id: "docs", href: "/docs", label: "Documents", icon: FileText },
  { id: "projects", href: "/projects", label: "Projects", icon: FolderKanban },
  { id: "jordan", href: "/jordan", label: "Jordan", icon: Bot },
  { id: "subagents", href: "/subagents", label: "Subagents", icon: Users },
  { id: "stats", href: "/stats", label: "Stats", icon: BarChart3 },
  { id: "calendar", href: "/calendar", label: "Calendar", icon: CalendarDays },
  { id: "settings", href: "/settings", label: "Settings", icon: Settings },
];

const STORAGE_KEY = "mc-sidebar-order";

function loadOrder(): string[] {
  if (typeof window === "undefined") return defaultNav.map((n) => n.id);
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return JSON.parse(saved);
  } catch {}
  return defaultNav.map((n) => n.id);
}

function saveOrder(order: string[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(order));
}

export default function Sidebar() {
  const pathname = usePathname();
  const [order, setOrder] = useState<string[]>(loadOrder);
  const [dragId, setDragId] = useState<string | null>(null);
  const [dragOverId, setDragOverId] = useState<string | null>(null);

  // Build ordered nav from saved order
  const navMap = Object.fromEntries(defaultNav.map((n) => [n.id, n]));
  const nav = order.map((id) => navMap[id]).filter(Boolean);

  // Overview + main nav
  const overviewItem = nav.find((n) => n.id === "overview");
  const mainNav = nav.filter((n) => n.id !== "overview");

  const handleDragStart = useCallback((id: string) => {
    setDragId(id);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent, id: string) => {
    e.preventDefault();
    setDragOverId(id);
  }, []);

  const handleDrop = useCallback(
    (targetId: string) => {
      if (!dragId || dragId === targetId) {
        setDragId(null);
        setDragOverId(null);
        return;
      }
      const newOrder = [...order];
      const fromIdx = newOrder.indexOf(dragId);
      const toIdx = newOrder.indexOf(targetId);
      newOrder.splice(fromIdx, 1);
      newOrder.splice(toIdx, 0, dragId);
      setOrder(newOrder);
      saveOrder(newOrder);
      setDragId(null);
      setDragOverId(null);
    },
    [dragId, order]
  );

  const handleDragEnd = useCallback(() => {
    setDragId(null);
    setDragOverId(null);
  }, []);

  return (
    <aside className="w-56 bg-gray-900 border-r border-gray-800/60 flex flex-col shrink-0 select-none">
      {/* Logo */}
      <div className="px-4 py-4 border-b border-gray-800/60">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 bg-purple-600 rounded-lg flex items-center justify-center text-sm font-bold text-white">
            MC
          </div>
          <div>
            <div className="text-sm font-semibold text-gray-100 leading-tight">
              Mission Control
            </div>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-2 py-3 space-y-0.5 overflow-y-auto">
        {/* Overview */}
        {overviewItem && (
          <Link
            href={overviewItem.href}
            className={`flex items-center gap-2.5 px-2.5 py-1.5 rounded-md text-[13px] font-medium transition-theme ${
              pathname === "/"
                ? "bg-purple-500/10 text-purple-400"
                : "text-gray-400 hover:text-gray-200 hover:bg-gray-800/50"
            }`}
          >
            <overviewItem.icon className="w-4 h-4 opacity-70" />
            {overviewItem.label}
          </Link>
        )}

        {/* Separator */}
        <div className="h-px bg-gray-800/60 my-1.5 mx-2" />

        {/* Draggable main nav */}
        {mainNav.map((item) => (
          <div
            key={item.id}
            draggable
            onDragStart={() => handleDragStart(item.id)}
            onDragOver={(e) => handleDragOver(e, item.id)}
            onDrop={() => handleDrop(item.id)}
            onDragEnd={handleDragEnd}
            className={`flex items-center gap-2.5 px-2.5 py-1.5 rounded-md text-[13px] font-medium cursor-grab active:cursor-grabbing transition-all ${
              dragOverId === item.id
                ? "border-t-2 border-purple-500"
                : ""
            } ${
              dragId === item.id
                ? "opacity-40 scale-95"
                : ""
            } ${
              pathname.startsWith(item.href)
                ? "bg-purple-500/10 text-purple-400"
                : "text-gray-400 hover:text-gray-200 hover:bg-gray-800/50"
            }`}
            title="Drag to reorder"
          >
            <Link href={item.href} className="flex items-center gap-2.5 flex-1 no-underline">
              <item.icon className="w-4 h-4 opacity-70" />
              {item.label}
            </Link>
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div className="px-4 py-3 border-t border-gray-800/60">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-full bg-purple-600 flex items-center justify-center text-[10px] font-bold text-white">
            J
          </div>
          <div className="min-w-0">
            <div className="text-xs text-gray-300 font-medium truncate">Jordan</div>
            <div className="text-[10px] text-gray-500">active</div>
          </div>
          <div className="ml-auto w-2 h-2 rounded-full bg-green-500 animate-pulse" />
        </div>
      </div>
    </aside>
  );
}
