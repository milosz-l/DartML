import matplotlib.pyplot as plt
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
