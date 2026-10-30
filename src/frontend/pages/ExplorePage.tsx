import React, { useState, useEffect, useMemo } from "react";
import { motion } from "framer-motion";
import { Search, X, Compass, Layers } from "lucide-react";
import { StockCard, ExploreStockItem } from "../components/explore/StockCard";
import { StockProfileModal } from "../components/explore/StockProfileModal";
import { useAppStore } from "../store/useAppStore";

import { ProToolsBacktester } from "../components/explore/ProToolsBacktester";
import { abortRegistry } from "../services/abortRegistry";
import { ChipButton } from "../components/ui/ChipButton";
import { apiUrl } from "../config";

// Chip label -> canonical sector served by the API (see SECTORS in src/app/universe.py)
const SECTORS: { label: string; sector: string | null }[] = [
  { label: "All", sector: null },
  { label: "Banking & Finance", sector: "Financial Services" },
  { label: "Technology", sector: "Information Technology" },
  { label: "Energy", sector: "Energy" },
  { label: "Automobile", sector: "Automobile" },
  { label: "Healthcare", sector: "Healthcare" },
  { label: "Consumer Goods", sector: "Consumer Goods" },
  { label: "Metals & Mining", sector: "Metals & Mining" },
  { label: "Defense", sector: "Defense" },
  { label: "Infrastructure", sector: "Infrastructure" },
  { label: "Telecom", sector: "Telecom" },
  { label: "Gold & Silver", sector: "Commodities" },
];


export const ExplorePage: React.FC = () => {
  const { allExploreStocks, setAllExploreStocks, setSelectedStockSymbol } =
    useAppStore();

  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedSector, setSelectedSector] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [activeModalSymbol, setActiveModalSymbol] = useState<string | null>(null);
  const [loadError, setLoadError] = useState<boolean>(false);

  // Arriving from a Home "Top Movers" tap: open that stock's profile straight away
  useEffect(() => {
    const preselected = useAppStore.getState().selectedStockSymbol;
    if (preselected) {
      setActiveModalSymbol(preselected);
      setIsModalOpen(true);
    }
  }, []);

  // Fetch stocks on mount with async cancellation seam
  useEffect(() => {
    const signal = abortRegistry.register("explore-stocks");

    fetch(apiUrl("/api/explore/stocks"), { signal })
      .then((res) => {
        if (!res.ok) throw new Error("Explore stocks API failed");
        return res.json();
      })
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setAllExploreStocks(data);
        }
      })
      .catch((err) => {
        // abort(reason) rejects with the reason string, not an AbortError
        if (err?.name === "AbortError" || signal.aborted) return;
        // Never substitute invented prices: show the real failure instead.
        setLoadError(true);
      });

    return () => {
      abortRegistry.abort("explore-stocks");
    };
  }, [setAllExploreStocks]);

  const stockList = allExploreStocks;

  // In-memory search and sector filtering
  const filteredStocks = useMemo(() => {
    return stockList.filter((stock) => {
      const matchesSearch =
        searchQuery.trim() === "" ||
        stock.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
        stock.name.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesSector = selectedSector === null || stock.sector === selectedSector;

      return matchesSearch && matchesSector;
    });
  }, [stockList, searchQuery, selectedSector]);

  const handleSelectStock = (stock: ExploreStockItem) => {
    setActiveModalSymbol(stock.symbol);
    setSelectedStockSymbol(stock.symbol);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setActiveModalSymbol(null);
    setSelectedStockSymbol(null);
  };

  // Staggered motion container
  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.05,
      },
    },
  };

  return (
    <div className="flex flex-col gap-4 p-4 w-full mx-auto">
      <h1 className="sr-only">Explore Page</h1>
      {/* Header Banner */}
      <div className="flex items-center justify-between pb-1">
        <div>
          <div className="flex items-center gap-1.5 text-accent mb-0.5">
            <Compass className="w-4 h-4" />
            <span className="text-[11px] font-bold uppercase tracking-wider">
              Market Intelligence
            </span>
          </div>
          <h1 className="text-xl font-black text-[var(--text-main)] tracking-tight">
            Explore Universe
          </h1>
        </div>
        <div className="text-right">
          <span className="text-xs font-mono font-semibold text-[var(--text-muted)]">
            {filteredStocks.length} Assets
          </span>
        </div>
      </div>

      {/* In-Memory Search Input */}
      <div className="relative">
        <Search className="w-4 h-4 text-[var(--text-muted)] absolute left-3.5 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          placeholder="Search stocks or symbols (e.g. RELIANCE, TCS)..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-10 pr-9 py-2.5 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] text-sm font-semibold text-[var(--text-main)] placeholder:text-[var(--text-muted)] focus:outline-none focus:border-violet-500 transition-colors shadow-sm"
        />
        {searchQuery && (
          <button
            type="button"
            onClick={() => setSearchQuery("")}
            className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-[var(--text-muted)] hover:text-accent rounded-full transition-colors"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Horizontal Sector Filter Chips */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar -mx-4 px-4">
        {SECTORS.map(({ label, sector }) => (
          <ChipButton
            key={label}
            active={selectedSector === sector}
            onClick={() => setSelectedSector(sector)}
            className="shrink-0"
          >
            {label}
          </ChipButton>
        ))}
      </div>

      {/* Redesigned Stock Cards Grid */}
      {filteredStocks.length > 0 ? (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 sm:grid-cols-2 gap-3.5"
        >
          {filteredStocks.map((stock) => (
            <StockCard
              key={stock.symbol}
              stock={stock}
              onSelect={handleSelectStock}
            />
          ))}
        </motion.div>
      ) : (
        <div className="p-8 text-center rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)]">
          <Layers className="w-8 h-8 text-[var(--text-muted)] mx-auto mb-2 opacity-50" />
          <h3 className="font-bold text-sm text-[var(--text-main)]" role={loadError ? "alert" : undefined}>
            {loadError
              ? "Unable to load the stock universe"
              : stockList.length === 0
              ? "Loading stock universe..."
              : "No matching assets found"}
          </h3>
          <p className="text-xs text-[var(--text-muted)] mt-1">
            {loadError
              ? "The Explore API is unavailable. Please try again shortly."
              : stockList.length === 0
              ? "Fetching live scores and regime data."
              : "Try adjusting your search query or switching sector filters."}
          </p>
        </div>
      )}

      {/* Pro Tools: Strategy Backtester Toggle */}
      <ProToolsBacktester />

      {/* 360 Stock Intelligence Profile Modal */}
      <StockProfileModal
        symbol={activeModalSymbol}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </div>
  );
};
