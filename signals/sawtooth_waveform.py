"""
A sawtooth waveform increases linearly during each period and then drops
abruptly before repeating.
"""

import matplotlib.pyplot as plt
import numpy as np


def sawtooth_waveform(t_start, t_end):
    time = np.linspace(t_start, t_end, 1000)
    period = 1.0
    signal = 2 * ((time / period) - np.floor(0.5 + time / period))

    plt.figure(figsize=(9, 4))
    plt.plot(time, signal)

    plt.title(
        "Sawtooth Waveform\n"
        "Rises steadily and then drops suddenly in a repeating pattern"
    )
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.xlim(t_start, t_end)
    plt.ylim(-1.2, 1.2)

    plt.grid(True)
    plt.tight_layout()
    plt.show()
