"""
A unit step signal is a type of signal that is zero for negative time and one for positive time, typically denoted as u(t)

https://www.geeksforgeeks.org/electronics-engineering/unit-step-signal-in-control-system/
"""

import numpy as np
import matplotlib.pyplot as plt


def unit_step(n_start, n_end):
    n = np.arange(n_start, n_end + 1)
    u = (n >= 0).astype(int)  # 1 where n>=0, 0 elsewhere

    plt.figure(figsize=(8, 4))
    plt.stem(n, u)

    plt.title(
        "Unit Step Signal\n"
        "Changes from zero to one at the origin and remains there"
    )
    plt.xlabel("n")
    plt.ylabel("u[n]")

    plt.xticks(np.arange(n_start, n_end + 1, 10))
    plt.yticks([0, 1])
    plt.ylim(-0.1, 1.2)

    plt.grid(True)
    plt.tight_layout()
    plt.show()
