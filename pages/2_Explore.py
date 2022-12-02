import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Transform Data
st.title("Explore Data")

if 'df' in st.session_state:
    # show uploaded df
    st.write('Uploaded DataFrame:')
    st.write(st.session_state['df'])

    # calculate correlation heatmap if not done yet
    # TODO: select features to show on heatmap
    if 'heatmap_fig' not in st.session_state:
        st.session_state['heatmap_fig'] = plt.figure(figsize=(16, 16))
        sns.heatmap(st.session_state['df'].corr(numeric_only=True), square=True, cmap='RdYlGn', annot=True, fmt=".2f", linewidth=0.5)

    # calculate pairplot if not done yet
    # TODO: select kind of pairplot
    # TODO: select optional hue of pairplot
    if 'pairplot_fig' not in st.session_state:
        # st.session_state['pairplot_fig'] = plt.figure(figsize=(16, 16))
        st.session_state['pairplot_fig'] = sns.pairplot(st.session_state['df'])

    # show visualizations
    st.write('Correlation heatmap:')
    st.pyplot(st.session_state['heatmap_fig'])
    st.write('Pairplot:')
    st.pyplot(st.session_state['pairplot_fig'])
