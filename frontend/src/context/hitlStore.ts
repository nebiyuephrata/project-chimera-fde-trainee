import { create } from "zustand";
import type { HitlTask } from "../types/hitl";

export interface HitlState {
  tasks: HitlTask[];
  setTasks: (tasks: HitlTask[]) => void;
  addTask: (task: HitlTask) => void;
  updateTask: (task: HitlTask) => void;
  updateStatus: (taskId: string, status: HitlTask["status"]) => void;
}

export const useHitlStore = create<HitlState>((set) => ({
  tasks: [],
  setTasks: (tasks) => set({ tasks }),
  addTask: (task) =>
    set((state) => ({ tasks: [task, ...state.tasks] })),
  updateTask: (task) =>
    set((state) => ({
      tasks: state.tasks.map((item) => (item.task_id === task.task_id ? task : item)),
    })),
  updateStatus: (taskId, status) =>
    set((state) => ({
      tasks: state.tasks.map((item) =>
        item.task_id === taskId ? { ...item, status } : item
      ),
    })),
}));
