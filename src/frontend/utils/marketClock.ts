/**
 * Centralized 5-State IST Market Session Clock and Telemetry Freshness Engine.
 *
 * 5 States:
 * - LIVE: During market hours (09:15 to 15:30 IST on NSE trading days) with active streaming updates.
 * - SNAPSHOT: Off-market hours displaying authoritative End-of-Day (EOD) closing data.
 * - CLOSED: Weekend or market holiday (e.g. 'NSE: Market Closed · Reopens Mon 09:15 IST').
 * - STALE: Ticks older than 15s during active market hours flagged with a warning pill.
 * - RESYNCING: Connection drop / recovery state.
 */

export type MarketSessionState = "LIVE" | "SNAPSHOT" | "CLOSED" | "STALE" | "RESYNCING";

export interface MarketSessionInfo {
  state: MarketSessionState;
  label: string;
  statusText: string;
  istTimeStr: string;
  isTradingDay: boolean;
  isMarketHours: boolean;
  reopenLabel?: string;
  lastTickAgeSeconds?: number;
}

// Known National Stock Exchange (NSE) Trading Holidays (2025/2026 standard calendar)
export const NSE_HOLIDAYS_YYYY_MM_DD = new Set<string>([
  // 2025
  "2025-01-26", "2025-02-26", "2025-03-14", "2025-03-31", "2025-04-10",
  "2025-04-14", "2025-04-18", "2025-05-01", "2025-08-15", "2025-08-27",
  "2025-10-02", "2025-10-21", "2025-10-22", "2025-11-05", "2025-12-25",
  // 2026
  "2026-01-26", "2026-03-03", "2026-03-20", "2026-04-03", "2026-04-14",
  "2026-05-01", "2026-08-15", "2026-09-04", "2026-10-02", "2026-10-20",
  "2026-11-08", "2026-11-10", "2026-12-25",
]);

/**
 * Returns current Date adjusted to Indian Standard Time (UTC+05:30).
 */
export function getNowIST(overrideDate?: Date): {
  date: Date;
  year: number;
  month: number;
  day: number;
  weekday: number;
  hours: number;
  minutes: number;
  seconds: number;
  dateKey: string;
  istTimeStr: string;
} {
  const base = overrideDate || new Date();
  // UTC milliseconds + 5 hours 30 mins (19,800,000 ms)
  const utcMs = base.getTime() + base.getTimezoneOffset() * 60000;
  const istDate = new Date(utcMs + 5.5 * 3600000);

  const year = istDate.getFullYear();
  const month = istDate.getMonth() + 1;
  const day = istDate.getDate();
  const weekday = istDate.getDay(); // 0 = Sun, 1 = Mon ... 6 = Sat
  const hours = istDate.getHours();
  const minutes = istDate.getMinutes();
  const seconds = istDate.getSeconds();

  const mm = month < 10 ? `0${month}` : `${month}`;
  const dd = day < 10 ? `0${day}` : `${day}`;
  const hh = hours < 10 ? `0${hours}` : `${hours}`;
  const min = minutes < 10 ? `0${minutes}` : `${minutes}`;
  const ss = seconds < 10 ? `0${seconds}` : `${seconds}`;

  return {
    date: istDate,
    year,
    month,
    day,
    weekday,
    hours,
    minutes,
    seconds,
    dateKey: `${year}-${mm}-${dd}`,
    istTimeStr: `${hh}:${min}:${ss} IST`,
  };
}

export function isNSEHoliday(dateKey: string): boolean {
  return NSE_HOLIDAYS_YYYY_MM_DD.has(dateKey);
}

/**
 * Calculates next NSE trading day string.
 */
export function getNextTradingDay(startDate: Date): { dayName: string; dateKey: string } {
  const cur = new Date(startDate.getTime());
  const dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  for (let i = 1; i <= 10; i++) {
    cur.setDate(cur.getDate() + 1);
    const day = cur.getDay();
    const mm = cur.getMonth() + 1 < 10 ? `0${cur.getMonth() + 1}` : `${cur.getMonth() + 1}`;
    const dd = cur.getDate() < 10 ? `0${cur.getDate()}` : `${cur.getDate()}`;
    const key = `${cur.getFullYear()}-${mm}-${dd}`;

    if (day !== 0 && day !== 6 && !isNSEHoliday(key)) {
      return { dayName: dayNames[day], dateKey: key };
    }
  }
  return { dayName: "Mon", dateKey: "" };
}

