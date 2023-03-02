import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_histogram(df, column_name):
    plt.hist(df[column_name])
    plt.title(f'Histogram of {column_name}')
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    plt.show()


def plot_boxplot(df, column_name):
    plt.boxplot(df[column_name])
    plt.title(f'Boxplot of {column_name}')
    plt.ylabel(column_name)
    plt.show()


def plot_scatterplot(df, x_column_name, y_column_name):
    plt.scatter(df[x_column_name], df[y_column_name])
    plt.title(f'Scatterplot of {x_column_name} vs. {y_column_name}')
    plt.xlabel(x_column_name)
    plt.ylabel(y_column_name)
    plt.show()


def plot_corr_heatmap(df):
    corr = df.corr()
    sns.heatmap(corr, cmap='coolwarm', annot=True)
    plt.title('Correlation Heatmap')
    plt.show()
