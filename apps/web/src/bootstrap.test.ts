import { afterEach, describe, expect, it, vi } from "vitest";
import { BootstrapFailure, HttpBootstrapClient } from "./bootstrap";

afterEach(() => vi.unstubAllGlobals());

describe("HTTP bootstrap client", () => {
  it("sends the in-memory bearer token with storage-safe request options", async () => {
    const fetchMock = vi.fn(() =>
      Promise.resolve(
        new Response(
          JSON.stringify({
            principal: {
              principal_id: "0199a000-0000-7000-8000-000000000001",
              principal_type: "PERSON",
              status: "ACTIVE",
            },
            first_run_required: true,
            next_route: "/account-setup",
            permitted_person_ids: [],
            permitted_household_ids: [],
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
      ),
    );
    vi.stubGlobal("fetch", fetchMock);
    const signal = new AbortController().signal;

    await new HttpBootstrapClient().load("memory-only-token", signal);

    expect(fetchMock).toHaveBeenCalledWith("/api/v1/bootstrap", {
      method: "GET",
      headers: { Authorization: "Bearer memory-only-token" },
      cache: "no-store",
      credentials: "omit",
      redirect: "error",
      signal,
    });
  });

  it("fails closed when a success response has an unexpected shape", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.resolve(new Response(JSON.stringify({ principal: {} }), { status: 200 }))),
    );

    await expect(
      new HttpBootstrapClient().load("memory-only-token", new AbortController().signal),
    ).rejects.toEqual(new BootstrapFailure("unavailable"));
  });
});