/**
 * Evaluates the 5-State IST Market Session Clock.
 */
export function evaluateMarketSession(
  overrideDate?: Date,
  lastTickTimestamp?: Date | number | null,
  isResyncing = false
): MarketSessionInfo {
  const ist = getNowIST(overrideDate);
  const isWeekend = ist.weekday === 0 || ist.weekday === 6; // Sun or Sat
  const isHoliday = isNSEHoliday(ist.dateKey);
  const isTradingDay = !isWeekend && !isHoliday;

  // Market hours: 09:15 to 15:30 IST
  const timeInMinutes = ist.hours * 60 + ist.minutes;
  const openMinutes = 9 * 60 + 15; // 555
  const closeMinutes = 15 * 60 + 30; // 930
  const isMarketHours = isTradingDay && timeInMinutes >= openMinutes && timeInMinutes <= closeMinutes;

  let lastTickAge: number | undefined = undefined;
  if (lastTickTimestamp) {
    const tickTime = typeof lastTickTimestamp === "number" ? lastTickTimestamp : lastTickTimestamp.getTime();
    lastTickAge = Math.max(0, (Date.now() - tickTime) / 1000);
  }

  // 1. Connection Drop / Recovery -> RESYNCING
  if (isResyncing) {
    return {
      state: "RESYNCING",
      label: "Resyncing",
      statusText: "Connection Drop · Resyncing NSE Telemetry...",
      istTimeStr: ist.istTimeStr,
      isTradingDay,
      isMarketHours,
      lastTickAgeSeconds: lastTickAge,
    };
  }

  // 2. Weekend or Holiday -> CLOSED
  if (!isTradingDay) {
    const nextTradingDay = getNextTradingDay(ist.date);
    const reopenLabel = `Reopens ${nextTradingDay.dayName} 09:15 IST`;
    return {
      state: "CLOSED",
      label: "Market Closed",
      statusText: `NSE: Market Closed · ${reopenLabel}`,
      istTimeStr: ist.istTimeStr,
      isTradingDay: false,
      isMarketHours: false,
      reopenLabel,
      lastTickAgeSeconds: lastTickAge,
    };
  }

  // 3. Trading Day During 09:15 - 15:30 IST
  if (isMarketHours) {
    if (lastTickAge !== undefined && lastTickAge > 15.0) {
      return {
        state: "STALE",
        label: "Feed Stale",
        statusText: `NSE Feed Stale · Last tick ${Math.round(lastTickAge)}s ago`,
        istTimeStr: ist.istTimeStr,
        isTradingDay: true,
        isMarketHours: true,
        lastTickAgeSeconds: lastTickAge,
      };
    }
    return {
      state: "LIVE",
      label: "NSE Live",
      statusText: "Live NSE Feed · Active Market Session",
      istTimeStr: ist.istTimeStr,
      isTradingDay: true,
      isMarketHours: true,
      lastTickAgeSeconds: lastTickAge,
    };
  }

  // 4. Off-market hours on Trading Day -> SNAPSHOT
  if (timeInMinutes > closeMinutes) {
    const nextDay = getNextTradingDay(ist.date);
    return {
      state: "SNAPSHOT",
      label: "EOD Snapshot",
      statusText: `NSE: Authoritative EOD 15:30 IST · Reopens ${nextDay.dayName} 09:15 IST`,
      istTimeStr: ist.istTimeStr,
      isTradingDay: true,
      isMarketHours: false,
      reopenLabel: `Reopens ${nextDay.dayName} 09:15 IST`,
      lastTickAgeSeconds: lastTickAge,
    };
  } else {
    // Pre-market before 09:15
    return {
      state: "SNAPSHOT",
      label: "Pre-Market",
      statusText: "NSE: Authoritative EOD Snapshot · Market Opens 09:15 IST",
      istTimeStr: ist.istTimeStr,
      isTradingDay: true,
      isMarketHours: false,
      reopenLabel: "Opens Today 09:15 IST",
      lastTickAgeSeconds: lastTickAge,
    };
  }
}
