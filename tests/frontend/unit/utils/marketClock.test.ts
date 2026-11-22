import { describe, it, expect } from "vitest";
import { evaluateMarketSession, getNowIST, isNSEHoliday } from "../../../../src/frontend/utils/marketClock";

describe("Centralized 5-State IST Market Session Clock", () => {
  it("computes accurate IST date components", () => {
    // 2026-03-11 06:00:00 UTC -> 11:30:00 IST
    const utcDate = new Date(Date.UTC(2026, 2, 11, 6, 0, 0));
    const ist = getNowIST(utcDate);

    expect(ist.year).toBe(2026);
    expect(ist.month).toBe(3);
    expect(ist.day).toBe(11);
    expect(ist.hours).toBe(11);
    expect(ist.minutes).toBe(30);
    expect(ist.dateKey).toBe("2026-03-11");
  });

  it("identifies official NSE trading holidays", () => {
    expect(isNSEHoliday("2026-01-26")).toBe(true); // Republic day
    expect(isNSEHoliday("2026-08-15")).toBe(true); // Independence day
    expect(isNSEHoliday("2026-03-11")).toBe(false); // Normal day
  });

  it("evaluates LIVE state during active market hours", () => {
    const wedDate = new Date(Date.UTC(2026, 2, 11, 6, 0, 0)); // 11:30 IST
    const lastTick = Date.now() - 4000; // 4s ago

    const session = evaluateMarketSession(wedDate, lastTick);
    expect(session.state).toBe("LIVE");
    expect(session.label).toBe("NSE Live");
    expect(session.isMarketHours).toBe(true);
  });

  it("evaluates STALE state when last tick > 15 seconds", () => {
    const wedDate = new Date(Date.UTC(2026, 2, 11, 6, 0, 0)); // 11:30 IST
    const lastTick = Date.now() - 25000; // 25s ago

    const session = evaluateMarketSession(wedDate, lastTick);
    expect(session.state).toBe("STALE");
    expect(session.label).toBe("Feed Stale");
    expect(session.statusText).toContain("NSE Feed Stale");
  });

  it("evaluates RESYNCING state on connection recovery", () => {
    const wedDate = new Date(Date.UTC(2026, 2, 11, 6, 0, 0));
    const session = evaluateMarketSession(wedDate, null, true);
    expect(session.state).toBe("RESYNCING");
    expect(session.label).toBe("Resyncing");
  });

  it("evaluates CLOSED state on weekend", () => {
    // 2026-03-15 is Sunday
    const sunDate = new Date(Date.UTC(2026, 2, 15, 8, 30, 0)); // 14:00 IST
    const session = evaluateMarketSession(sunDate);

    expect(session.state).toBe("CLOSED");
    expect(session.label).toBe("Market Closed");
    expect(session.statusText).toContain("NSE: Market Closed");
    expect(session.statusText).toContain("Reopens Mon 09:15 IST");
  });

  it("evaluates SNAPSHOT state after 15:30 IST on trading day", () => {
    const eodDate = new Date(Date.UTC(2026, 2, 11, 11, 30, 0)); // 17:00 IST
    const session = evaluateMarketSession(eodDate);

    expect(session.state).toBe("SNAPSHOT");
    expect(session.label).toBe("EOD Snapshot");
    expect(session.isMarketHours).toBe(false);
  });
});
