// Browser traffic always uses the same origin. Next.js proxies this path to the
// backend, avoiding CORS/third-party-cookie failures in production.
export const API_BASE = "/api/v1";

export class ApiError extends Error {
  constructor(message: string, public readonly status: number) {
    super(message);
    this.name = "ApiError";
  }
}

export async function apiFetch<T>(path: string, options: RequestInit & { signal?: AbortSignal } = {}): Promise<T> {
  const headers: Record<string, string> = {
    ...(options.body ? { "Content-Type": "application/json" } : {}),
    ...(options.headers as Record<string, string>),
  };

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    credentials: "include",
    headers,
  });
  if (!response.ok) {
    let message = `Yêu cầu thất bại (${response.status})`;
    try {
      const payload = (await response.json()) as { detail?: string };
      if (payload.detail) message = payload.detail;
    } catch {
      // Response is not JSON.
    }
    throw new ApiError(message, response.status);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

/**
 * Post to a Server-Sent Events endpoint and hand each event to `onEvent`.
 *
 * Written against fetch rather than EventSource because EventSource cannot send
 * a request body, headers, or credentials the way the chat endpoint needs.
 */
export async function apiStream(
  path: string,
  options: {
    body: unknown;
    headers?: Record<string, string>;
    signal?: AbortSignal;
    onEvent: (event: string, data: unknown) => void;
  },
): Promise<void> {
  const token = typeof window !== "undefined" ? localStorage.getItem("nera_auth_token") : null;
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    credentials: "include",
    signal: options.signal,
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
    body: JSON.stringify(options.body),
  });

  if (!response.ok || !response.body) {
    let message = `Yêu cầu thất bại (${response.status})`;
    try {
      const payload = (await response.json()) as { detail?: string };
      if (payload.detail) message = payload.detail;
    } catch {
      // Response is not JSON.
    }
    throw new ApiError(message, response.status);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    // SSE frames are separated by a blank line; keep any partial tail buffered.
    let boundary = buffer.indexOf("\n\n");
    while (boundary !== -1) {
      const frame = buffer.slice(0, boundary);
      buffer = buffer.slice(boundary + 2);
      let eventName = "message";
      const dataLines: string[] = [];
      for (const line of frame.split("\n")) {
        if (line.startsWith("event:")) eventName = line.slice(6).trim();
        else if (line.startsWith("data:")) dataLines.push(line.slice(5).trim());
      }
      if (dataLines.length > 0) {
        try {
          options.onEvent(eventName, JSON.parse(dataLines.join("\n")));
        } catch {
          // A frame we cannot parse is not worth failing the whole turn over.
        }
      }
      boundary = buffer.indexOf("\n\n");
    }
  }
}
