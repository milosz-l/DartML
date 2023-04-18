# import regression models
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import LinearSVR
from sklearn.ensemble import RandomForestRegressor

# import classification models
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


regression_models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(),
    "Lasso Regression": Lasso(),
    "Linear SVC (Support Vector Regressor)": LinearSVR(),
    "Random Forest Regressor": RandomForestRegressor(),
}

classification_models = {
    "Logistic Regression": LogisticRegression(),
    "Naive Bayes Classifier": GaussianNB(),
    "KNN": KNeighborsClassifier(),
    "Random Forest Classifier": RandomForestClassifier(),
    "SVC (Support Vector Classifier)": SVC(),
}
