"""
A unit impulse signal is a signal that is zero everywhere except at the origin (t = 0), where it's value is unit, and its integral over the entire real line is equal to one.

https://www.tutorialspoint.com/signals_and_systems/unit_impulse_signal.htm

"""

import numpy as np
import matplotlib.pyplot as plt


def unit_impulse(n_start, n_end):
    n = np.arange(n_start, n_end + 1)
    delta = (n == 0).astype(int)

    plt.figure(figsize=(8, 4))
    plt.stem(n, delta)

    plt.title(
        "Unit Impulse Signal\n"
        "Zero at every sample except for a single value at the origin"
    )
    plt.xlabel("n")
    plt.ylabel("δ[n]")

    plt.xticks(np.arange(n_start, n_end + 1, 10))
    plt.yticks([0, 1])
    plt.ylim(-0.1, 1.2)

    plt.grid(True)
    plt.tight_layout()
    plt.show()
