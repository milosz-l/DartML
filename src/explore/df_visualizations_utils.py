from io import BytesIO

import matplotlib.pyplot as plt


def clear_fig_cache() -> None:
    """
    Clears matplotlib's figure cache.
    """
    plt.clf()
    plt.close()


def fig_to_buf(fig) -> bytes:
    """
    Converts a matplotlib figure to a bytes buffer.
    """
    buf = BytesIO()
    fig.savefig(buf, format="png")
    clear_fig_cache()
    data = buf.getvalue()
    return data
