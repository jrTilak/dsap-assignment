from signals.complex_exponential_signal import complex_exponential
from signals.pcm_signal import pcm_signal
from signals.real_exponential_signal import real_exponential_decreasing
from signals.rectangular_signal import rectangular_signal
from signals.sawtooth_waveform import sawtooth_waveform
from signals.unit_impulse_signal import unit_impulse
from signals.unit_ramp_signal import unit_ramp
from signals.unit_step_signal import unit_step


def main():
    print("===== DSAP Assignment =====")
    print("1. Unit Impulse Signal")
    print("2. Unit Step Signal")
    print("3. Unit Ramp Signal")
    print("4. Complex Exponential Signal")
    print("5. Real Exponential Signal (Decreasing)")
    print("6. Rectangular Signal")
    print("7. Sawtooth Waveform")
    print("8. PCM (Pulse Code Modulation) Signal")
    print("===========================")

    choice = input("Choose an option (1-8): ")

    if choice not in {str(number) for number in range(1, 9)}:
        print("Invalid option. Please choose a number from 1 to 8.")
        print("Exit from program")
        return

    # n_start = int(input("Enter the starting value: "))
    # n_end = int(input("Enter the ending value: "))

    if choice == "1":
        unit_impulse(-50, 50)

    elif choice == "2":
        unit_step(-50, 50)

    elif choice == "3":
        unit_ramp(-50, 50)

    elif choice == "4":
        complex_exponential(-50, 50)

    elif choice == "5":
        real_exponential_decreasing(-50, 50)

    elif choice == "6":
        rectangular_signal(-50, 50)

    elif choice == "7":
        sawtooth_waveform(0, 10)

    elif choice == "8":
        pcm_signal(0, 10)

    print("Exit from program")


if __name__ == "__main__":
    main()
