"""Economically Constrained Gaussian Mixture & Markov Switching Regime Classifier."""

from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

from app.core.models import MarketRegimeType, RegimeProbabilities


REGIME_METADATA: Dict[MarketRegimeType, Dict[str, str]] = {
    MarketRegimeType.LOW_VOLATILITY_BULL: {
        "id": "0",
        "name": "Low-Volatility Bull",
        "description": "Steady upward price drift with muted realized and implied volatility. Optimal for momentum and growth equities.",
        "recommended_strategy": "Overweight High-Beta Growth & Momentum Equities; Full equity allocation.",
    },
    MarketRegimeType.HIGH_VOLATILITY_BEAR: {
        "id": "1",
        "name": "High-Volatility Bear",
        "description": "Negative price drift with sharp volatility spikes and elevated India VIX. High risk of severe drawdowns.",
        "recommended_strategy": "Defensive Capital Protection; Overweight FMCG, Healthcare, Cash & Low-Beta assets.",
    },
    MarketRegimeType.SIDEWAYS_CONSOLIDATION: {
        "id": "2",
        "name": "Sideways Consolidation",
        "description": "Mean-reverting, range-bound market with moderate volatility and negligible directional trend.",
        "recommended_strategy": "Quality Value, High Dividend Yield, and Mean-Reversion factor baskets.",
    },
}


