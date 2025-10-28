# Repo structure and submission instructions

Suggested repository structure (already present files included):

- README.md  — high-level instructions (created)
- requirements.txt — Python deps (created)
- edge_ai_prototype_notebook.ipynb — Colab notebook (created)
- code/ — place implementation scripts, training/eval scripts
- models/ — store trained models (.h5/.tflite)
- data/ — (not committed) dataset pointers and instructions
- docs/ — essays, case study critique, ethics writeup, concept paper
  - smart_agriculture_proposal.md
  - smart_agriculture_diagram.svg
  - ethics_personalized_medicine_300_words.md
  - futuristic_2030_concept.md
  - quantum_simulation_qiskit.py
- presentations/ — pitch deck outline and slides
  - presentations/pitch_deck_outline.md
- results/ — training logs, metrics, confusion matrices

Assembling the final PDF (recommended):
1. Convert notebooks and markdowns to PDF using `jupyter nbconvert` and `pandoc`.
2. Use the following steps on Windows PowerShell (example):

```powershell
# Convert notebook to PDF (requires TeX or use HTML then print to PDF)
jupyter nbconvert --to pdf "edge_ai_prototype_notebook.ipynb"

# Convert markdown files to PDF with pandoc (install pandoc):
pandoc smart_agriculture_proposal.md -o smart_agriculture_proposal.pdf --pdf-engine=xelatex
pandoc ethics_personalized_medicine_300_words.md -o ethics_personalized_medicine_300_words.pdf --pdf-engine=xelatex
pandoc futuristic_2030_concept.md -o futuristic_2030_concept.pdf --pdf-engine=xelatex

# Merge PDFs (requires pdftk or use PowerShell and .NET tools). Example using PDFtk (install required):
pdftk edge_ai_prototype_notebook.pdf smart_agriculture_proposal.pdf ethics_personalized_medicine_300_words.pdf futuristic_2030_concept.pdf cat output final_report.pdf
```

If you prefer a single-step approach with pandoc to create a combined PDF report:

```powershell
pandoc -s -o final_report.pdf edge_ai_prototype_notebook.ipynb smart_agriculture_proposal.md ethics_personalized_medicine_300_words.md futuristic_2030_concept.md -V geometry:margin=1in --pdf-engine=xelatex
```

Posting to PLP Academy Community
- Export `final_report.pdf` and upload it to the PLP Academy Community article submission page. Include a short description, repo link (GitHub), and tags: #AIFutureAssignment, #EdgeAI, #QuantumAI.

Notes & tips
- Ensure large data is not committed to repo; provide download instructions or a small sample dataset instead.
- Include a `LICENSE` and `CONTRIBUTING.md` if working with others.
