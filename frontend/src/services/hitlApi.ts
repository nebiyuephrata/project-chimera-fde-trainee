import type { HitlTask } from "../types/hitl";

export async function fetchHitlQueue(): Promise<HitlTask[]> {
  const response = await fetch("/api/hitl.json");
  if (!response.ok) {
    throw new Error("Failed to fetch HITL queue");
  }
  const data = (await response.json()) as { tasks: HitlTask[] };
  return data.tasks;
}
