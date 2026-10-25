# Server-Side Quantitative ML Computation with Asynchronous ASGI Gateway

**Status:** accepted

## Context
Running complex matrix algebra (Ledoit-Wolf shrinkage, hierarchical clustering, Gaussian Mixture Models, quantile regression) directly on client mobile devices causes thermal throttling, battery drain, and inconsistent execution times across diverse smartphone hardware.

## Decision
All quantitative and econometric computations are executed server-side via Python 3.12 (scikit-learn, scipy, numpy, pandas) wrapped in an asynchronous FastAPI ASGI gateway. The React client acts as a high-performance reactive presentation shell communicating via JSON REST endpoints and Server-Sent Events (SSE).

## Consequences
- Guaranteed sub-200ms optimization execution regardless of client device specifications.
- Protects proprietary model architectures and weighting logic from client-side reverse engineering.
