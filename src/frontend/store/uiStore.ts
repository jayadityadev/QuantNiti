import { useAppStore } from "./useAppStore";

export function useUIStore() {
  const store = useAppStore();
  return {
    theme: store.theme,
    toggleTheme: () => store.setTheme(store.theme === "dark" ? "light" : "dark"),
    setTheme: store.setTheme,
    isOnboarded: store.isOnboarded,
    setOnboarded: (val: boolean) => store.setIsOnboarded(val),
    activeTab: store.activeTab,
    setActiveTab: store.setActiveTab,
    activeModal: store.activeModal,
    modalPayload: store.modalPayload,
    openModal: store.openModal,
    closeModal: store.closeModal,
  };
}
