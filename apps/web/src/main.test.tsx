// @vitest-environment jsdom

import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { VittavaanApp } from "./App";
import type { BootstrapClient, BootstrapResponse } from "./bootstrap";
import type { HandoffClient } from "./handoff";

afterEach(() => {
  window.history.replaceState(null, "", "/");
});

describe("application shell", () => {
  it("offers the reviewed secure sign-in handoff", async () => {
    const handoff: HandoffClient = {
      start: vi.fn(() => Promise.resolve("http://localhost:3000/login")),
      exchange: vi.fn(() => Promise.reject(new Error("not called"))),
    };
    render(<VittavaanApp handoff={handoff} />);
    expect(
      await screen.findByRole("heading", { name: "Sign in to Vittavaan" }),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Continue to sign in" })).toBeEnabled();
  });

  it("removes the one-time code from the URL before loading bootstrap", async () => {
    window.history.replaceState(
      null,
      "",
      "/auth/return?code=one-time-code&state=browser-bound-state",
    );
    const handoff: HandoffClient = {
      start: vi.fn(() => Promise.reject(new Error("not called"))),
      exchange: vi.fn(() => Promise.resolve("memory-only-token")),
    };
    const bootstrapResponse: BootstrapResponse = {
      principal: {
        principal_id: "0199a000-0000-7000-8000-000000000001",
        principal_type: "PERSON",
        status: "ACTIVE",
      },
      first_run_required: true,
      next_route: "/account-setup",
      permitted_person_ids: [],
      permitted_household_ids: [],
    };
    const bootstrap: BootstrapClient = {
      load: vi.fn(() => Promise.resolve(bootstrapResponse)),
    };

    render(<VittavaanApp handoff={handoff} bootstrap={bootstrap} />);

    expect(
      await screen.findByRole("heading", { name: "Let’s set up your portfolio" }),
    ).toBeInTheDocument();
    expect(window.location.pathname).toBe("/");
    expect(window.location.search).toBe("");
  });
});
