import streamlit as st


# Transform Data
st.title("Modify Data")

if 'df' in st.session_state:
    # show uploaded df
    st.write('Uploaded DataFrame:')
    st.write(st.session_state.df)

    # ask for target column name
    target_column_name = st.selectbox(
        'Please select target column',
        st.session_state.df.columns.tolist()
    )   # TODO: add default if any column had been chosen before
    st.session_state.target_column_name = target_column_name
