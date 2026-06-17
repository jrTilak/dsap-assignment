"""
A decreasing real exponential signal becomes smaller as the sample index
increases. Multiplication by the unit step makes it zero for n < 0.
"""

import matplotlib.pyplot as plt
import numpy as np


def real_exponential_decreasing(n_start, n_end):
    n = np.arange(n_start, n_end + 1)
    base = 0.7
    signal = np.where(n >= 0, base**n, 0.0)

    plt.figure(figsize=(8, 4))
    plt.stem(n, signal)

    plt.title(
        "Decreasing Real Exponential Signal\n"
        "Begins at its highest value and gradually approaches zero"
    )
    plt.xlabel("n")
    plt.ylabel("x[n] = (0.7)ⁿu[n]")
    plt.xticks(np.arange(n_start, n_end + 1, 10))
    plt.ylim(-0.05, 1.1)

    plt.grid(True)
    plt.tight_layout()
    plt.show()
