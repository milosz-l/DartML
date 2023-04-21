import streamlit as st


# Transform Data
st.title("Modify Data")

if "df" in st.session_state:
    # show uploaded df
    st.write("Uploaded DataFrame:")
    st.write(st.session_state.df)

    # ask for target column name
    columns_list = st.session_state.df.columns.tolist()
    if "target_column_name" in st.session_state:
        if st.session_state.target_column_name in columns_list:
            selectbox_default_index = columns_list.index(st.session_state.target_column_name)
        else:
            selectbox_default_index = 0
        # st.experimental_show(selectbox_default_index)
    else:
        selectbox_default_index = 0
    st.session_state.target_column_name = st.selectbox("Please select target column", columns_list, index=selectbox_default_index)
