import type { Property } from "@/lib/types";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  properties?: Property[];
  quickReplies?: string[];
}

export interface ChatResponse {
  response: string;
  session_id: string;
  properties: Property[];
  insights: Record<string, unknown>;
  memory_summary?: string;
}

export interface SessionSummary {
  session_id: string;
  preview: string;
  message_count: number;
  last_active: string;
}

export interface SessionDetail {
  messages: Array<{ role: string; content: string; properties?: Property[] }>;
}
