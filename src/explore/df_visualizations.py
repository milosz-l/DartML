import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time

FIG_WIDTH = 16
FIG_HEIGHT = 16


def plot_histogram(df, column_name):
    start_time = time.time()
    fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    plt.hist(df[column_name])
    end_time = time.time()
    plt.title(f'Histogram of {column_name} ({end_time - start_time:.2f} s)')
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    return fig


def plot_boxplot(df, column_name):
    start_time = time.time()
    fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    plt.boxplot(df[column_name])
    end_time = time.time()
    plt.title(f'Boxplot of {column_name} ({end_time - start_time:.2f} s)')
    plt.ylabel(column_name)
    return fig


def plot_scatterplot(df, x_column_name, y_column_name):
    start_time = time.time()
    fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    plt.scatter(df[x_column_name], df[y_column_name])
    end_time = time.time()
    plt.title(f'Scatterplot of {x_column_name} vs. {y_column_name} ({end_time - start_time:.2f} s)')
    plt.xlabel(x_column_name)
    plt.ylabel(y_column_name)
    return fig


def plot_corr_heatmap(df):
    start_time = time.time()
    fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, square=True, cmap='RdYlGn', annot=True, fmt=".2f", linewidth=0.5)
    end_time = time.time()
    plt.title(f'Correlation Heatmap ({end_time - start_time:.2f} s)')
    return fig


def plot_pairplot(df):
    start_time = time.time()
    # fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    g = sns.pairplot(df)
    end_time = time.time()
    g.fig.suptitle(f'Pairplot ({end_time - start_time:.2f} s)')
    return g.fig
