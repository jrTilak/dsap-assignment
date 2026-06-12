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

    plt.title("Unit Ramp Signal")
    plt.xlabel("n")
    plt.ylabel("r[n]")

    plt.xticks(np.arange(n_start, n_end + 1, 1))
    plt.yticks(np.arange(0, 3, 1))

    plt.grid(True)
    plt.tight_layout()
    plt.show()
