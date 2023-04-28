import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time
import streamlit as st
from src.utils.timer import add_timer_note
import numpy as np
from io import BytesIO


def clear_fig_cache():
    plt.clf()
    plt.close()


def fig_to_buf(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    clear_fig_cache()
    data = buf.getvalue()
    return data
