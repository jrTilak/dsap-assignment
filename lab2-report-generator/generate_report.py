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


# Input: n, rectangular width
# Output: rectangular signal values
def rectangular_signal(n, width):
    signal = np.where((n >= 0) & (n < width), 1, 0)
    return signal


# Input: signal x, scaling factor A
# Output: amplitude-scaled signal
def amplitude_scaling(x, A):
    y = A * x
    return y


# Input: n, signal x, scaling factor a
# Output: time-scaled signal values
def time_scaling(n, x, a):
    lookup = dict(zip(n, x, strict=True))
    y = np.array([lookup.get(a * index, 0) for index in n])
    return y


# Input: n, signal x, delay value k
# Output: delayed signal values
def time_delay(n, x, k):
    lookup = dict(zip(n, x, strict=True))
    y = np.array([lookup.get(index - k, 0) for index in n])
    return y


# Input: n, signal x, advance value k
# Output: advanced signal values
def time_advance(n, x, k):
    lookup = dict(zip(n, x, strict=True))
    y = np.array([lookup.get(index + k, 0) for index in n])
    return y


# Input: n, signal x
# Output: time-flipped signal values
def time_flipping(n, x):
    lookup = dict(zip(n, x, strict=True))
    y = np.array([lookup.get(-index, 0) for index in n])
    return y


# Input: two signals x1 and x2
# Output: sample-wise multiplied signal
def time_domain_multiplication(x1, x2):
    y = x1 * x2
    return y


# Input: two signals x1 and x2
# Output: inverse FFT of multiplied spectra
def frequency_domain_multiplication(x1, x2):
    X1 = np.fft.fft(x1)
    X2 = np.fft.fft(x2)
    y = np.fft.ifft(X1 * X2).real
    return y


# Input: two signals x and h
# Output: linear convolution values
def convolution_operation(x, h):
    y = np.convolve(x, h, mode="full")
    return y


# Input: two signals x and y
# Output: correlation values
def correlation_operation(x, y):
    rxy = np.correlate(x, y, mode="full")
    return rxy


OPERATION_DETAILS = [
    {
        "name": "Amplitude Scaling",
        "function": amplitude_scaling,
        "explanation": "Amplitude scaling changes the height or strength of a signal without changing its time position.",
        "formula": r"y[n] = A x[n]",
        "parameters": r"Here, \(A = 2\).",
        "returns": "The function returns the amplitude-scaled signal values.",
    },
    {
        "name": "Time Scaling",
        "function": time_scaling,
        "explanation": "Time scaling compresses or expands a signal along the time axis.",
        "formula": r"y[n] = x[an]",
        "parameters": r"Here, \(a = 2\).",
        "returns": "The function returns the time-scaled signal values.",
    },
    {
        "name": "Time Shifting: Time Delay",
        "function": time_delay,
        "explanation": "Time delay shifts a signal to the right by a selected number of samples.",
        "formula": r"y[n] = x[n - k]",
        "parameters": r"Here, \(k = 5\).",
        "returns": "The function returns the delayed signal values.",
    },
    {
        "name": "Time Shifting: Time Advance",
        "function": time_advance,
        "explanation": "Time advance shifts a signal to the left by a selected number of samples.",
        "formula": r"y[n] = x[n + k]",
        "parameters": r"Here, \(k = 5\).",
        "returns": "The function returns the advanced signal values.",
    },
    {
        "name": "Time Flipping",
        "function": time_flipping,
        "explanation": "Time flipping reverses a signal around the vertical axis.",
        "formula": r"y[n] = x[-n]",
        "parameters": "",
        "returns": "The function returns the time-flipped signal values.",
    },
    {
        "name": "Multiplication in the Time Domain",
        "function": time_domain_multiplication,
        "explanation": "Multiplication in the time domain multiplies two signals sample by sample.",
        "formula": r"y[n] = x_1[n] \times x_2[n]",
        "parameters": "The base rectangular signal and a delayed rectangular signal are used.",
        "returns": "The function returns the sample-wise product of two signals.",
    },
    {
        "name": "Multiplication in the Frequency Domain",
        "function": frequency_domain_multiplication,
        "explanation": "Frequency domain multiplication is performed by multiplying the FFT values of two signals.",
        "formula": r"Y[k] = X_1[k] \times X_2[k]",
        "parameters": "The inverse FFT is used to show the result in the time domain.",
        "returns": "The function returns the time-domain signal obtained from multiplied spectra.",
    },
    {
        "name": "Convolution",
        "function": convolution_operation,
        "explanation": "Convolution combines two signals and is commonly used to represent the response of a system.",
        "formula": r"y[n] = x[n] * h[n]",
        "parameters": "The base rectangular signal and a delayed rectangular signal are used.",
        "returns": "The function returns the linear convolution of two signals.",
    },
    {
        "name": "Correlation",
        "function": correlation_operation,
        "explanation": "Correlation measures the similarity between two signals as one signal is shifted over another.",
        "formula": r"r_{xy}[n] = \operatorname{corr}(x[n], y[n])",
        "parameters": "The base rectangular signal and a delayed rectangular signal are used.",
        "returns": "The function returns the correlation values of two signals.",
    },
]


