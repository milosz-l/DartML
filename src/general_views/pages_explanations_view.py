import streamlit as st
from typing import Literal


def show_sample_page_explanation():
    st.markdown(
        """
        In this tab, you can upload your own dataset or use an example **dataset**. After that, you will be able to sample the data and specify the train/test split. All options chosen in this tab will be shown in the sidebar on the left. If you want to restore the default options, just go back to the Explore tab.
        """
    )

def show_explore_page_explanation():
    st.markdown(
        """
        In this tab, you can perform the **Exploratory Data Analysis (EDA)** on your dataset.
        - For **numerical** columns, there is an interactive correlation heatmap, that also allows you not only to see the correlation between the columns, but also to dive deeper into the relationships between these columns.
        - For **categorical** columns, there are bar charts that show the distribution of each unique value in the column.

        The plots are cached, so you can switch between the tabs without waiting for the plots to be generated again. They will be generated once again only if you change the dataset.
        """
    )

def show_modify_and_model_page_explanation():
    st.markdown(
        """
        In this tab, you define the AutoML **model training** configuration:
        - **Target column** - the column that you want to predict.
        - **Problem type** - the type of the problem you want to solve. If left on *auto*, the app will try to infer the problem type based on the target column.
        - **Metric** - the metric that will be used to evaluate the model.
        - **Algorithms to train** - the algorithms that will be used to train the models.
        - **Total time limit** - the total time limit for the AutoML training.
        """
    )

def show_assess_page_explanation():
    st.markdown(
        """
        In this tab you can **evaluate** the trained models. You can see the **leaderboard** with the models ranked by the chosen metric. Depending on the training mode you chose in previous tab, there may be visualizations like:
        - **Features importance plot** that shows the importance of each feature for each model.
        - **Spearman Correlation of Models** heatmap that shows the correlations between the predictions of each model.
        - **Decision trees visualizations**.
        - **SHAP** (SHapley Additive exPlanations) visualizations.

        Whole generated report with visualizations and trained models can be downloaded as a *zip* file.
        """
    )

def show_page_explanation_in_expander(page_title: Literal["sample", "explore", "modify_and_model", "assess"], expanded=False):
    with st.expander("Info", expanded=expanded):
        if page_title == "sample":
            show_sample_page_explanation()
        elif page_title == "explore":
            show_explore_page_explanation()
        elif page_title == "modify_and_model":
            show_modify_and_model_page_explanation()
        elif page_title == "assess":
            show_assess_page_explanation()
        else:
            raise ValueError(f"Unknown page title: {page_title}")