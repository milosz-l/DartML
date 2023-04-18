import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class ClassificationTrainer(BaseEstimator, ClassifierMixin):
    def __init__(self, model, test_size=0.2):
        self.model = model
        self.test_size = test_size

    def fit(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc}")
        return self

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def score(self, X, y):
        y_pred = self.predict(X)
        return accuracy_score(y, y_pred)


# from sklearn.tree import DecisionTreeClassifier

# clf = DecisionTreeClassifier()
# trainer = ClassificationTrainer(clf)

# trainer.fit(X_train, y_train)

# y_pred = trainer.predict(X_test)
# y_pred_proba = trainer.predict_proba(X_test)
# score = trainer.score(X_test, y_test)
