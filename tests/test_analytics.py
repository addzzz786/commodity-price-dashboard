import numpy as np
import pandas as pd
from src.analytics import compute_log_returns, compute_rolling_volatility, compute_correlation_matrix, run_pca

def test_log_returns_shape():
    prices = pd.DataFrame({
        "A": [100, 110, 121, 133, 146],
        "B": [200, 210, 220, 230, 240],
    })

    result = compute_log_returns(prices)
    assert result.shape[0] == 4
   


def test_log_returns_additivity():
    prices = pd.DataFrame({
        "A": [100, 110, 121],
    })

    result = compute_log_returns(prices)
    total = np.log(prices["A"].iloc[2] / prices["A"].iloc[0])
    np.testing.assert_almost_equal(result["A"].sum(), total, decimal=10)
    


def test_rolling_vol_annualisation():
    vol = pd.DataFrame({
        "A": [0.01, -0.01, 0.01, -0.01]
    })
    result = compute_rolling_volatility(vol, window=2)
    expected = 0.01 * np.sqrt(2) * np.sqrt(252)
    np.testing.assert_almost_equal(result["A"].dropna().iloc[0], expected, decimal=10)
    


def test_correlation_diagonal_is_one():
    prices = pd.DataFrame({
        "A": [100, 110, 120],
        "B": [200, 191, 169],
        "C": [158, 145, 168],
    })
    result = compute_correlation_matrix(compute_log_returns(prices))
    np.testing.assert_array_almost_equal(np.diag(result.values), np.ones(3))
   


def test_correlation_is_symmetric():
    prices = pd.DataFrame({
        "A": [100, 110, 120],
        "B": [200, 191, 169],
    })
    result = compute_correlation_matrix(compute_log_returns(prices))
    np.testing.assert_array_almost_equal(result.values, result.T.values)
    


def test_pca_variance_sums_to_one():
    np.random.seed(42)
    log_returns = pd.DataFrame(np.random.randn(100, 3))
    PCA = run_pca(log_returns)
    np.testing.assert_almost_equal(PCA["variance_explained"].sum(), 1.0, decimal=10)
   

def test_pca_components_are_uncorrelated():
    np.random.seed(42)
    log_returns = pd.DataFrame(np.random.randn(100, 3))
    PCA = run_pca(log_returns)
    components = PCA["components"]
    correlation = np.corrcoef(components[:, 0], components[:, 1])[0, 1]
    np.testing.assert_almost_equal(correlation, 0.0, decimal=10)