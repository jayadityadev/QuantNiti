// ─────────────────────────────────────────────────────────────────────────────
// Curated lessons from TIDI ಕನ್ನಡ and GTF – A Stock Market Institute.
// Every videoId is a real public upload that allows embedding (checked via
// YouTube oEmbed + playableInEmbed). If a lesson ever stops playing, swap its
// videoId for another upload from the same channel.
// ─────────────────────────────────────────────────────────────────────────────

export type LessonChannel = "TIDI" | "GTF";
export type LessonLevel = "beginner" | "intermediate" | "advanced";

export interface Lesson {
  id: string;
  videoId: string;
  title: string;
  channel: LessonChannel;
  category: string;
  level: LessonLevel;
  durationSeconds: number;
  description: string;
}

export const CHANNELS: Record<
  LessonChannel,
  { name: string; handle: string; url: string; language: string; badge: string; iconText: string }
> = {
  TIDI: {
    name: "TIDI ಕನ್ನಡ",
    handle: "@TIDIkannada",
    url: "https://www.youtube.com/@TIDIkannada",
    language: "Kannada",
    badge: "bg-red-600/20 text-red-400 border-red-500/30",
    iconText: "text-red-500",
  },
  GTF: {
    name: "GTF – A Stock Market Institute",
    handle: "@gettogetherfinance",
    url: "https://www.youtube.com/@gettogetherfinance",
    language: "Hindi",
    badge: "bg-emerald-600/20 text-emerald-400 border-emerald-500/30",
    iconText: "text-emerald-500",
  },
};

