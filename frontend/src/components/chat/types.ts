import type { Property } from "@/lib/types";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  properties?: Property[];
  quickReplies?: string[];
  authRequired?: boolean;
  aiMode?: string;
  aiModel?: string | null;
  aiLatencyMs?: number;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  properties: Property[];
  insights: Record<string, unknown>;
  suggested_actions?: string[];
  memory_summary?: string;
  auth_required?: boolean;
  ai_mode: string;
  ai_model?: string | null;
  ai_latency_ms: number;
}

export interface SessionSummary {
  session_id: string;
  preview: string;
  message_count: number;
  last_active: string;
}

export interface SessionDetail {
  messages: Array<{ role: string; content: string; properties?: Property[]; ai_mode?: string; ai_model?: string | null }>;
}
