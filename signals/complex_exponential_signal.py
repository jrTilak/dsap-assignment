"""
A complex exponential signal has real and imaginary sinusoidal components:
x[n] = exp(j * omega * n) = cos(omega * n) + j sin(omega * n).
"""

import matplotlib.pyplot as plt
import numpy as np


def complex_exponential(n_start, n_end):
    n = np.arange(n_start, n_end + 1)
    omega = np.pi / 4
    signal = np.exp(1j * omega * n)

    figure, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)

    axes[0].stem(n, signal.real)
    axes[0].set_title("Real Part")
    axes[0].set_ylabel("cos(ωn)")
    axes[0].set_ylim(-1.2, 1.2)
    axes[0].grid(True)

    axes[1].stem(n, signal.imag)
    axes[1].set_title("Imaginary Part")
    axes[1].set_xlabel("n")
    axes[1].set_ylabel("sin(ωn)")
    axes[1].set_ylim(-1.2, 1.2)
    axes[1].set_xticks(np.arange(n_start, n_end + 1, 10))
    axes[1].grid(True)

    figure.suptitle(
        "Complex Exponential Signal\n"
        "A repeating signal with real and imaginary wave components"
    )
    figure.tight_layout(rect=(0, 0, 1, 0.93))
    plt.show()
