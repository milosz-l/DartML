import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


class RegressionTrainer(BaseEstimator, RegressorMixin):
    def __init__(self, model, test_size=0.2):
        self.model = model
        self.test_size = test_size

    def fit(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error: {mse}')
        return self

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, y):
        y_pred = self.predict(X)
        return mean_squared_error(y, y_pred)


# from sklearn.linear_model import LinearRegression

# reg = LinearRegression()
# trainer = RegressionTrainer(reg)

# trainer.fit(X_train, y_train)

# y_pred = trainer.predict(X_test)
# score = trainer.score(X_test, y_test)
