import streamlit as st


def show_logo() -> None:
    """
    Shows the app logo on top of the sidebar.
    """
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "🎯 DartML";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
