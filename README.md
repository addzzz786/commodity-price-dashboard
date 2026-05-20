# Commodity Price Analytics Dashboard

> Quantitative analysis of covariance, volatility, and underlying risk 
> factors across crude oil (WTI), natural gas (Henry Hub), and copper 
> futures — covering January 2020 to May 2026.

---

## Overview

This project builds an end-to-end analytical pipeline for three commodity 
futures markets. Starting from raw price data, it produces rebased price 
comparisons, log return distributions, rolling volatility estimates, a 
correlation matrix, and a full PCA decomposition.

The date range is deliberately chosen to span several major market regimes: 
the COVID-19 demand collapse (2020), the post-pandemic commodity supercycle 
(2021), the Russia-Ukraine energy shock (2022),the 2025-26 tariff 
uncertainty and the Iran-US conflict. 

---

## Mathematical Methods

**Log Returns**  
Raw prices are transformed into log returns: `r_t = ln(P_t / P_{t-1})`.  
Log returns are used rather than simple returns because they are additive 
across time, the multi-period return is simply the sum of single-period 
log returns. They also produce a non-negative, more symmetric distribution, which is a 
prerequisite for many downstream statistical models.

**Rolling Volatility**  
Annualised volatility is estimated as the rolling 30-day standard deviation 
of log returns, scaled by `sqrt(252)`. The square-root-of-time scaling 
follows from the variance of i.i.d. returns scaling linearly with time, 
so standard deviation scales with the square root. This captures 
time-varying volatility clustering - the caveat of the i.i.d. implementation
is that volatility clusters in reality.

**Correlation Matrix**  
The Pearson correlation matrix `ρ_ij = Cov(r_i, r_j) / (σ_i · σ_j)` 
measures linear co-movement between asset pairs, normalised to [-1, 1]. 
The resulting matrix is always symmetric and positive semi-definite,
all eigenvalues are non-negative, which is a necessary condition for 
it to represent a valid covariance structure.

**Principal Component Analysis**  
PCA is implemented from scratch using NumPy eigendecomposition, no 
sklearn. The covariance matrix of standardised returns is decomposed as 
`Σ = V D V^T`, where the columns of V are eigenvectors (principal 
components) and the diagonal of D contains eigenvalues (variance 
explained per component). The data is then projected onto the top k 
eigenvectors, reducing dimensionality while retaining the dominant 
sources of co-movement. In commodity markets, PC1 typically represents 
a broad macro risk factor driving all three assets simultaneously.

---

## Results

### Rebased Price History
![Rebased commodity prices 2020-2026](assets/prices.png)
*Brief interpretation — what do you notice about the price paths?*

### Daily Log Returns
![Daily log returns](assets/log_returns.png)
*Which pair is most correlated and why does that make economic sense?*

### Rolling Volatility
![30-day annualised rolling volatility](assets/rolling_volatility.png)

### Correlation Heatmap
![Pearson correlation matrix](assets/correlation_heatmap.png)

### PCA Summary
![PCA variance explained](assets/pca_summary.png)
*How many components explain 90% of variance? What does that tell you 
about the number of independent risk factors in this market?*

---

## Project Structure

```
commodity-price-dashboard/
├── src/
│   ├── data_loader.py      # Price fetching and caching via yfinance
│   ├── analytics.py        # Mathematical transformations (returns, vol, PCA)
│   └── visualisation.py    # Chart generation via matplotlib
├── notebooks/
│   └── 01_exploration.ipynb  # End-to-end analysis pipeline
├── tests/
│   └── test_analytics.py   # Unit tests for analytical functions
└── requirements.txt
```

---

## How to Run

```bash
git clone https://github.com/YOURUSERNAME/commodity-price-dashboard.git
cd commodity-price-dashboard
python -m venv venv
venv\Scripts\Activate.ps1      # Windows
pip install -r requirements.txt
jupyter notebook notebooks/01_exploration.ipynb
```

---

## Dependencies

- `numpy` — matrix operations and eigendecomposition  
- `pandas` — time series data structures  
- `matplotlib` — visualisation  
- `yfinance` — commodity futures price data  
- `scipy` — statistical functions

