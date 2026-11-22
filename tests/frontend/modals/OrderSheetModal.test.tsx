import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeEach, vi } from "vitest";
import { OrderSheetModal } from "../../../src/frontend/components/modals/OrderSheetModal";
import { getDemoPortfolio } from "../../../src/frontend/components/portfolio/demoPortfolioData";

describe("OrderSheetModal clipboard handling", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("reports a copy failure instead of showing 'Copied!' when writeText rejects", async () => {
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: {
        writeText: vi
          .fn()
          .mockRejectedValue(new DOMException("Denied", "NotAllowedError")),
      },
    });

    render(
      <OrderSheetModal
        isOpen={true}
        onClose={() => {}}
        portfolio={getDemoPortfolio()}
      />
    );

    fireEvent.click(
      screen.getByRole("button", { name: /Copy Order Instructions/i })
    );

    await waitFor(() =>
      expect(screen.getByRole("alert")).toHaveTextContent(/Copy failed/i)
    );
    expect(
      screen.queryByText(/Copied to Clipboard/i)
    ).not.toBeInTheDocument();
  });

  it("shows the copied state only after writeText resolves", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText },
    });

    render(
      <OrderSheetModal
        isOpen={true}
        onClose={() => {}}
        portfolio={getDemoPortfolio()}
      />
    );

    fireEvent.click(
      screen.getByRole("button", { name: /Copy Order Instructions/i })
    );

    await waitFor(() => expect(writeText).toHaveBeenCalledTimes(1));
    expect(
      await screen.findByRole("button", { name: /Copied to Clipboard/i })
    ).toBeInTheDocument();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});
