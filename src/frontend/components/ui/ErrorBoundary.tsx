import React from "react";
import { AlertTriangle, RotateCcw } from "lucide-react";

export interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
}

/**
 * Catches render-time errors from the routed app so one malformed API field
 * cannot unmount the whole React root into a blank screen.
 */
export class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = { hasError: false };

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    // Keep the detail in the console for support; the user sees a recovery path.
    console.error("Unhandled UI error", error, info.componentStack);
  }

  private handleReload = () => {
    if (typeof window !== "undefined") {
      window.location.reload();
    }
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div
          role="alert"
          className="min-h-screen flex flex-col items-center justify-center gap-4 p-6 bg-[var(--bg-primary)] text-[var(--text-main)] text-center"
        >
          <div className="w-12 h-12 rounded-2xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-500">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <div className="space-y-1.5 max-w-xs">
            <h1 className="text-lg font-bold tracking-tight">
              Something went wrong
            </h1>
            <p className="text-sm text-[var(--text-muted)]">
              This screen hit an unexpected error. Reload to continue, your
              saved data stays on this device.
            </p>
          </div>
          <button
            type="button"
            onClick={this.handleReload}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium text-sm text-white bg-slate-900 hover:bg-slate-800 dark:bg-teal-600 dark:hover:bg-teal-500 shadow-sm transition-colors duration-150 focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:outline-none"
          >
            <RotateCcw className="w-4 h-4" />
            Reload app
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
