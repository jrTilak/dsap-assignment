"""
A unit ramp signal is a type of signal that starts at zero and increases linearly with time.

https://www.geeksforgeeks.org/electronics-engineering/unit-ramp-signal/
"""

import numpy as np
import matplotlib.pyplot as plt


def unit_ramp(n_start, n_end):
    n = np.arange(n_start, n_end + 1)
    r = np.where(n >= 0, n, 0)  # if n>=0 use n, else 0

    plt.figure(figsize=(8, 4))
    plt.stem(n, r)

    plt.title(
        "Unit Ramp Signal\n"
        "Starts at the origin and increases steadily with each sample"
    )
    plt.xlabel("n")
    plt.ylabel("r[n]")

    plt.xticks(np.arange(n_start, n_end + 1, 10))
    plt.ylim(-0.5, max(1, n_end) + 1)

    plt.grid(True)
    plt.tight_layout()
    plt.show()
