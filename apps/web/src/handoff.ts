export interface HandoffClient {
  start(): Promise<string>;
  exchange(code: string, state: string): Promise<string>;
}

function objectValue(value: unknown): Record<string, unknown> | null {
  return typeof value === "object" && value !== null ? (value as Record<string, unknown>) : null;
}

export class HttpHandoffClient implements HandoffClient {
  constructor(private readonly apiBaseUrl = "/api/v1") {}

  async start(): Promise<string> {
    const response = await fetch(`${this.apiBaseUrl}/auth/handoff/start`, {
      method: "POST",
      cache: "no-store",
      credentials: "same-origin",
      redirect: "error",
    });
    const payload = objectValue(await response.json().catch(() => null));
    if (!response.ok || typeof payload?.authorization_url !== "string") {
      throw new Error("handoff start unavailable");
    }
    const destination = new URL(payload.authorization_url);
    if (!["http:", "https:"].includes(destination.protocol)) {
      throw new Error("handoff destination invalid");
    }
    return destination.toString();
  }

  async exchange(code: string, state: string): Promise<string> {
    const response = await fetch(`${this.apiBaseUrl}/auth/handoff/exchange`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, state }),
      cache: "no-store",
      credentials: "same-origin",
      redirect: "error",
    });
    const payload = objectValue(await response.json().catch(() => null));
    if (
      !response.ok ||
      payload?.token_type !== "Bearer" ||
      typeof payload.access_token !== "string"
    ) {
      throw new Error("handoff exchange unavailable");
    }
    return payload.access_token;
  }
}
