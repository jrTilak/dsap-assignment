from __future__ import annotations

import inspect
import json
import shutil
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


ROOT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT_DIR / "output"
DATA_PATH = ROOT_DIR / "data.json"
TEMPLATE_PATH = ROOT_DIR / "template.tex"


# Input: n, sample index array
# Output: unit impulse values
def unit_impulse(n):
    signal = np.where(n == 0, 1, 0)
    return signal


# Input: x, sample index array
# Output: unit step values
def unit_step_function(x):
    signal = np.where(x >= 0, 1, 0)
    return signal


# Input: x, sample index array
# Output: unit ramp values
def unit_ramp_function(x):
    signal = np.where(x >= 0, x, 0)
    return signal


# Input: n, decay factor a, angular frequency omega
# Output: complex exponential values
def complex_exponential_function(n, a, omega):
    signal = np.exp((a + 1j * omega) * n)
    return signal


# Input: n, positive growth factor a
# Output: increasing real exponential values
def real_exponential_function_increasing(n, a):
    signal = np.exp(a * n)
    return signal


# Input: n, positive decay factor a
# Output: decreasing real exponential values
def real_exponential_function_decreasing(n, a):
    signal = np.exp(-a * n)
    return signal


# Input: n, rectangular width
# Output: rectangular signal values
def rectangular_signal(n, width):
    signal = np.where((n >= 0) & (n < width), 1, 0)
    return signal


# Input: n, signal period
# Output: sawtooth signal values
def sawtooth_signal(n, period):
    signal = (n % period) / period
    return signal


# Input: n, quantization levels
# Output: quantized PCM signal values
def pcm_signal(n, levels):
    analog_signal = np.sin(2 * np.pi * n / 20)
    quantized_indices = np.round(((analog_signal + 1) / 2) * (levels - 1))
    signal = (2 * quantized_indices / (levels - 1)) - 1
    return signal


SIGNAL_DETAILS = [
    {
        "key": "unit_impulse",
        "name": "Unit Impulse Signal",
        "function": unit_impulse,
        "explanation": (
            "The unit impulse signal has value 1 at the origin and 0 elsewhere."
        ),
        "formula": (
            r"\delta[n] = 1 \text{ for } n = 0"
            "\n"
            r"\delta[n] = 0 \text{ for } n \neq 0"
        ),
        "returns": "The function returns a NumPy array containing 1 only at n = 0.",
    },
    {
        "key": "unit_step",
        "name": "Unit Step Signal",
        "function": unit_step_function,
        "explanation": "The unit step signal changes from 0 to 1 at the origin.",
        "formula": (
            r"u[n] = 1 \text{ for } n \geq 0"
            "\n"
            r"u[n] = 0 \text{ for } n < 0"
        ),
        "returns": "The function returns a NumPy array with 0 before the origin and 1 from the origin onward.",
    },
    {
        "key": "unit_ramp",
        "name": "Unit Ramp Signal",
        "function": unit_ramp_function,
        "explanation": (
            "The unit ramp signal increases linearly after the origin and remains "
            "zero before the origin."
        ),
        "formula": (
            r"r[n] = n \text{ for } n \geq 0"
            "\n"
            r"r[n] = 0 \text{ for } n < 0"
        ),
        "returns": "The function returns a NumPy array that is zero before n = 0 and equal to n after n = 0.",
    },
    {
        "key": "complex_exponential",
        "name": "Complex Exponential Signal",
        "function": complex_exponential_function,
        "explanation": (
            "A complex exponential signal contains real and imaginary components. "
            "It can show oscillation and growth or decay depending on the value "
            "of the exponential factor."
        ),
        "formula": r"x[n] = e^{(a + j\omega)n}",
        "returns": "The function returns a complex NumPy array containing real and imaginary signal values.",
    },
    {
        "key": "real_exponential_increasing",
        "name": "Real Exponential Increasing Signal",
        "function": real_exponential_function_increasing,
        "explanation": (
            "A real exponential signal increases when the exponent factor is positive."
        ),
        "formula": r"x[n] = e^{an}",
        "returns": "The function returns a NumPy array whose values increase exponentially.",
    },
    {
        "key": "real_exponential_decreasing",
        "name": "Real Exponential Decreasing Signal",
        "function": real_exponential_function_decreasing,
        "explanation": (
            "A real exponential signal decreases when the exponent factor is negative."
        ),
        "formula": r"x[n] = e^{-an}",
        "returns": "The function returns a NumPy array whose values decrease exponentially.",
    },
    {
        "key": "rectangular_signal",
        "name": "Rectangular Signal",
        "function": rectangular_signal,
        "explanation": (
            "A rectangular signal has constant amplitude for a fixed duration "
            "and zero value outside that duration."
        ),
        "formula": (
            r"x[n] = 1 \text{ for } 0 \leq n < W"
            "\n"
            r"x[n] = 0 \text{ otherwise}"
        ),
        "returns": "The function returns a NumPy array with value 1 inside the selected width and 0 elsewhere.",
    },
    {
        "key": "sawtooth_signal",
        "name": "Sawtooth Signal",
        "function": sawtooth_signal,
        "explanation": (
            "A sawtooth signal increases linearly during one period and then "
            "drops back to the starting value."
        ),
        "formula": r"x[n] = (n \bmod T) / T",
        "returns": "The function returns a NumPy array containing one repeated rising ramp per period.",
    },
    {
        "key": "pcm_signal",
        "name": "PCM Signal",
        "function": pcm_signal,
        "explanation": (
            "Pulse Code Modulation represents an analog signal using discrete "
            "quantized levels. In this assignment, a sine wave is quantized into "
            "16 levels."
        ),
        "formula": r"q[n] = \operatorname{round}\left(((x[n] + 1) / 2) \times (L - 1)\right)",
        "returns": "The function returns a NumPy array containing quantized sine wave samples.",
    },
]


