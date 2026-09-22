// @vitest-environment jsdom

import { afterEach, describe, expect, it, vi } from "vitest";
import { HttpHandoffClient } from "./handoff";

afterEach(() => vi.unstubAllGlobals());

describe("HTTP handoff client", () => {
  it("starts with a same-origin cookie-bound request", async () => {
    const fetchMock = vi.fn(() =>
      Promise.resolve(
        new Response(
          JSON.stringify({ authorization_url: "http://localhost:3000/login?state=safe" }),
          { status: 200 },
        ),
      ),
    );
    vi.stubGlobal("fetch", fetchMock);

    const destination = await new HttpHandoffClient().start();

    expect(destination).toBe("http://localhost:3000/login?state=safe");
    expect(fetchMock).toHaveBeenCalledWith("/api/v1/auth/handoff/start", {
      method: "POST",
      cache: "no-store",
      credentials: "same-origin",
      redirect: "error",
    });
  });

  it("exchanges a disposable code without storing the returned token", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({ access_token: "memory-only-token", token_type: "Bearer" }),
            { status: 200 },
          ),
        ),
      ),
    );

    const token = await new HttpHandoffClient().exchange("one-time-code", "browser-state");

    expect(token).toBe("memory-only-token");
    expect(window.localStorage.getItem("vittavaan.accessToken")).toBeNull();
    expect(window.sessionStorage.getItem("vittavaan.accessToken")).toBeNull();
  });
});
