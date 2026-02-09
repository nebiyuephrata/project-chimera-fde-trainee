import type { HitlTask } from "../types/hitl";

export async function fetchHitlQueue(): Promise<HitlTask[]> {
  const response = await fetch("http://localhost:8000/hitl/tasks");
  if (!response.ok) {
    throw new Error("Failed to fetch HITL queue");
  }
  const data = (await response.json()) as { tasks: HitlTask[] };
  return data.tasks;
}

export async function updateHitlTask(
  taskId: string,
  action: "approve" | "reject" | "edit"
): Promise<HitlTask> {
  const response = await fetch(`http://localhost:8000/hitl/${taskId}/${action}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  if (!response.ok) {
    throw new Error("Failed to update HITL task");
  }
  const data = (await response.json()) as { task: HitlTask };
  return data.task;
}

export async function checkHitlHealth(): Promise<boolean> {
  const response = await fetch("http://localhost:8000/health");
  if (!response.ok) {
    return false;
  }
  const data = (await response.json()) as { status?: string };
  return data.status === "ok";
}
