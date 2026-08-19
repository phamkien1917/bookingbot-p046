import { useState, useCallback, useRef } from "react";
import { apiFetch } from "@/lib/api";
import type { ChatMessage, SessionSummary, ChatResponse } from "@/components/chat/types";

export function useChatSession(initialGreeting: ChatMessage, propertyId: string | null, initialPrompt: string | null) {
  const [messages, setMessages] = useState<ChatMessage[]>([initialGreeting]);
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [sessionId, setSessionId] = useState(() => crypto.randomUUID());
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [insights, setInsights] = useState<Record<string, unknown>>({});
  const [memorySummary, setMemorySummary] = useState("");
  const [savedProperties, setSavedProperties] = useState<any[]>([]);

  const abortControllerRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(async (text: string, isFeedback = false) => {
    if (!text.trim()) return;
    
    // Abort previous request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    const newMessages = [...messages, { role: "user" as const, content: text }];
    if (!isFeedback) setInput("");
    setMessages(newMessages);
    setLoading(true);
    setError("");

    try {
      const data = await apiFetch<ChatResponse>("/chat", {
        method: "POST",
        body: JSON.stringify({
          session_id: sessionId,
          message: text,
          property_id: propertyId || undefined,
        }),
        signal: abortControllerRef.current.signal,
      });

      setSessionId(data.session_id);
      setMessages([...newMessages, {
        role: "assistant",
        content: data.response,
        properties: data.properties,
      }]);
      setInsights(data.insights || {});
      if (data.memory_summary) {
        setMemorySummary(data.memory_summary);
      }
    } catch (err: any) {
      if (err.name !== "AbortError") {
        setError(err.message || "Đã xảy ra lỗi");
      }
    } finally {
      setLoading(false);
    }
  }, [messages, sessionId, propertyId]);

  return {
    messages,
    setMessages,
    sessions,
    setSessions,
    sessionId,
    setSessionId,
    input,
    setInput,
    loading,
    error,
    insights,
    memorySummary,
    savedProperties,
    sendMessage,
    setInsights,
    setMemorySummary,
  };
}
