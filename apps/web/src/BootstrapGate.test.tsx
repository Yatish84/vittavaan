// @vitest-environment jsdom

import "@testing-library/jest-dom/vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { BootstrapGate } from "./BootstrapGate";
import type { BootstrapClient, BootstrapResponse } from "./bootstrap";
import { BootstrapFailure } from "./bootstrap";

const response: BootstrapResponse = {
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

function client(result: BootstrapResponse | BootstrapFailure): BootstrapClient {
  return {
    load: vi.fn(() =>
      result instanceof BootstrapFailure ? Promise.reject(result) : Promise.resolve(result),
    ),
  };
}

describe("bootstrap gate", () => {
  it("shows the first-run route for a new principal", async () => {
    render(<BootstrapGate accessToken="memory-only-token" client={client(response)} />);
    expect(await screen.findByRole("heading", { name: "Let’s set up your portfolio" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Start account setup" })).toHaveAttribute(
      "href",
      "/account-setup",
    );
  });

  it("shows signed out after a 401", async () => {
    render(
      <BootstrapGate
        accessToken="expired-token"
        client={client(new BootstrapFailure("unauthenticated"))}
      />,
    );
    expect(await screen.findByRole("heading", { name: "Sign in to Vittavaan" })).toBeInTheDocument();
  });

  it("shows a non-bypassable denial after a 403", async () => {
    render(
      <BootstrapGate
        accessToken="valid-token"
        client={client(new BootstrapFailure("denied"))}
      />,
    );
    expect(await screen.findByRole("heading", { name: "Access is unavailable" })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Try again" })).not.toBeInTheDocument();
  });

  it("allows a temporary failure to be retried", async () => {
    const load = vi.fn(() => Promise.reject(new BootstrapFailure("unavailable")));
    const bootstrapClient: BootstrapClient = { load };
    render(<BootstrapGate accessToken="valid-token" client={bootstrapClient} />);
    fireEvent.click(await screen.findByRole("button", { name: "Try again" }));
    expect(load).toHaveBeenCalledTimes(2);
  });
});
