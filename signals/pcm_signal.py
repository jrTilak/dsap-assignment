"""
Pulse Code Modulation (PCM) converts an analog signal into digital data by
sampling, quantizing, and binary encoding it.
"""

import matplotlib.pyplot as plt
import numpy as np


def pcm_signal(t_start, t_end):
    analog_time = np.linspace(t_start, t_end, 1000)
    analog_signal = np.sin(2 * np.pi * analog_time)

    sample_count = 81
    sample_time = np.linspace(t_start, t_end, sample_count)
    sampled_signal = np.sin(2 * np.pi * sample_time)

    bit_depth = 3
    level_count = 2**bit_depth
    quantized_indices = np.rint(
        (sampled_signal + 1) * (level_count - 1) / 2
    ).astype(int)
    quantized_indices = np.clip(quantized_indices, 0, level_count - 1)
    quantized_signal = 2 * quantized_indices / (level_count - 1) - 1

    encoded_samples = [
        format(index, f"0{bit_depth}b") for index in quantized_indices
    ]
    bit_stream = np.array(
        [int(bit) for encoded_sample in encoded_samples for bit in encoded_sample]
    )

    figure, axes = plt.subplots(3, 1, figsize=(10, 9))

    axes[0].plot(analog_time, analog_signal, label="Analog signal")
    axes[0].stem(
        sample_time,
        sampled_signal,
        linefmt="C1-",
        markerfmt="C1o",
        basefmt=" ",
        label="Samples",
    )
    axes[0].set_title("1. Sampling")
    axes[0].set_ylabel("Amplitude")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].stem(sample_time, quantized_signal)
    axes[1].set_title(f"2. Quantization ({level_count} levels)")
    axes[1].set_ylabel("Quantized amplitude")
    axes[1].set_yticks(np.linspace(-1, 1, level_count))
    axes[1].grid(True)

    bit_positions = np.arange(len(bit_stream) + 1)
    extended_bits = np.append(bit_stream, bit_stream[-1])
    axes[2].step(bit_positions, extended_bits, where="post")
    axes[2].set_title(
        f"3. PCM Binary Encoding ({bit_depth} bits per sample)"
    )
    axes[2].set_xlabel("Bit index")
    axes[2].set_ylabel("Bit value")
    axes[2].set_yticks([0, 1])
    axes[2].set_ylim(-0.2, 1.2)
    axes[2].set_xlim(0, len(bit_stream))
    axes[2].grid(True)

    figure.suptitle(
        "Pulse Code Modulation (PCM) Signal\n"
        "Shows how an analog wave is sampled, rounded, and stored as binary data"
    )
    figure.tight_layout(rect=(0, 0, 1, 0.94))
    plt.show()
