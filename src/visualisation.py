import matplotlib.pyplot as plt
import pandas as pd

def plot_prices(prices: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots()
    ax.set_title("Commodity Price History (Rebased to 1)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Rebased Price (1 = start)")
    for column in prices.columns:
        ax.plot(prices.index, prices[column], label=column)
    ax.legend()
    plt.show()
    return fig


def plot_log_returns(log_returns: pd.DataFrame) -> plt.Figure:
    n = len(log_returns.columns)
    fig, axes = plt.subplots(n, 1, figsize=(12, 8), sharex=True)
    for ax, column in zip(axes, log_returns.columns):
        ax.plot(log_returns.index, log_returns[column], 
                linewidth=0.6, label=column)
        ax.set_ylabel("Log Return")
        ax.set_title(column)
        ax.axhline(y=0, color="black", linewidth=0.5, linestyle="--")
    axes[-1].set_xlabel("Date")
    fig.suptitle("Daily Log Returns", fontsize=13, y=1.01)
    plt.tight_layout()
    plt.show()
    return fig


def plot_rolling_volatility(rolling_vol: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 5))
    for column in rolling_vol.columns:
        ax.plot(rolling_vol.index, rolling_vol[column] * 100, 
                label=column, linewidth=0.8)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    ax.set_title("Rolling 30-Day Annualised Volatility")
    ax.set_xlabel("Date")
    ax.set_ylabel("Annualised Volatility")
    ax.legend()
    plt.tight_layout()
    plt.show()
    return fig


def plot_correlation_heatmap(corr_matrix: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots()
    ax.set_title("Asset Correlation Heatmap")
    ax.set_xticks(range(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns, rotation=45)
    ax.set_yticks(range(len(corr_matrix.columns)))
    ax.set_yticklabels(corr_matrix.columns)

    im = ax.imshow(corr_matrix, cmap="RdYlGn", vmin=-1, vmax=1)

    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix.columns)):
            ax.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}",
                ha="center", va="center")
    
    plt.colorbar(im, ax=ax)
    plt.show()
    return fig

def plot_pca_summary(pca_results: pd.DataFrame) -> plt.Figure:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.bar(range(1, len(pca_results["asset_names"]) + 1), pca_results["variance_explained"])
    ax1.set_xlabel("Components")
    ax1.set_ylabel("Contribution to each Principal Component")
    ax1.set_title("PCA Summary")

    ax2.plot(range(1, len(pca_results["asset_names"]) + 1), pca_results["cumulative_variance"])
    ax2.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax2.axhline(y=0.9, linestyle="--", color="red", linewidth=0.8, label="90% threshold")
    ax2.set_xlabel("Components")
    ax2.set_ylabel("Cumulative contribution of all Components")
    ax2.set_title("Cumulative PCA per Component")
    ax2.legend()
    plt.show()
    return fig



    