CODE_INTERFACES = {
    "amplitude_scaling": (
        "# Input: signal x, scaling factor A\n"
        "# Output: amplitude-scaled signal"
    ),
    "time_scaling": (
        "# Input: n, signal x, scaling factor a\n"
        "# Output: time-scaled signal values"
    ),
    "time_delay": (
        "# Input: n, signal x, delay value k\n"
        "# Output: delayed signal values"
    ),
    "time_advance": (
        "# Input: n, signal x, advance value k\n"
        "# Output: advanced signal values"
    ),
    "time_flipping": "# Input: n, signal x\n# Output: time-flipped signal values",
    "time_domain_multiplication": (
        "# Input: two signals x1 and x2\n"
        "# Output: sample-wise multiplied signal"
    ),
    "frequency_domain_multiplication": (
        "# Input: two signals x1 and x2\n"
        "# Output: inverse FFT of multiplied spectra"
    ),
    "convolution_operation": (
        "# Input: two signals x and h\n"
        "# Output: linear convolution values"
    ),
    "correlation_operation": (
        "# Input: two signals x and y\n"
        "# Output: correlation values"
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
    return "\\[\n" + formula + "\n\\]"


def source_for_report(function) -> str:
    interface = CODE_INTERFACES[function.__name__]
    source = inspect.getsource(function).strip()
    return f"{interface}\n{source}"


def build_operation_sections() -> str:
    sections = []

    for operation_number, detail in enumerate(OPERATION_DETAILS, start=1):
        code = source_for_report(detail["function"])
        parameter_text = f"\n\n{detail['parameters']}" if detail["parameters"] else ""
        section = rf"""
\subsection*{{{operation_number}. {latex_escape(detail["name"]).upper()}}}

{latex_escape(detail["explanation"])}

{latex_formula_block(detail["formula"])}
{parameter_text}

\begin{{lstlisting}}[style=pythoncode]
{code}
\end{{lstlisting}}

{latex_escape(detail["returns"])}
""".strip()
        sections.append(section)

    return "\n\n".join(sections)


def build_figure_sections() -> str:
    return r"""
The combined output image below shows the original signal and all implemented signal operation results in one view.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{combined_operations.png}
    \caption{Combined output of all implemented signal operations}
\end{figure}
""".strip()


def load_config() -> dict:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def relative_to_output(path: Path) -> str:
    return path.resolve().relative_to(OUTPUT_DIR.resolve().parent).as_posix()


def plot_signal(n, y, title, ylabel, output_path):
    plt.figure(figsize=(8, 4.5))
    plt.plot(n, y)
    plt.title(title)
    plt.xlabel("Sample index (n)")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def generate_signal_operation_images() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for old_image in OUTPUT_DIR.glob("*.png"):
        old_image.unlink()

    n = np.arange(-50, 51)
    x = rectangular_signal(n, width=20)
    x2 = time_delay(n, x, k=10)

    scaled = amplitude_scaling(x, A=2)
    time_scaled = time_scaling(n, x, a=2)
    delayed = time_delay(n, x, k=5)
    advanced = time_advance(n, x, k=5)
    flipped = time_flipping(n, x)
    time_multiplied = time_domain_multiplication(x, x2)
    frequency_multiplied = frequency_domain_multiplication(x, x2)
    convolved = convolution_operation(x, x2)
    correlated = correlation_operation(x, x2)

    n_full = np.arange(n[0] + n[0], n[-1] + n[-1] + 1)

    generate_combined_image(
        [
            (n, x, "Original"),
            (n, scaled, "Amplitude Scaling"),
            (n, time_scaled, "Time Scaling"),
            (n, delayed, "Time Delay"),
            (n, advanced, "Time Advance"),
            (n, flipped, "Time Flipping"),
            (n, time_multiplied, "Time Multiplication"),
            (n, frequency_multiplied, "Frequency Multiplication"),
            (n_full, convolved, "Convolution"),
            (n_full, correlated, "Correlation"),
        ]
    )


def generate_combined_image(plots: list[tuple[np.ndarray, np.ndarray, str]]) -> None:
    figure, axes = plt.subplots(4, 3, figsize=(14, 13))

    for axis, (n, y, title) in zip(axes.flat, plots, strict=False):
        axis.plot(n, y)
        axis.set_title(title)
        axis.set_xlabel("n")
        axis.set_ylabel("Amplitude")
        axis.grid(True)

    for axis in axes.flat[len(plots) :]:
        axis.axis("off")

    figure.suptitle("Combined Output of Signal Operations", fontsize=16)
    figure.tight_layout(rect=(0, 0, 1, 0.96))
    figure.savefig(OUTPUT_DIR / "combined_operations.png", dpi=300)
    plt.close(figure)


def render_report_tex(config: dict) -> Path:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    logo_path = ROOT_DIR / config["logo_path"]
    if not logo_path.exists():
        raise FileNotFoundError(f"Logo file not found: {logo_path}")

    replacements = {
        "{{UNIVERSITY_NAME}}": latex_escape(config["university_name"]),
        "{{INSTITUTE_NAME}}": latex_escape(config["institute_name"]),
        "{{DEPARTMENT_NAME}}": latex_escape(config["department_name"]),
        "{{ASSIGNMENT_NUMBER}}": latex_escape(config["assignment_number"]),
        "{{ASSIGNMENT_TITLE}}": latex_escape(config["assignment_title"]),
        "{{STUDENT_NAME}}": latex_escape(config["student_name"]),
        "{{ROLL_NUMBER}}": latex_escape(config["roll_number"]),
        "{{DATE}}": latex_escape(config["date"]),
        "{{LOGO_PATH}}": "../" + relative_to_output(logo_path),
        "{{OPERATION_SECTIONS}}": build_operation_sections(),
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

    raise RuntimeError("No LaTeX compiler found. Install tectonic, latexmk, or pdflatex.")


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

    print("Generating signal operation plots...")
    generate_signal_operation_images()

    print("Writing report...")
    tex_path = render_report_tex(config)

    print("Compiling PDF...")
    pdf_path = compile_pdf(tex_path)

    print(f"Final report generated: {pdf_path}")


if __name__ == "__main__":
    main()
