from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
BUILD_DIR = ROOT_DIR / "build" / "cover"
DIST_DIR = ROOT_DIR / "dist"


COVER_CONFIG = {
    "university": "TRIBHUVAN UNIVERSITY",
    "institute": "INSTITUTE OF ENGINEERING",
    "campus": "PURWANCHAL CAMPUS",
    "assignment": "DSAP ASSIGNMENT - 1",
    "title": "IMPLEMENTATION OF BASIC SIGNALS",
    "student_name": "Tilak Thapa",
    "roll_number": "PUR079BCT094",
    "department": "DEPARTMENT OF ELECTRONICS AND COMPUTER ENGINEERING",
    "location": "PURWANCHAL CAMPUS\nDHARAN, SUNSARI",
    "date": "18 JUNE",
    "logo_path": ROOT_DIR / "logo.jpg",
    "output_pdf": DIST_DIR / "lab1_cover.pdf",
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


def build_latex(config: dict) -> str:
    student = (
        f"{latex_escape(config['student_name'])} "
        f"[{latex_escape(config['roll_number'])}]"
    )

    return rf"""
\documentclass[12pt,a4paper]{{article}}
\usepackage[a4paper,top=1.15in,bottom=1in,left=1in,right=1in]{{geometry}}
\usepackage{{graphicx}}

\pagestyle{{empty}}
\setlength{{\parindent}}{{0pt}}

\begin{{document}}
\begin{{titlepage}}
\centering

\vspace*{{0.15in}}

{{\Large\bfseries {latex_escape(config['university'])}\par}}
\vspace{{0.16in}}
{{\large {latex_escape(config['institute'])}\par}}
\vspace{{0.12in}}
{{\large {latex_escape(config['campus'])}\par}}

\vspace{{0.65in}}
\includegraphics[width=1.7in]{{logo.jpg}}

\vspace{{0.75in}}
{{\Large\bfseries {latex_escape(config['assignment'])}\par}}

\vspace{{0.35in}}
{{\Large\bfseries {latex_escape(config['title'])}\par}}

\vspace{{0.7in}}
{{\large\bfseries BY\par}}

\vspace{{0.25in}}
{{\large {student}\par}}

\vfill

{{\large {latex_escape(config['department'])}\par}}
\vspace{{0.14in}}
{{\large {latex_lines(config['location'])}\par}}

\vspace{{0.5in}}
{{\large {latex_escape(config['date'])}\par}}

\end{{titlepage}}
\end{{document}}
""".strip()


def find_latex_command() -> list[str]:
    if shutil.which("latexmk"):
        return ["latexmk", "-pdf", "-interaction=nonstopmode", "cover_page.tex"]

    if shutil.which("pdflatex"):
        return ["pdflatex", "-interaction=nonstopmode", "cover_page.tex"]

    if shutil.which("xelatex"):
        return ["xelatex", "-interaction=nonstopmode", "cover_page.tex"]

    if shutil.which("tectonic"):
        return ["tectonic", "cover_page.tex"]

    raise RuntimeError(
        "No LaTeX compiler found. Install latexmk, pdflatex, xelatex, or tectonic."
    )


def generate_cover(config: dict) -> Path:
    logo_path = Path(config["logo_path"])
    output_pdf = Path(config["output_pdf"])

    if not logo_path.exists():
        raise FileNotFoundError(f"Logo file not found: {logo_path}")

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(logo_path, BUILD_DIR / "logo.jpg")

    tex_path = BUILD_DIR / "cover_page.tex"
    tex_path.write_text(build_latex(config), encoding="utf-8")

    command = find_latex_command()
    subprocess.run(command, cwd=BUILD_DIR, check=True)

    generated_pdf = BUILD_DIR / "cover_page.pdf"
    if not generated_pdf.exists():
        raise FileNotFoundError(f"LaTeX did not generate {generated_pdf}")

    shutil.copy2(generated_pdf, output_pdf)
    return output_pdf


if __name__ == "__main__":
    pdf_path = generate_cover(COVER_CONFIG)
    print(f"Cover page generated: {pdf_path}")
