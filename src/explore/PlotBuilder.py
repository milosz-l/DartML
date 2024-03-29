import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.explore.df_visualizations_utils import clear_fig_cache, fig_to_buf

FIG_WIDTH = 16
FIG_HEIGHT = 16


class PlotBuilder:
    """
    Class used for building matplotlib and seaborn plots for given dataframe.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_histogram(self, column_name: str) -> bytes:
        """
        Returns a histogram for given column.
        """
        start_time = time.time()
        fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        plt.hist(self.df[column_name])
        end_time = time.time()
        plt.title(f"Histogram of {column_name} ({end_time - start_time:.2f} s)")
        plt.xlabel(column_name)
        plt.ylabel("Frequency")
        return fig_to_buf(fig)

    def get_boxplot(self, column_name: str) -> bytes:
        """
        Returns a boxplot for given column.
        """
        start_time = time.time()
        fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        plt.boxplot(self.df[column_name])
        end_time = time.time()
        plt.title(f"Boxplot of {column_name} ({end_time - start_time:.2f} s)")
        plt.ylabel(column_name)
        return fig_to_buf(fig)

    def get_scatterplot(self, x_column_name: str, y_column_name: str) -> bytes:
        """
        Returns a scatterplot for given columns.
        """
        start_time = time.time()
        fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        plt.scatter(self.df[x_column_name], self.df[y_column_name])
        end_time = time.time()
        plt.title(
            f"Scatterplot of {x_column_name} vs. {y_column_name} ({end_time - start_time:.2f} s)"
        )
        plt.xlabel(x_column_name)
        plt.ylabel(y_column_name)
        return fig_to_buf(fig)

    def get_corr_heatmap(self) -> bytes:
        """
        Returns a correlation heatmap.
        """
        start_time = time.time()
        fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        corr = self.df.corr()
        sns.heatmap(
            corr, square=True, cmap="RdYlGn", annot=True, fmt=".2f", linewidth=0.5
        )
        end_time = time.time()
        plt.title(f"Correlation Heatmap ({end_time - start_time:.2f} s)")
        return fig_to_buf(fig)

    def get_pairplot(self) -> bytes:
        """
        Returns a pairplot.
        """
        start_time = time.time()
        # fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        g = sns.pairplot(self.df)
        end_time = time.time()
        g.fig.suptitle(f"Pairplot ({end_time - start_time:.2f} s)")
        return fig_to_buf(g.fig)

    def __del__(self):
        """
        Clears matplotlib's figure cache to avoid memory leaks.
        """
        clear_fig_cache()
