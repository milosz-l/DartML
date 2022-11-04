import streamlit as st


# Train Model
st.title("Train Model")

# choose type of problem
# problem_type = st.sidebar.selectbox(
problem_type = st.selectbox(
    'Choose problem type',
    ('regression', 'classification')
)

# choose algorithms
if problem_type == 'regression':
    algorithms = ['Linear Regression', 'Ridge Regression', 'Lasso Regression', 'SVM', 'Random Forest', 'XGBoost']
else:
    algorithms = ['Logistic Regression', 'Naive Bayes', 'KNN', 'Random Forest', 'SVM']

algorithms_to_compare = st.multiselect(
    "Choose algorithms", algorithms, algorithms[-4:-2]
)
