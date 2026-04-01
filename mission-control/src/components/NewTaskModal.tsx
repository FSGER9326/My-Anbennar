"use client";

import { useState } from "react";
import { X, Plus } from "lucide-react";

interface NewTaskModalProps {
  open: boolean;
  onClose: () => void;
  onCreated: () => void;
}

export default function NewTaskModal({ open, onClose, onCreated }: NewTaskModalProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState(3);
  const [assignee, setAssignee] = useState("jordan");
  const [tags, setTags] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    setSubmitting(true);

    try {
      await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim(),
          priority,
          assignee,
          tags: tags
            .split(",")
            .map((t) => t.trim())
            .filter(Boolean),
        }),
      });
      setTitle("");
      setDescription("");
      setPriority(3);
      setAssignee("jordan");
      setTags("");
      onCreated();
      onClose();
    } finally {
      setSubmitting(false);
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <form
        onSubmit={handleSubmit}
        className="relative w-full max-w-md bg-gray-900 border border-gray-700 rounded-xl shadow-2xl p-5 mx-4"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-gray-100">New Task</h3>
          <button
            type="button"
            onClick={onClose}
            className="text-gray-500 hover:text-gray-300 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="space-y-3">
          {/* Title */}
          <div>
            <input
              type="text"
              placeholder="Task title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-100 placeholder:text-gray-600 focus:outline-none focus:border-purple-500/50 transition-colors"
              autoFocus
              required
            />
          </div>

          {/* Description */}
          <div>
            <textarea
              placeholder="Description (optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-100 placeholder:text-gray-600 focus:outline-none focus:border-purple-500/50 transition-colors resize-none"
            />
          </div>

          {/* Priority + Assignee row */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-[10px] uppercase text-gray-500 mb-1">Priority</label>
              <select
                value={priority}
                onChange={(e) => setPriority(Number(e.target.value))}
                className="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-100 focus:outline-none focus:border-purple-500/50"
              >
                <option value={1}>P1 — Critical</option>
                <option value={2}>P2 — High</option>
                <option value={3}>P3 — Medium</option>
                <option value={4}>P4 — Low</option>
                <option value={5}>P5 — Backlog</option>
              </select>
            </div>

            <div>
              <label className="block text-[10px] uppercase text-gray-500 mb-1">Assignee</label>
              <select
                value={assignee}
                onChange={(e) => setAssignee(e.target.value)}
                className="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-100 focus:outline-none focus:border-purple-500/50"
              >
                <option value="jordan">🟣 Jordan</option>
                <option value="falk">🔵 Falk</option>
                <option value="subagent-auto">🤖 Auto (subagent)</option>
              </select>
            </div>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-[10px] uppercase text-gray-500 mb-1">Tags</label>
            <input
              type="text"
              placeholder="modding, config, skill"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              className="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-100 placeholder:text-gray-600 focus:outline-none focus:border-purple-500/50 transition-colors"
            />
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-2 mt-4">
          <button
            type="button"
            onClick={onClose}
            className="px-3 py-1.5 text-sm text-gray-400 hover:text-gray-200 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting || !title.trim()}
            className="flex items-center gap-1.5 px-4 py-1.5 bg-purple-600 hover:bg-purple-700 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors"
          >
            <Plus className="w-3.5 h-3.5" />
            {submitting ? "Creating..." : "Create Task"}
          </button>
        </div>
      </form>
    </div>
  );
}