CODE_INTERFACES = {
    "unit_impulse": "# Input: n, sample index array\n# Output: unit impulse values",
    "unit_step_function": "# Input: x, sample index array\n# Output: unit step values",
    "unit_ramp_function": "# Input: x, sample index array\n# Output: unit ramp values",
    "complex_exponential_function": (
        "# Input: n, decay factor a, angular frequency omega\n"
        "# Output: complex exponential values"
    ),
    "real_exponential_function_increasing": (
        "# Input: n, positive growth factor a\n"
        "# Output: increasing real exponential values"
    ),
    "real_exponential_function_decreasing": (
        "# Input: n, positive decay factor a\n"
        "# Output: decreasing real exponential values"
    ),
    "rectangular_signal": (
        "# Input: n, rectangular width\n"
        "# Output: rectangular signal values"
    ),
    "sawtooth_signal": "# Input: n, signal period\n# Output: sawtooth signal values",
    "pcm_signal": (
        "# Input: n, quantization levels\n"
        "# Output: quantized PCM signal values"
    ),
}


def latex_escape(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(character, character) for character in value)


def latex_lines(value: str) -> str:
    return r"\\ ".join(latex_escape(line) for line in value.splitlines())


def latex_formula_block(formula: str) -> str:
    lines = formula.splitlines()
    if len(lines) == 1:
        return "\\[\n" + lines[0] + "\n\\]"

    aligned_lines = " \\\\\n".join(lines)
    return "\\[\n\\begin{aligned}\n" + aligned_lines + "\n\\end{aligned}\n\\]"


def source_for_report(function) -> str:
    interface = CODE_INTERFACES[function.__name__]
    source = inspect.getsource(function).strip()
    return f"{interface}\n{source}"


def build_signal_sections() -> str:
    sections = []

    for signal_number, detail in enumerate(SIGNAL_DETAILS, start=1):
        code = source_for_report(detail["function"])
        section = rf"""
\subsection*{{{signal_number}. {latex_escape(detail["name"]).upper()}}}

{latex_escape(detail["explanation"])}

{latex_formula_block(detail["formula"])}

\begin{{lstlisting}}[style=pythoncode]
{code}
\end{{lstlisting}}

{latex_escape(detail["returns"])}
""".strip()
        sections.append(section)

    return "\n\n".join(sections)


def build_figure_sections() -> str:
    return r"""
The combined output image below shows all implemented signals in one view. The unit impulse contains one non-zero sample at the origin. The unit step changes from zero to one at the origin. The unit ramp grows linearly after zero. The complex exponential shows oscillating real and imaginary values with decreasing amplitude. The real exponential increasing signal grows with sample index, while the real exponential decreasing signal gradually approaches zero. The rectangular signal stays high for the selected width. The sawtooth signal repeats after each selected period. The PCM signal shows a quantized sinusoidal waveform.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.96\textwidth]{combined_signals.png}
    \caption{Combined output of all implemented signals}
\end{figure}
""".strip()


def load_config() -> dict:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def relative_to_output(path: Path) -> str:
    return path.resolve().relative_to(OUTPUT_DIR.resolve().parent).as_posix()


def build_teacher_line(config: dict) -> str:
    teacher_name = config.get("teacher_name", "").strip()
    if not teacher_name:
        return ""

    return f"    \\item Teacher: {latex_escape(teacher_name)}"


