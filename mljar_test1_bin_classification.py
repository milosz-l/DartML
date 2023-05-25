import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML

df = pd.read_csv(
    "https://raw.githubusercontent.com/pplonski/datasets-for-start/master/adult/data.csv",
    skipinitialspace=True,
)
X_train, X_test, y_train, y_test = train_test_split(df[df.columns[:-1]], df["income"], test_size=0.25)

automl = AutoML(mode="Explain", ml_task="binary_classification")
automl.fit(X_train, y_train)

predictions = automl.predict(X_test)
