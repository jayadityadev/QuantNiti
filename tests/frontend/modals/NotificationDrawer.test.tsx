import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { NotificationDrawer } from "../../../src/frontend/components/modals/NotificationDrawer";
import { useAppStore } from "../../../src/frontend/store/useAppStore";

const ALERTS = [
  {
    id: "alert_1",
    type: "REGIME_TRANSITION",
    severity: "INFO",
    title: "Market Regime Transition",
    message: "NIFTY 50 momentum shifted above the 50-day EMA.",
    timestamp: "2 mins ago",
    read: false,
  },
  {
    id: "alert_2",
    type: "PORTFOLIO_DRIFT",
    severity: "HIGH",
    title: "Portfolio Drift Detected",
    message: "IT sector weighting drifted above the target band.",
    timestamp: "1 hour ago",
    read: false,
  },
  {
    id: "alert_3",
    type: "RSI_EXTREME",
    severity: "MEDIUM",
    title: "RSI Extremum",
    message: "RSI moved into overbought territory.",
    timestamp: "3 hours ago",
    read: true,
  },
];

function mockAlertsResponse(payload: { alerts: any[]; total: number; unread_count: number }) {
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => payload,
  });
}

describe("NotificationDrawer", () => {
  beforeEach(() => {
    useAppStore.setState({ unreadAlertCount: 0 });
    mockAlertsResponse({ alerts: ALERTS, total: ALERTS.length, unread_count: 2 });
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  it("renders alerts from the backend, category filters, and web push prompt", async () => {
    render(<NotificationDrawer isOpen={true} onClose={() => {}} />);

    expect(screen.getByText("Smart Notifications")).toBeInTheDocument();
    expect(screen.getByText("Enable Web Push Alerts")).toBeInTheDocument();
    expect(await screen.findByText("Market Regime Transition")).toBeInTheDocument();
    expect(screen.getByText("Portfolio Drift Detected")).toBeInTheDocument();
    expect(useAppStore.getState().unreadAlertCount).toBe(2);
  });

  it("does not fabricate alerts when the backend returns none", async () => {
    mockAlertsResponse({ alerts: [], total: 0, unread_count: 0 });
    render(<NotificationDrawer isOpen={true} onClose={() => {}} />);

    expect(await screen.findByText("No notifications in this category.")).toBeInTheDocument();
    expect(screen.queryByText("Market Regime Active: Bull Market")).not.toBeInTheDocument();
    expect(useAppStore.getState().unreadAlertCount).toBe(0);
  });

  it("filters notifications by category pill, including enum alert types", async () => {
    render(<NotificationDrawer isOpen={true} onClose={() => {}} />);
    expect(await screen.findByText("Market Regime Transition")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Drift" }));

    expect(screen.getByText("Portfolio Drift Detected")).toBeInTheDocument();
    expect(screen.queryByText("Market Regime Transition")).not.toBeInTheDocument();
  });

  it("clears the unread badge when marking everything read", async () => {
    render(<NotificationDrawer isOpen={true} onClose={() => {}} />);
    expect(await screen.findByText("Market Regime Transition")).toBeInTheDocument();
    expect(useAppStore.getState().unreadAlertCount).toBe(2);

    fireEvent.click(screen.getByRole("button", { name: /mark read/i }));

    expect(useAppStore.getState().unreadAlertCount).toBe(0);
  });

  it("sets up and tears down 45-second polling interval on open/unmount", () => {
    vi.useFakeTimers();
    const setIntervalSpy = vi.spyOn(window, "setInterval");
    const clearIntervalSpy = vi.spyOn(window, "clearInterval");

    const { unmount } = render(<NotificationDrawer isOpen={true} onClose={() => {}} />);

    expect(setIntervalSpy).toHaveBeenCalledWith(expect.any(Function), 45000);

    unmount();
    expect(clearIntervalSpy).toHaveBeenCalled();
  });
});
