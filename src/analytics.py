import numpy as np
import pandas as pd


def compute_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return np.log(prices / prices.shift(1)).dropna()


def compute_rolling_volatility(log_returns: pd.DataFrame, 
                                window: int = 30) -> pd.DataFrame:
    return log_returns.rolling(window=window).std() * np.sqrt(252)


def compute_correlation_matrix(log_returns: pd.DataFrame) -> pd.DataFrame:
    return log_returns.corr()


def run_pca(log_returns: pd.DataFrame, n_components: int = 3) -> dict:
    X = log_returns.values
    X_centred = X - np.mean(X, axis=0)
    X_std = X_centred / X.std(axis=0)
    cov_matrix = np.cov(X_std.T) # Need to transpose X_std so that the rows are the variables (asset_names) & columns are the data points
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    sort_idx = np.argsort(eigenvalues)[::-1] # [::-1] reverses the order so we have the biggest eigenvalue first (descending order)
    eigenvalues = eigenvalues[sort_idx] # 1D array so can index directly
    eigenvectors = eigenvectors[:, sort_idx] # 2D array so need to sort the columns instead of the rows
    variance_explained = eigenvalues / eigenvalues.sum() # converting raw variance into a proportion of total variance
    cumulative_variance = np.cumsum(variance_explained) # running total of proportional variance for each component
    components = X_std @ eigenvectors[:, :n_components] # taking most important eigenvectors and collapsing dimensionality to reduce noise
    return {
        "eigenvalues"           : eigenvalues,
        "eigenvectors"          : eigenvectors,
        "components"            : components,
        "variance_explained"    : variance_explained,
        "cumulative_variance"   : cumulative_variance,
        "asset_names"           : list(log_returns.columns),
        "cov_matrix"            : cov_matrix,
    }

def rebase_prices(prices: pd.DataFrame) -> pd.DataFrame:
    return prices / prices.iloc[0]