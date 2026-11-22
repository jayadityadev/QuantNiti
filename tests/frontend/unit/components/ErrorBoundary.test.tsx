import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, afterEach } from "vitest";
import { ErrorBoundary } from "../../../../src/frontend/components/ui/ErrorBoundary";

const Boom = () => {
  throw new Error("Malformed API payload");
};

describe("ErrorBoundary", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("renders a recoverable fallback instead of unmounting to a blank screen", () => {
    // React logs the caught error; keep the test output clean.
    vi.spyOn(console, "error").mockImplementation(() => {});

    render(
      <ErrorBoundary>
        <Boom />
      </ErrorBoundary>
    );

    expect(screen.getByRole("alert")).toHaveTextContent(/Something went wrong/i);
    expect(
      screen.getByRole("button", { name: /Reload app/i })
    ).toBeInTheDocument();
  });

  it("renders children normally when nothing throws", () => {
    render(
      <ErrorBoundary>
        <div>Healthy screen</div>
      </ErrorBoundary>
    );

    expect(screen.getByText("Healthy screen")).toBeInTheDocument();
    expect(screen.queryByText(/Something went wrong/i)).not.toBeInTheDocument();
  });
});
