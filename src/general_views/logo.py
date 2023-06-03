import streamlit as st


def show_logo():
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
