from signals.unit_impulse_signal import unit_impulse
from signals.unit_ramp_signal import unit_ramp
from signals.unit_step_signal import unit_step


def main():
    print("===== DSAP Assignment =====")
    print("1. Unit Impulse Signal")
    print("2. Unit Step Signal")
    print("3. Unit Ramp Signal")
    print("===========================")

    choice = input("Choose an option (1-9): ")

    if choice == "1":
        n_start = int(input("Enter start value (negative, e.g. -10): "))
        n_end = int(input("Enter end value (positive, e.g. 10): "))
        unit_impulse(n_start, n_end)

    elif choice == "2":
        n_start = int(input("Enter start value (negative, e.g. -10): "))
        n_end = int(input("Enter end value (positive, e.g. 10): "))
        unit_step(n_start, n_end)

    elif choice == "3":
        n_start = int(input("Enter start value (negative, e.g. -10): "))
        n_end = int(input("Enter end value (positive, e.g. 10): "))
        unit_ramp(n_start, n_end)

    else:
        print("Option not available yet.")

    print("Exit from program")


if __name__ == "__main__":
    main()
