import matplotlib.pyplot as plt
import pandas as pd


class DataFrameVisualizer:

    def __init__(self, df):
        self.df = df

    def plot_histogram(self, column_name):
        plt.hist(self.df[column_name])
        plt.title(f'Histogram of {column_name}')
        plt.xlabel(column_name)
        plt.ylabel('Frequency')
        plt.show()

    def plot_boxplot(self, column_name):
        plt.boxplot(self.df[column_name])
        plt.title(f'Boxplot of {column_name}')
        plt.ylabel(column_name)
        plt.show()

    def plot_scatterplot(self, x_column_name, y_column_name):
        plt.scatter(self.df[x_column_name], self.df[y_column_name])
        plt.title(f'Scatterplot of {x_column_name} vs. {y_column_name}')
        plt.xlabel(x_column_name)
        plt.ylabel(y_column_name)
        plt.show()
