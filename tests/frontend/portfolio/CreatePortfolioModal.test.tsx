import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeEach, vi } from "vitest";
import { CreatePortfolioModal } from "../../../src/frontend/components/portfolio/CreatePortfolioModal";

describe("CreatePortfolioModal", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("submits exactly once when the create button is activated", async () => {
    const onCreate = vi.fn().mockResolvedValue(undefined);
    const onClose = vi.fn();

    render(
      <CreatePortfolioModal
        isOpen={true}
        onClose={onClose}
        onCreate={onCreate}
      />
    );

    fireEvent.click(
      screen.getByRole("button", { name: /Create Virtual Portfolio/i })
    );

    await waitFor(() => expect(onCreate).toHaveBeenCalledTimes(1));
    expect(onCreate).toHaveBeenCalledWith({
      name: "Retirement 2040",
      capital: 100000,
      riskPersona: "Balanced",
    });
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("labels both inputs for assistive technology", () => {
    render(
      <CreatePortfolioModal isOpen={true} onClose={() => {}} onCreate={vi.fn()} />
    );

    expect(
      screen.getByLabelText(/Portfolio \/ Goal Name/i)
    ).toBeInTheDocument();
    expect(
      screen.getByLabelText(/Initial Virtual Capital/i)
    ).toBeInTheDocument();
  });

  it("keeps the modal open and shows an error when creation rejects", async () => {
    const onCreate = vi.fn().mockRejectedValue(new Error("Network unavailable"));
    const onClose = vi.fn();

    render(
      <CreatePortfolioModal
        isOpen={true}
        onClose={onClose}
        onCreate={onCreate}
      />
    );

    fireEvent.click(
      screen.getByRole("button", { name: /Create Virtual Portfolio/i })
    );

    await waitFor(() =>
      expect(screen.getByRole("alert")).toHaveTextContent("Network unavailable")
    );
    expect(onClose).not.toHaveBeenCalled();
  });
});
