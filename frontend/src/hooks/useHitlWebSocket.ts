import { useCallback, useEffect, useRef, useState } from "react";
import toast from "react-hot-toast";
import type { HitlWsMessage } from "../types/hitl";
import { useHitlStore } from "../context/hitlStore";

const BASE_DELAY = 500;
const MAX_DELAY = 8_000;

export function useHitlWebSocket(url: string) {
  const [status, setStatus] = useState<"connecting" | "open" | "closed" | "error">(
    "connecting"
  );
  const socketRef = useRef<WebSocket | null>(null);
  const attemptsRef = useRef(0);
  const addTask = useHitlStore((state) => state.addTask);
  const updateTask = useHitlStore((state) => state.updateTask);

  const connect = useCallback(() => {
    setStatus("connecting");
    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.onopen = () => {
      attemptsRef.current = 0;
      setStatus("open");
    };

    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data) as HitlWsMessage;
        if (message.type === "task.new") {
          addTask(message.payload);
          toast("New HITL task received");
        }
        if (message.type === "task.update") {
          updateTask(message.payload);
        }
      } catch {
        // ignore malformed payloads
      }
    };

    socket.onerror = () => {
      setStatus("error");
      socket.close();
    };

    socket.onclose = () => {
      setStatus("closed");
      attemptsRef.current += 1;
      const delay = Math.min(BASE_DELAY * 2 ** attemptsRef.current, MAX_DELAY);
      window.setTimeout(connect, delay);
    };
  }, [addTask, updateTask, url]);

  useEffect(() => {
    connect();
    return () => socketRef.current?.close();
  }, [connect]);

  return { status, reconnect: connect };
}
