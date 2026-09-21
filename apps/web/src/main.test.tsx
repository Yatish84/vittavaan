// @vitest-environment jsdom

import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { FoundationApp } from "./App";

describe("foundation shell", () => {
  it("has an accessible heading", () => {
    render(<FoundationApp />);
    expect(screen.getByRole("heading", { name: "Foundation environment" })).toBeInTheDocument();
  });
});
