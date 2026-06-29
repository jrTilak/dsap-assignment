# Lab 1 Report Generator

Generates a complete DSAP Assignment 1 PDF report using Python, Matplotlib, and LaTeX.

## Requirements

- Python
- NumPy
- Matplotlib
- A LaTeX compiler such as `tectonic` or `pdflatex`

On Arch Linux:

```bash
sudo pacman -S tectonic
```

## Run

From the repository root:

```bash
uv run python lab1-report-generator/generate_report.py
```

Final PDF:

```text
lab1-report-generator/output/final-report.pdf
```

Edit `data.json` to change student details, title, department, logo path, date, and other report metadata.
