"use client";

import { useState } from "react";
import { MoreHorizontal, ArrowRight, ArrowLeft } from "lucide-react";

interface Task {
  id: string;
  title: string;
  description: string;
  status: "backlog" | "in-progress" | "review" | "done";
  priority: number;
  assignee: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

interface TaskCardProps {
  task: Task;
  onMove: (id: string, newStatus: Task["status"]) => void;
}

const priorityDot: Record<number, string> = {
  1: "bg-red-500",
  2: "bg-orange-500",
  3: "bg-yellow-500",
  4: "bg-blue-500",
  5: "bg-purple-500",
};

const assigneeDisplay: Record<string, { emoji: string; label: string }> = {
  jordan: { emoji: "🟣", label: "Jordan" },
  falk: { emoji: "🔵", label: "Falk" },
  "subagent-auto": { emoji: "🤖", label: "Auto" },
  "subagent-qa": { emoji: "🤖", label: "QA" },
  "subagent-audit": { emoji: "🤖", label: "Audit" },
  "subagent-wiki": { emoji: "🤖", label: "Wiki" },
  "subagent-inspire": { emoji: "🤖", label: "Inspire" },
  "subagent-sync": { emoji: "🤖", label: "Sync" },
  "subagent-bg": { emoji: "🤖", label: "BgWorker" },
};

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h`;
  const days = Math.floor(hours / 24);
  return `${days}d`;
}

const statusOrder: Task["status"][] = ["backlog", "in-progress", "review", "done"];

export default function TaskCard({ task, onMove }: TaskCardProps) {
  const [showMenu, setShowMenu] = useState(false);
  const assignee = assigneeDisplay[task.assignee] || { emoji: "🟣", label: task.assignee };
  const currentIdx = statusOrder.indexOf(task.status);

  return (
    <div className="group relative bg-gray-900/80 border border-gray-800/60 rounded-lg px-3 py-2.5 hover:border-gray-700 transition-all duration-150">
      {/* Priority dot + title */}
      <div className="flex items-start gap-2">
        <div
          className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${priorityDot[task.priority] || "bg-gray-600"}`}
        />
        <div className="min-w-0 flex-1">
          <div className="text-[13px] text-gray-200 font-medium leading-snug truncate">
            {task.title}
          </div>
        </div>

        {/* Quick action menu */}
        <div className="relative opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={() => setShowMenu(!showMenu)}
            className="p-0.5 text-gray-600 hover:text-gray-300"
          >
            <MoreHorizontal className="w-3.5 h-3.5" />
          </button>

          {showMenu && (
            <div className="absolute right-0 top-6 z-10 bg-gray-800 border border-gray-700 rounded-lg shadow-xl py-1 min-w-[120px]">
              {currentIdx > 0 && (
                <button
                  onClick={() => {
                    onMove(task.id, statusOrder[currentIdx - 1]);
                    setShowMenu(false);
                  }}
                  className="flex items-center gap-2 w-full px-3 py-1.5 text-xs text-gray-300 hover:bg-gray-700/50"
                >
                  <ArrowLeft className="w-3 h-3" />
                  Move left
                </button>
              )}
              {currentIdx < statusOrder.length - 1 && (
                <button
                  onClick={() => {
                    onMove(task.id, statusOrder[currentIdx + 1]);
                    setShowMenu(false);
                  }}
                  className="flex items-center gap-2 w-full px-3 py-1.5 text-xs text-gray-300 hover:bg-gray-700/50"
                >
                  <ArrowRight className="w-3 h-3" />
                  Move right
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Meta row */}
      <div className="flex items-center gap-2 mt-2 ml-4 flex-wrap">
        <span className="text-[10px] text-gray-500">
          {assignee.emoji} {assignee.label}
        </span>
        <span className="text-[10px] text-gray-600">·</span>
        <span className="text-[10px] text-gray-500">{timeAgo(task.updatedAt)} ago</span>
        {task.tags.slice(0, 2).map((tag) => (
          <span
            key={tag}
            className="text-[10px] px-1.5 py-0.5 rounded bg-gray-800 text-gray-500"
          >
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
}
