"""
A rectangular signal has a constant non-zero amplitude inside a selected
interval and is zero outside that interval.
"""

import matplotlib.pyplot as plt
import numpy as np


def rectangular_signal(n_start, n_end):
    n = np.arange(n_start, n_end + 1)
    half_width = 10
    signal = (np.abs(n) <= half_width).astype(int)

    plt.figure(figsize=(8, 4))
    plt.stem(n, signal)

    plt.title(
        "Rectangular Signal\n"
        "Has a constant value within a fixed interval and zero outside it"
    )
    plt.xlabel("n")
    plt.ylabel("x[n]")
    plt.xticks(np.arange(n_start, n_end + 1, 10))
    plt.yticks([0, 1])
    plt.ylim(-0.1, 1.2)

    plt.grid(True)
    plt.tight_layout()
    plt.show()
