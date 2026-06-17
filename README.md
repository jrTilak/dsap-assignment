# DSAP Assignment

- [Unit Impulse Signal](signals/unit_impulse_signal.py)
- [Unit Step Signal](signals/unit_step_signal.py)
- [Unit Ramp Signal](signals/unit_ramp_signal.py)
- [Complex Exponential Signal](signals/complex_exponential_signal.py)
- [Decreasing Real Exponential Signal](signals/real_exponential_signal.py)
- [Rectangular Signal](signals/rectangular_signal.py)
- [Sawtooth Waveform](signals/sawtooth_waveform.py)
- [PCM (Pulse Code Modulation) Signal](signals/pcm_signal.py)

## How to run

### 1. Install uv

Linux or macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone the assignment

```bash
git clone https://github.com/jrTilak/dsap-assignment.git
cd dsap-assignment
```

### 3. Install dependencies

```bash
uv sync
```

This installs the required Python version and project dependencies, including
NumPy and Matplotlib.

### 4. Run the program

```bash
uv run python main.py
```

GitHub: [jrTilak/dsap-assignment](https://github.com/jrTilak/dsap-assignment)
