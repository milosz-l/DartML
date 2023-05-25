import streamlit as st
from src.model.RegressionTrainer import RegressionTrainer
from src.model.ClassificationTrainer import ClassificationTrainer
from src.model.Models import regression_models, classification_models
from sklearn.model_selection import train_test_split


# Train Model
st.title("🤖 Model")

if "target_column_name" not in st.session_state:
    st.write("You need to choose a target columnt first! Please go to Modify tab.")
else:
    # print selected target column
    st.write(f"Selected target column = {st.session_state.target_column_name}")

    # choose type of problem
    # problem_type = st.sidebar.selectbox(
    problem_type = st.selectbox("Choose problem type", ("regression", "classification"))

    # choose models
    if problem_type == "regression":
        models_names = list(regression_models.keys())
    else:
        models_names = list(classification_models.keys())

    chosen_models_names = st.multiselect("Choose models", models_names, models_names[-4:-2])

    if st.button("train"):
        # prepare data
        df = st.session_state.df
        target_column_name = st.session_state.target_column_name
        y = df[target_column_name]
        X = df.drop(columns=target_column_name)
        X = X.select_dtypes(include="number")  # take only numerical columns
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # train models
        scores_dict = {}
        if problem_type == "regression":
            models_dict = regression_models
            models = [models_dict[model_name] for model_name in chosen_models_names]
            for model in models:
                trainer = RegressionTrainer(model)
                trainer.fit(X_train, y_train)
                scores_dict[model.__class__.__name__] = trainer.score(X_test, y_test)
        else:
            models_dict = classification_models
            models = [models_dict[model_name] for model_name in chosen_models_names]
            for model in models:
                trainer = ClassificationTrainer(model)
                trainer.fit(X_train, y_train)
                scores_dict[model.__class__.__name__] = trainer.score(X_test, y_test)

        st.write("## Scores")  # TODO: change to automatic
        max_score = max(scores_dict.values())
        for model_name, score in scores_dict.items():
            # st.write(f'{model_name}: {score}')
            st.metric(model_name, score, score - max_score)
