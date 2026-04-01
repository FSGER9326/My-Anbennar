"use client";

import { useEffect, useState } from "react";
import {
  ChevronRight,
  ChevronDown,
  MessageSquare,
  Plus,
  CheckCircle2,
  Circle,
  Pause,
  Play,
  TrendingUp,
} from "lucide-react";

interface Milestone {
  name: string;
  done: boolean;
}

interface Project {
  id: string;
  name: string;
  description: string;
  status: string;
  progress: number;
  color: string;
  lastUpdated: string;
  milestones: Milestone[];
  tasks: string[];
  planningNotes: string[];
}

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [planningMode, setPlanningMode] = useState<string | null>(null);
  const [newNote, setNewNote] = useState("");
  const [newProject, setNewProject] = useState(false);
  const [newProjectName, setNewProjectName] = useState("");

  useEffect(() => {
    fetch("/api/projects")
      .then((r) => r.json())
      .then((d) => setProjects(d.projects || []));
  }, []);

  const toggleExpand = (id: string) => {
    setExpanded(expanded === id ? null : id);
  };

  const addPlanningNote = async (projectId: string) => {
    if (!newNote.trim()) return;
    const project = projects.find((p) => p.id === projectId);
    if (!project) return;
    const updated = {
      ...project,
      planningNotes: [...project.planningNotes, newNote.trim()],
    };
    await fetch(`/api/projects/${projectId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updated),
    });
    setProjects(projects.map((p) => (p.id === projectId ? updated : p)));
    setNewNote("");
  };

  const createProject = async () => {
    if (!newProjectName.trim()) return;
    const res = await fetch("/api/projects", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newProjectName.trim() }),
    });
    const created = await res.json();
    setProjects([...projects, created]);
    setNewProject(false);
    setNewProjectName("");
  };

  const statusIcon = (status: string) => {
    switch (status) {
      case "active":
        return <Play className="w-3.5 h-3.5 text-green-400" />;
      case "planning":
        return <Circle className="w-3.5 h-3.5 text-yellow-400" />;
      case "paused":
        return <Pause className="w-3.5 h-3.5 text-gray-400" />;
      case "done":
        return <CheckCircle2 className="w-3.5 h-3.5 text-blue-400" />;
      default:
        return <Circle className="w-3.5 h-3.5 text-gray-500" />;
    }
  };

  const statusColor = (status: string) => {
    switch (status) {
      case "active":
        return "text-green-400 bg-green-400/10";
      case "planning":
        return "text-yellow-400 bg-yellow-400/10";
      case "paused":
        return "text-gray-400 bg-gray-400/10";
      case "done":
        return "text-blue-400 bg-blue-400/10";
      default:
        return "text-gray-500 bg-gray-500/10";
    }
  };

  return (
    <div className="flex-1 overflow-auto">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-800/60 flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-gray-100">Projects</h1>
          <p className="text-xs text-gray-500 mt-0.5">
            {projects.length} projects · {projects.filter((p) => p.status === "active").length} active
          </p>
        </div>
        <button
          onClick={() => setNewProject(true)}
          className="px-3 py-1.5 bg-purple-600 hover:bg-purple-700 text-white text-xs font-medium rounded-md transition-colors flex items-center gap-1.5"
        >
          <Plus className="w-3.5 h-3.5" />
          New Project
        </button>
      </div>

      {/* New Project Modal */}
      {newProject && (
        <div className="px-6 py-3 bg-gray-900/50 border-b border-gray-800/60 flex items-center gap-3">
          <input
            type="text"
            value={newProjectName}
            onChange={(e) => setNewProjectName(e.target.value)}
            placeholder="Project name..."
            className="flex-1 bg-gray-800 border border-gray-700 rounded-md px-3 py-1.5 text-sm text-gray-200 placeholder:text-gray-500 focus:outline-none focus:border-purple-500"
            onKeyDown={(e) => e.key === "Enter" && createProject()}
            autoFocus
          />
          <button
            onClick={createProject}
            className="px-3 py-1.5 bg-purple-600 hover:bg-purple-700 text-white text-xs font-medium rounded-md"
          >
            Create
          </button>
          <button
            onClick={() => setNewProject(false)}
            className="px-3 py-1.5 text-gray-400 text-xs hover:text-gray-300"
          >
            Cancel
          </button>
        </div>
      )}

      {/* Projects List */}
      <div className="p-6 space-y-2">
        {projects.map((project) => (
          <div
            key={project.id}
            className="bg-gray-900/50 border border-gray-800/60 rounded-lg overflow-hidden"
          >
            {/* Project Row */}
            <div
              className="px-4 py-3 flex items-center gap-3 cursor-pointer hover:bg-gray-800/30 transition-colors"
              onClick={() => toggleExpand(project.id)}
            >
              <div className="transition-transform">
                {expanded === project.id ? (
                  <ChevronDown className="w-4 h-4 text-gray-500" />
                ) : (
                  <ChevronRight className="w-4 h-4 text-gray-500" />
                )}
              </div>
              <div
                className="w-2 h-2 rounded-full shrink-0"
                style={{ backgroundColor: project.color }}
              />
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-gray-200 truncate">
                  {project.name}
                </div>
                <div className="text-xs text-gray-500 truncate">
                  {project.description}
                </div>
              </div>
              <span
                className={`px-2 py-0.5 text-[10px] font-medium rounded-full ${statusColor(
                  project.status
                )}`}
              >
                {project.status}
              </span>
              {/* Progress bar */}
              <div className="w-24 flex items-center gap-2">
                <div className="flex-1 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all"
                    style={{
                      width: `${project.progress}%`,
                      backgroundColor: project.color,
                    }}
                  />
                </div>
                <span className="text-[10px] text-gray-500 w-8 text-right">
                  {project.progress}%
                </span>
              </div>
            </div>

            {/* Expanded Detail */}
            {expanded === project.id && (
              <div className="border-t border-gray-800/60">
                {/* Milestones */}
                <div className="px-4 py-3">
                  <div className="text-xs font-medium text-gray-400 mb-2 flex items-center gap-1.5">
                    <TrendingUp className="w-3.5 h-3.5" />
                    Milestones
                  </div>
                  <div className="space-y-1.5">
                    {project.milestones.map((m, i) => (
                      <div
                        key={i}
                        className="flex items-center gap-2 text-xs"
                      >
                        {m.done ? (
                          <CheckCircle2 className="w-3.5 h-3.5 text-green-500 shrink-0" />
                        ) : (
                          <Circle className="w-3.5 h-3.5 text-gray-600 shrink-0" />
                        )}
                        <span
                          className={
                            m.done
                              ? "text-gray-500 line-through"
                              : "text-gray-300"
                          }
                        >
                          {m.name}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Planning Mode */}
                <div className="px-4 py-3 border-t border-gray-800/40">
                  <button
                    onClick={() =>
                      setPlanningMode(
                        planningMode === project.id ? null : project.id
                      )
                    }
                    className="flex items-center gap-1.5 text-xs font-medium text-purple-400 hover:text-purple-300 transition-colors"
                  >
                    <MessageSquare className="w-3.5 h-3.5" />
                    {planningMode === project.id
                      ? "Close Planning"
                      : "Planning Mode"}
                  </button>

                  {planningMode === project.id && (
                    <div className="mt-3 space-y-2">
                      {/* Existing notes */}
                      {project.planningNotes.map((note, i) => (
                        <div
                          key={i}
                          className="flex items-start gap-2 text-xs text-gray-300 bg-gray-800/50 rounded-md px-3 py-2"
                        >
                          <span className="text-purple-400 mt-0.5">•</span>
                          {note}
                        </div>
                      ))}

                      {/* New note input */}
                      <div className="flex gap-2">
                        <input
                          type="text"
                          value={newNote}
                          onChange={(e) => setNewNote(e.target.value)}
                          placeholder="Add planning note..."
                          className="flex-1 bg-gray-800 border border-gray-700 rounded-md px-3 py-1.5 text-xs text-gray-200 placeholder:text-gray-500 focus:outline-none focus:border-purple-500"
                          onKeyDown={(e) =>
                            e.key === "Enter" && addPlanningNote(project.id)
                          }
                        />
                        <button
                          onClick={() => addPlanningNote(project.id)}
                          className="px-2.5 py-1.5 bg-purple-600 hover:bg-purple-700 text-white text-xs font-medium rounded-md"
                        >
                          Add
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}

        {projects.length === 0 && (
          <div className="text-center py-12 text-gray-500 text-sm">
            No projects yet. Create one to get started.
          </div>
        )}
      </div>
    </div>
  );
}