def generate_signal_images() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for old_image in OUTPUT_DIR.glob("*.png"):
        old_image.unlink()

    n_centered = np.arange(-50, 50)
    n_positive = np.arange(100)

    impulse = unit_impulse(n_centered)
    step = unit_step_function(n_centered)
    ramp = unit_ramp_function(n_centered)
    complex_signal = complex_exponential_function(n_positive, a=-0.02, omega=0.2)
    increasing = real_exponential_function_increasing(n_positive, a=0.05)
    decreasing = real_exponential_function_decreasing(n_positive, a=0.05)
    rectangle = rectangular_signal(n_positive, width=20)
    sawtooth = sawtooth_signal(n_positive, period=20)
    pcm = pcm_signal(n_positive, levels=16)

    generate_combined_image(
        [
            (n_centered, impulse, "Unit Impulse"),
            (n_centered, step, "Unit Step"),
            (n_centered, ramp, "Unit Ramp"),
            (n_positive, complex_signal, "Complex Exponential"),
            (n_positive, increasing, "Real Exp. Increasing"),
            (n_positive, decreasing, "Real Exp. Decreasing"),
            (n_positive, rectangle, "Rectangular"),
            (n_positive, sawtooth, "Sawtooth"),
            (n_positive, pcm, "PCM"),
        ]
    )


def generate_combined_image(signals: list[tuple[np.ndarray, np.ndarray, str]]) -> None:
    figure, axes = plt.subplots(3, 3, figsize=(13, 10))

    for axis, (n, y, title) in zip(axes.flat, signals, strict=False):
        if np.iscomplexobj(y):
            axis.plot(n, y.real, label="Real")
            axis.plot(n, y.imag, label="Imaginary")
            axis.legend(fontsize=7)
        else:
            axis.plot(n, y)

        axis.set_title(title)
        axis.set_xlabel("n")
        axis.set_ylabel("Amplitude")
        axis.grid(True)

    for axis in axes.flat[len(signals) :]:
        axis.axis("off")

    figure.suptitle("Combined Output of All Implemented Signals", fontsize=16)
    figure.tight_layout(rect=(0, 0, 1, 0.96))
    figure.savefig(OUTPUT_DIR / "combined_signals.png", dpi=300)
    plt.close(figure)


def render_report_tex(config: dict) -> Path:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    logo_path = ROOT_DIR / config["logo_path"]
    if not logo_path.exists():
        raise FileNotFoundError(f"Logo file not found: {logo_path}")

    replacements = {
        "{{UNIVERSITY_NAME}}": latex_escape(config["university_name"]),
        "{{INSTITUTE_NAME}}": latex_escape(config["institute_name"]),
        "{{CAMPUS_NAME}}": latex_escape(config["campus_name"]),
        "{{ASSIGNMENT_NUMBER}}": latex_escape(config["assignment_number"]),
        "{{ASSIGNMENT_TITLE}}": latex_escape(config["assignment_title"]),
        "{{STUDENT_NAME}}": latex_escape(config["student_name"]),
        "{{ROLL_NUMBER}}": latex_escape(config["roll_number"]),
        "{{DEPARTMENT_NAME}}": latex_escape(config["department_name"]),
        "{{CAMPUS_ADDRESS}}": latex_lines(config["campus_address"]),
        "{{SUBJECT_NAME}}": latex_escape(config["subject_name"]),
        "{{TEACHER_LINE}}": build_teacher_line(config),
        "{{DATE}}": latex_escape(config["date"]),
        "{{LOGO_PATH}}": "../" + relative_to_output(logo_path),
        "{{SIGNAL_SECTIONS}}": build_signal_sections(),
        "{{FIGURE_SECTIONS}}": build_figure_sections(),
    }

    rendered = template
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)

    tex_path = OUTPUT_DIR / "final-report.tex"
    tex_path.write_text(rendered, encoding="utf-8")
    return tex_path


def find_latex_command(tex_path: Path) -> list[str]:
    if shutil.which("tectonic"):
        return ["tectonic", tex_path.name]

    if shutil.which("latexmk"):
        return ["latexmk", "-pdf", "-interaction=nonstopmode", tex_path.name]

    if shutil.which("pdflatex"):
        return ["pdflatex", "-interaction=nonstopmode", tex_path.name]

    raise RuntimeError(
        "No LaTeX compiler found. Install tectonic, latexmk, or pdflatex."
    )


def compile_pdf(tex_path: Path) -> Path:
    command = find_latex_command(tex_path)
    subprocess.run(command, cwd=OUTPUT_DIR, check=True)

    if command[0] == "pdflatex":
        subprocess.run(command, cwd=OUTPUT_DIR, check=True)

    pdf_path = OUTPUT_DIR / "final-report.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"LaTeX did not generate {pdf_path}")

    return pdf_path


def main() -> None:
    config = load_config()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating combined signal preview image...")
    generate_signal_images()

    print("Writing LaTeX report...")
    tex_path = render_report_tex(config)

    print("Compiling final PDF...")
    pdf_path = compile_pdf(tex_path)

    print(f"Final report generated: {pdf_path}")


if __name__ == "__main__":
    main()
