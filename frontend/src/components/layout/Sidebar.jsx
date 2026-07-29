// frontend/src/components/layout/Sidebar.jsx

import { NavLink, useNavigate } from "react-router-dom";
import { LayoutDashboard, FlaskConical, GitCompare, History, Boxes, Cpu, Sparkles, LogOut, Brain } from "lucide-react";
import toast from "react-hot-toast";
import useAuthStore from "../../store/authStore";
import { inferenceApi } from "../../api/inferenceApi";
import { useQuery } from "@tanstack/react-query";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Overview", icon: LayoutDashboard, enabled: true },
  { to: "/studio", label: "Studio", icon: FlaskConical, enabled: true },
  { to: "/compare", label: "Compare", icon: GitCompare, enabled: true },
  { to: "/history", label: "History", icon: History, enabled: true },  
];

const LIBRARY_ITEMS = [
  { to: "/library/machine_learning", label: "Machine Learning", icon: Boxes },
  { to: "/library/deep_learning", label: "Deep Learning", icon: Cpu },
  { to: "/library/generative_ai", label: "Generative AI", icon: Sparkles },
];



export default function Sidebar() {


  const { data: inferenceTasks } = useQuery({
    queryKey: ["inference", "tasks"],
    queryFn: inferenceApi.listTasks,
    staleTime: Infinity,   // never re-fetch — task list doesn't change at runtime
  });

  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    toast.success("Logged out successfully");
    navigate("/login");
  };

  const linkClass = ({ isActive }) =>
    `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors cursor-pointer
    ${isActive ? "bg-surface-hover text-ink" : "text-muted hover:text-ink hover:bg-surface-hover"}`;

  return (
    <aside className="w-56 shrink-0 h-screen sticky top-0 bg-surface border-r border-line flex flex-col">
      <div className="px-5 py-5">
        <h1 className="text-ink font-semibold tracking-tight">MLab</h1>
      </div>

      <nav className="flex-1 px-3 flex flex-col gap-0.5 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          if (!item.enabled) {
            return (
              <div key={item.label} title="Coming soon"
                className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-faint cursor-not-allowed">
                <Icon size={16} />
                {item.label}
              </div>
            );
          }
          return (
            <NavLink key={item.to} to={item.to} className={linkClass}>
              <Icon size={16} />
              {item.label}
            </NavLink>
          );
        })}

        <p className="px-3 pt-5 pb-1 text-[11px] text-faint uppercase tracking-wide">Library</p>
        {LIBRARY_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink key={item.to} to={item.to} className={linkClass}>
              <Icon size={16} />
              {item.label}
            </NavLink>
          );
        })}
      </nav>

      {inferenceTasks && inferenceTasks.length > 0 && (
        <>
          <p className="px-3 pt-5 pb-1 text-[11px] text-faint uppercase tracking-wide">Inference</p>
          {inferenceTasks.map((task) => (
            <NavLink key={task.name} to={`/infer/${task.name}`} className={linkClass}>
              <Brain size={16} />
              {task.display_name}
            </NavLink>
          ))}
        </>
      )}


      <div className="px-3 py-4 border-t border-line">
        <div className="px-3 py-2">
          <p className="text-sm text-ink truncate">{user?.username}</p>
          <p className="text-xs text-faint truncate">{user?.email}</p>
        </div>
        <button onClick={handleLogout}
          className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-muted
            hover:text-ink hover:bg-surface-hover transition-colors cursor-pointer">
          <LogOut size={16} />
          Logout
        </button>
      </div>
    </aside>
  );
}