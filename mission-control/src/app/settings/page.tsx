"use client";

import { useState } from "react";
import { Settings, RefreshCw } from "lucide-react";

export default function SettingsPage() {
  const [autoRefresh, setAutoRefresh] = useState(30);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="p-6 max-w-xl">
      <div className="mb-6">
        <h1 className="text-lg font-semibold text-gray-100">Settings</h1>
        <p className="text-xs text-gray-500 mt-0.5">Configure Mission Control</p>
      </div>

      <div className="space-y-6">
        {/* Refresh interval */}
        <section className="bg-gray-900/60 border border-gray-800/60 rounded-xl p-4">
          <h2 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3 flex items-center gap-1.5">
            <RefreshCw className="w-3.5 h-3.5" /> Auto-refresh
          </h2>
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-300">Poll interval</span>
            <select
              value={autoRefresh}
              onChange={(e) => setAutoRefresh(Number(e.target.value))}
              className="bg-gray-950 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-100 focus:outline-none focus:border-purple-500/50"
            >
              <option value={15}>15 seconds</option>
              <option value={30}>30 seconds</option>
              <option value={60}>1 minute</option>
              <option value={300}>5 minutes</option>
            </select>
          </div>
          <p className="text-[11px] text-gray-600 mt-2">
            Components poll their API routes at this interval. Lower = more responsive, higher = less resource usage.
          </p>
        </section>

        {/* Workspace info */}
        <section className="bg-gray-900/60 border border-gray-800/60 rounded-xl p-4">
          <h2 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3 flex items-center gap-1.5">
            <Settings className="w-3.5 h-3.5" /> Workspace
          </h2>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-gray-500">Path</span>
              <span className="text-gray-300 font-mono text-[11px]">C:\Users\User\.openclaw\workspace</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Mod Repo</span>
              <span className="text-gray-300 font-mono text-[11px]">C:\Users\User\Documents\GitHub\My-Anbennar</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Branch</span>
              <span className="text-gray-300 font-mono">chore/workflow-automation-pass</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Task DB</span>
              <span className="text-gray-300 font-mono text-[11px]">data/tasks.json</span>
            </div>
          </div>
        </section>

        {/* About */}
        <section className="bg-gray-900/60 border border-gray-800/60 rounded-xl p-4">
          <h2 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">
            About
          </h2>
          <div className="space-y-1.5 text-xs text-gray-500">
            <p>Verne Mission Control v0.1.0</p>
            <p>Next.js 16 + TypeScript + Tailwind CSS</p>
            <p>Agent: Jordan (openrouter/xiaomi/mimo-v2-omni)</p>
            <p>Built for Verne Anbennar EU4 mod development</p>
          </div>
        </section>
      </div>
    </div>
  );
}
