import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from src.explore.df_visualizations import plot_corr_heatmap
import time

# Transform Data
st.title("Explore Data")

if 'df' in st.session_state:
    # show uploaded df
    st.write('Uploaded DataFrame:')
    st.write(st.session_state['df'])

    # calculate correlation heatmap if not done yet
    start_time = time.time()
    if 'heatmap_fig' not in st.session_state:
        st.session_state['heatmap_fig'] = plot_corr_heatmap(st.session_state['df'])
    st.write('Correlation heatmap:')
    st.pyplot(st.session_state['heatmap_fig'])
    end_time = time.time()
    st.write(f'Showing the above plot took {end_time - start_time:.2f}s')

    # calculate pairplot if not done yet
    # if 'pairplot_fig' not in st.session_state:
    #     # st.session_state['pairplot_fig'] = plt.figure(figsize=(16, 16))
    #     st.session_state['pairplot_fig'] = sns.pairplot(st.session_state['df'])
    # st.write('Pairplot:')
    # st.pyplot(st.session_state['pairplot_fig'])