class MarketRegimeClassifier:
    """Economically constrained regime classifier combining GMM density and macro-economic boundaries.
    
    Economic state constraints:
    - Bull: mu > 0, sigma <= median vol, VIX low/moderate (momentum rallies stay Bull).
    - Bear: mu < 0, sigma > median vol, VIX elevated.
    - Sideways: |mu| <= threshold, range-bound consolidation.
    """

    def __init__(self, n_components: int = 3, random_state: int = 42):
        self.n_components = n_components
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.gmm = GaussianMixture(
            n_components=n_components,
            covariance_type="full",
            random_state=random_state,
            max_iter=200,
            n_init=3,
        )
        self.is_fitted = False
        self.cluster_to_regime: Dict[int, MarketRegimeType] = {}
        self.feature_columns: List[str] = []
        self.median_vol: float = 0.16
        self.median_vix: float = 16.0

    def fit(self, X: pd.DataFrame) -> "MarketRegimeClassifier":
        """Fit clustering and establish economically constrained state mapping."""
        if X.empty or len(X) < self.n_components:
            raise ValueError(f"Insufficient data to fit regime classifier (samples: {len(X)})")

        self.feature_columns = list(X.columns)
        X_scaled = self.scaler.fit_transform(X)
        self.gmm.fit(X_scaled)

        # Store macro distribution medians for economic constraints
        vol_col = "realized_vol_20d" if "realized_vol_20d" in X.columns else None
        vix_col = "vix_level" if "vix_level" in X.columns else None
        if vol_col and not X[vol_col].dropna().empty:
            self.median_vol = float(X[vol_col].median())
        if vix_col and not X[vix_col].dropna().empty:
            self.median_vix = float(X[vix_col].median())

        # Compute cluster centroids in original feature space
        centroids = self.scaler.inverse_transform(self.gmm.means_)
        centroids_df = pd.DataFrame(centroids, columns=self.feature_columns)

        # Economically constrained cluster assignment:
        # 1. Bear cluster: Lowest return, elevated vol and VIX.
        # 2. Bull cluster: Highest return (rallies belong here), positive drift.
        # 3. Sideways cluster: Intermediate return close to zero, moderate vol.
        ret_col = "log_return_20d" if "log_return_20d" in centroids_df.columns else centroids_df.columns[0]

        # Calculate economic scores prioritizing return drift over naive return/vol ratio
        cluster_metrics = []
        for c_idx in range(self.n_components):
            c_ret = float(centroids_df.loc[c_idx, ret_col])
            c_vol = float(centroids_df.loc[c_idx, vol_col]) if vol_col else 0.15
            c_vix = float(centroids_df.loc[c_idx, vix_col]) if vix_col else 16.0
            cluster_metrics.append({
                "idx": c_idx,
                "ret": c_ret,
                "vol": c_vol,
                "vix": c_vix,
            })

        # Sort clusters strictly by return drift: highest = Bull, lowest = Bear, middle = Sideways
        # If returns are identical, lower vol is favored
        sorted_clusters = sorted(cluster_metrics, key=lambda m: (m["ret"], -m["vol"]), reverse=True)

        bull_cluster = sorted_clusters[0]["idx"]
        bear_cluster = sorted_clusters[-1]["idx"]
        sideways_cluster = sorted_clusters[1]["idx"]

        self.cluster_to_regime = {
            bull_cluster: MarketRegimeType.LOW_VOLATILITY_BULL,
            bear_cluster: MarketRegimeType.HIGH_VOLATILITY_BEAR,
            sideways_cluster: MarketRegimeType.SIDEWAYS_CONSOLIDATION,
        }

        self.is_fitted = True
        return self

    def _format_input(self, X: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
        if isinstance(X, pd.Series):
            df = X.to_frame().T
        else:
            df = X.copy()
        if self.feature_columns:
            for col in self.feature_columns:
                if col not in df.columns:
                    df[col] = 0.0
            df = df[self.feature_columns]
        return df.fillna(0.0).replace([np.inf, -np.inf], 0.0)

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        """Predict calibrated posterior probabilities regularized with Bayesian Dirichlet prior."""
        if not self.is_fitted:
            raise RuntimeError("Classifier must be fitted before predict_proba()")

        formatted_df = self._format_input(X)
        X_scaled = self.scaler.transform(formatted_df)

        # Raw GMM density probabilities
        raw_proba = self.gmm.predict_proba(X_scaled)
        raw_proba = np.nan_to_num(raw_proba, nan=1.0 / self.n_components, posinf=1.0, neginf=0.0)

        # Invert cluster_to_regime
        regime_to_cluster = {v: k for k, v in self.cluster_to_regime.items()}
        bull_idx = regime_to_cluster[MarketRegimeType.LOW_VOLATILITY_BULL]
        bear_idx = regime_to_cluster[MarketRegimeType.HIGH_VOLATILITY_BEAR]
        side_idx = regime_to_cluster[MarketRegimeType.SIDEWAYS_CONSOLIDATION]

        # Extract economic indicators for each row
        ret_col = "log_return_20d" if "log_return_20d" in formatted_df.columns else formatted_df.columns[0]
        vol_col = "realized_vol_20d" if "realized_vol_20d" in formatted_df.columns else None
        vix_col = "vix_level" if "vix_level" in formatted_df.columns else None

        returns = formatted_df[ret_col].values
        vols = formatted_df[vol_col].values if vol_col else np.full(len(returns), self.median_vol)
        vixes = formatted_df[vix_col].values if vix_col else np.full(len(returns), self.median_vix)

        n_samples = len(returns)
        adjusted_proba = np.zeros((n_samples, 3), dtype=np.float64)

        for i in range(n_samples):
            r = returns[i]
            v = vols[i]
            vx = vixes[i]

            p_bull = raw_proba[i, bull_idx]
            p_bear = raw_proba[i, bear_idx]
            p_side = raw_proba[i, side_idx]

            # Economically grounded state likelihoods
            if r >= 0.04 and vx <= 22.0:
                # Strong bullish expansion rally: positive drift, subdued VIX
                w_bull = 0.80 + min(0.15, (r - 0.04) * 2.0)
                w_side = max(0.05, 1.0 - w_bull - 0.02)
                w_bear = 0.02
            elif r <= -0.04 and (vx > 18.0 or v > self.median_vol):
                # Strong bearish contraction: sharp negative drift, elevated VIX
                w_bear = 0.80 + min(0.15, (-r - 0.04) * 2.0)
                w_side = max(0.05, 1.0 - w_bear - 0.02)
                w_bull = 0.02
            elif abs(r) <= 0.020 and vx < 22.0:
                # Sideways rangebound consolidation
                w_side = 0.70
                w_bull = 0.15 + (0.10 if r > 0 else 0.0)
                w_bear = 0.15 + (0.10 if r < 0 else 0.0)
            else:
                # Moderate transition zone: blend raw GMM probabilities with return drift
                raw_b = max(1e-4, float(raw_proba[i, bull_idx]))
                raw_br = max(1e-4, float(raw_proba[i, bear_idx]))
                raw_s = max(1e-4, float(raw_proba[i, side_idx]))
                raw_tot = raw_b + raw_br + raw_s
                w_bull = raw_b / raw_tot
                w_bear = raw_br / raw_tot
                w_side = raw_s / raw_tot

                if r > 0:
                    w_bull *= (1.0 + min(2.0, r * 15.0))
                    w_bear *= max(0.2, 1.0 - r * 10.0)
                elif r < 0:
                    w_bear *= (1.0 + min(2.0, -r * 15.0))
                    w_bull *= max(0.2, 1.0 + r * 10.0)

            # Re-normalize pre-prior weights
            w_sum = w_bull + w_bear + w_side
            if w_sum > 0:
                w_bull /= w_sum
                w_bear /= w_sum
                w_side /= w_sum
            else:
                w_bull, w_bear, w_side = 1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0

            # Dirichlet prior regularization to prevent probability saturation collapse
            # Prior weights: Bull=0.15, Sideways=0.10, Bear=0.08 (market base rate reflecting long-run equity risk premium)
            alpha_bull = 0.15
            alpha_side = 0.10
            alpha_bear = 0.08
            alpha_total = alpha_bull + alpha_side + alpha_bear

            # Bayesian posterior smoothing: (w_k + alpha_k) / (1 + sum(alpha))
            reg_bull = (w_bull + alpha_bull) / (1.0 + alpha_total)
            reg_bear = (w_bear + alpha_bear) / (1.0 + alpha_total)
            reg_side = (w_side + alpha_side) / (1.0 + alpha_total)

            # Strict normalization to 1.0
            total_reg = reg_bull + reg_bear + reg_side
            adjusted_proba[i, 0] = reg_bull / total_reg
            adjusted_proba[i, 1] = reg_bear / total_reg
            adjusted_proba[i, 2] = reg_side / total_reg

        out = pd.DataFrame(index=X.index)
        out[MarketRegimeType.LOW_VOLATILITY_BULL.value] = adjusted_proba[:, 0]
        out[MarketRegimeType.HIGH_VOLATILITY_BEAR.value] = adjusted_proba[:, 1]
        out[MarketRegimeType.SIDEWAYS_CONSOLIDATION.value] = adjusted_proba[:, 2]

        return out

    def predict(self, X: pd.DataFrame) -> List[MarketRegimeType]:
        """Predict regime labels for a DataFrame of features based on maximum posterior probability."""
        if not self.is_fitted:
            raise RuntimeError("Classifier must be fitted before predict()")

        proba_df = self.predict_proba(X)
        regimes = [
            MarketRegimeType.LOW_VOLATILITY_BULL,
            MarketRegimeType.HIGH_VOLATILITY_BEAR,
            MarketRegimeType.SIDEWAYS_CONSOLIDATION,
        ]
        cols = [r.value for r in regimes]

        max_cols = proba_df[cols].idxmax(axis=1)
        return [MarketRegimeType(val) for val in max_cols]

    def predict_single(self, X: Union[pd.DataFrame, pd.Series]) -> MarketRegimeType:
        """Predict regime for a single feature vector."""
        if isinstance(X, pd.Series):
            df = X.to_frame().T
        else:
            df = X
        labels = self.predict(df)
        return labels[0]

    def get_regime_info(self, regime: MarketRegimeType) -> Dict[str, str]:
        """Get descriptive metadata and strategy recommendation for a regime."""
        return REGIME_METADATA.get(regime, {})