export const LESSONS: Lesson[] = [
  // ── BEGINNER ───────────────────────────────────────────────────────────────
  {
    id: "l1",
    videoId: "mhHtFoTWaeQ",
    title: "Stock Market for Beginners: Complete Basics",
    channel: "TIDI",
    category: "Basics",
    level: "beginner",
    durationSeconds: 2541,
    description:
      "Everything to know before your first investment: what shares are, how NSE & BSE work, and how to think about risk — explained in Kannada.",
  },
  {
    id: "l2",
    videoId: "HyJQU1pPx7E",
    title: "Trading in the Zone – Elementary Class 1",
    channel: "GTF",
    category: "Basics",
    level: "beginner",
    durationSeconds: 6157,
    description:
      "The first class of GTF's flagship course. Starts from zero: how the market works, who the participants are, and how price moves.",
  },
  {
    id: "l18",
    videoId: "1kvknZoU--M",
    title: "A Complete Course on Stock Market – Beginner to Advanced",
    channel: "GTF",
    category: "Basics",
    level: "beginner",
    durationSeconds: 188801,
    description:
      "GTF's complete course in one video (52+ hours). Use the chapters to jump between topics, from market basics to advanced price action.",
  },
  {
    id: "l3",
    videoId: "TEaTFy5KeFM",
    title: "How to Trade from Your Demat Account",
    channel: "TIDI",
    category: "Basics",
    level: "beginner",
    durationSeconds: 474,
    description:
      "A short, practical walkthrough of placing your first buy and sell orders from a Demat account.",
  },
  {
    id: "l4",
    videoId: "LN3ikphmh5I",
    title: "How to Read Candlesticks",
    channel: "TIDI",
    category: "Technical Analysis",
    level: "beginner",
    durationSeconds: 565,
    description:
      "Open, high, low and close — how a single candle tells the story of a trading session, and how to read a chart of them.",
  },
  {
    id: "l5",
    videoId: "maTBd-aEcDM",
    title: "How to Select Winning Stocks – Step by Step",
    channel: "TIDI",
    category: "Fundamentals",
    level: "beginner",
    durationSeconds: 1366,
    description:
      "A step-by-step process for shortlisting quality companies before you invest, instead of chasing tips.",
  },

  // ── INTERMEDIATE ───────────────────────────────────────────────────────────
  {
    id: "l6",
    videoId: "K8u1MZnK-DA",
    title: "Price Action Behind the Candles",
    channel: "GTF",
    category: "Technical Analysis",
    level: "intermediate",
    durationSeconds: 9990,
    description:
      "Trading in the Zone, Episode 6. Reading the buying and selling pressure behind candle patterns rather than memorising pattern names.",
  },
  {
    id: "l7",
    videoId: "HDGNBqyEMQs",
    title: "Demand & Supply Zones",
    channel: "GTF",
    category: "Strategy",
    level: "intermediate",
    durationSeconds: 8394,
    description:
      "Trading in the Zone, Episode 3. How to mark demand and supply zones on a chart and use them for entries and exits.",
  },
  {
    id: "l8",
    videoId: "bi92YyfKTgk",
    title: "Multiple Time Frame Analysis",
    channel: "GTF",
    category: "Strategy",
    level: "intermediate",
    durationSeconds: 9442,
    description:
      "Trading in the Zone, Episode 7. Aligning the higher-time-frame trend with lower-time-frame entries.",
  },
  {
    id: "l9",
    videoId: "HM9yGgOmwHo",
    title: "Intraday Strategy Using RSI & VWAP",
    channel: "TIDI",
    category: "Intraday",
    level: "intermediate",
    durationSeconds: 1616,
    description:
      "An intraday setup combining price action with RSI and VWAP, including where to enter and where to exit.",
  },
  {
    id: "l10",
    videoId: "1v00-Bpxm2A",
    title: "A Powerful Swing Trading Setup",
    channel: "TIDI",
    category: "Strategy",
    level: "intermediate",
    durationSeconds: 722,
    description:
      "A swing setup for holding positions over several days to capture medium-term moves.",
  },
  {
    id: "l11",
    videoId: "1atgqHaLGvc",
    title: "Sectoral Analysis",
    channel: "GTF",
    category: "Fundamentals",
    level: "intermediate",
    durationSeconds: 11334,
    description:
      "Trading in the Zone, Episode 16. How sector rotation works and how to find the strongest stocks inside the strongest sectors.",
  },

  // ── ADVANCED ───────────────────────────────────────────────────────────────
  {
    id: "l12",
    videoId: "DRTEMgQRxTU",
    title: "What Is Futures Trading?",
    channel: "TIDI",
    category: "F&O",
    level: "advanced",
    durationSeconds: 785,
    description:
      "Futures contracts, lot sizes, margin and expiry — the foundation you need before touching F&O.",
  },
  {
    id: "l13",
    videoId: "Ftw7mK6WbNc",
    title: "Options Basics – Foundation Part 1",
    channel: "TIDI",
    category: "F&O",
    level: "advanced",
    durationSeconds: 1278,
    description:
      "Calls, puts, strike prices and premiums — the building blocks of options trading.",
  },
  {
    id: "l14",
    videoId: "FQfVXFHa-Uc",
    title: "Option Greeks: Theta & Delta",
    channel: "TIDI",
    category: "F&O",
    level: "advanced",
    durationSeconds: 807,
    description:
      "What Delta and Theta mean in practice, and how time decay eats into an option buyer's premium.",
  },
  {
    id: "l15",
    videoId: "3ptyuNuRz9Q",
    title: "Algo Trading Full Course in Kannada",
    channel: "TIDI",
    category: "Algo Trading",
    level: "advanced",
    durationSeconds: 2537,
    description:
      "How algorithmic trading works, how strategies are automated, and what to watch out for before running one with real money.",
  },
  {
    id: "l16",
    videoId: "z6BQzqe_BRg",
    title: "Risk Management in the Stock Market",
    channel: "GTF",
    category: "Risk",
    level: "advanced",
    durationSeconds: 9707,
    description:
      "Trading in the Zone, Episode 10. Position sizing, risk per trade and protecting capital through losing streaks.",
  },
  {
    id: "l17",
    videoId: "ppitF1gd9tY",
    title: "How to Place a Stop Loss in a Live Market",
    channel: "TIDI",
    category: "Risk",
    level: "advanced",
    durationSeconds: 1357,
    description:
      "Where to put a stop loss, why it matters, and how to avoid getting stopped out by normal market noise.",
  },
];

export const LESSON_CATEGORIES = ["All", ...Array.from(new Set(LESSONS.map((l) => l.category)))];

export const formatDuration = (seconds: number): string => {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  if (h > 0) return `${h}h ${m}m`;
  return `${m} min`;
};

export const watchUrl = (videoId: string) => `https://www.youtube.com/watch?v=${videoId}`;

export const thumbnailUrl = (videoId: string) => `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`;
