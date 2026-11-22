import { HashRouter } from "react-router-dom";
import { ThemeProvider } from "./context/ThemeContext";
import { AppShell } from "./components/layout/AppShell";
import { ErrorBoundary } from "./components/ui/ErrorBoundary";

export default function App() {
  return (
    <ThemeProvider>
      <ErrorBoundary>
        <HashRouter>
          <AppShell />
        </HashRouter>
      </ErrorBoundary>
    </ThemeProvider>
  );
}
