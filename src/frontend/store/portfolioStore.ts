import { useAppStore } from "./useAppStore";

export function usePortfolioStore() {
  const store = useAppStore();
  return {
    capital: store.capital,
    setCapital: store.setCapital,
    horizon: store.horizon,
    setHorizon: store.setHorizon,
    riskPersona: store.riskPersona,
    setRiskPersona: store.setRiskPersona,
    regime: store.activeRegime,
    activeRegime: store.activeRegime,
    setActiveRegime: store.setActiveRegime,
    currentBasket: store.currentBasket,
    setCurrentBasket: store.setCurrentBasket,
    activePortfolio: store.activePortfolio,
    portfolios: store.portfolios,
  };
}
