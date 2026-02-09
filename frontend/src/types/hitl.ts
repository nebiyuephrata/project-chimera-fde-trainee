export type HitlTaskStatus = "pending" | "approved" | "rejected" | "editing";

export interface HitlTask {
  task_id: string;
  snippet: string;
  confidence: number;
  reason: string;
  timestamp: string;
  status: HitlTaskStatus;
}

export interface HitlWsMessage {
  type: "task.new" | "task.update";
  payload: HitlTask;
}
