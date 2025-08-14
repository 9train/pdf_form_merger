# pdf_form_merger
PDF Form Field Renamer &amp; Merger A Python tool that renames form field names in multiple PDFs to prevent data overwriting, then merges them into a single PDF per student while preserving all filled data. Ideal for combining multi-page student reports, grade sheets, or any form-based PDFs without losing information.


# 📝 PDF Form Field Renamer & Merger

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Made with pdfrw](https://img.shields.io/badge/made%20with-pdfrw-orange)](https://pypi.org/project/pdfrw/)

A Python utility that **renames PDF form field IDs** so that no two pages share the same field names, preventing value overwrites when merging.  
Perfect for **student reports, multi-page forms, and datasets** that must keep **all original data intact** after merging.  

---

## ✨ Features
- 🔄 **Unique Field IDs** — prevents data from being overwritten during merges.
- 📄 **Merge Multiple PDFs** — combines pages into a single file.
- 🖋 **Preserves Form Data** — keeps all filled values.
- 🎯 **Beginner-Friendly** — works with simple drag-and-drop workflow.
- ⚡ **Batch Processing** — easily modify and merge multiple PDFs per student.
- 🖌 **Keeps Formatting** — filled data still displays correctly (`NeedAppearances` set to `true`).

---

## 📂 Example Use Cases
- Combine multiple student grade reports into a single file.
- Merge multi-page application forms without losing individual page data.
- Consolidate filled PDF forms from different templates.

---

## 🚀 Installation
1. **Install Python 3.8+**  
   [Download here](https://www.python.org/downloads/).

2. **Clone this repository**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/pdf-field-renamer.git
   cd pdf-field-renamer
3. Install dependencies:
pip install pdfrw


🛠 Usage
📖 Beginner Setup Guide (Step-by-Step)
This section is written so even if you’ve never coded before, you can run this script.

1️⃣ Install Python
Go to python.org/downloads and download Python 3.8 or higher.
Windows: During installation, check the box "Add Python to PATH".
Mac: Python usually comes pre-installed, but update it if it’s too old.

2️⃣ Get the Script
Click the green Code button on this repo’s GitHub page.
Select Download ZIP.
Extract the ZIP file to a folder on your computer.

3️⃣ Put Your PDFs in the input Folder
Inside the project folder, you will see a folder named input.
Put all the PDFs you want to merge inside this folder.

Example:
input/
├── StudentName0.pdf
├── StudentName1.pdf
├── StudentName2.pdf
└── StudentName3.pdf

4️⃣ Open a Terminal or Command Prompt
Windows: Press Windows Key + R, type cmd, press Enter.
Mac: Press Command + Space, type terminal, press Enter.
VS Code: You can also open the folder in VS Code and press Ctrl + `` (backtick) to open the terminal.

5️⃣ Navigate to Your Project Folder
Type:
cd path/to/your/folder

Example:
cd Desktop/pdf-field-renamer

6️⃣ Install the Required Library
pip install pdfrw

7️⃣ Run the Script
Type:
python rename_merge_pdfs.py

If your system uses python3 instead:
python3 rename_merge_pdfs.py

8️⃣ Get Your Result
The script will create an output folder.
Your merged PDF will be there:

output/
└── merged_unique.pdf

-------------------Screenshots--------------------------

📄 Example Script (rename_merge_pdfs.py):
from pdfrw import PdfReader, PdfWriter, PdfName, PdfObject
import os

def rename_fields(input_files, output_file):
    writer = PdfWriter()
    for page_num, pdf_file in enumerate(input_files):
        pdf = PdfReader(pdf_file)
        if pdf.Root.AcroForm and '/Fields' in pdf.Root.AcroForm:
            for field in pdf.Root.AcroForm.Fields:
                if '/T' in field:
                    field_name = str(field.T)[1:-1]
                    new_name = f"{os.path.basename(pdf_file)}__p{page_num}__{field_name}"
                    field.T = PdfObject(f"({new_name})")
        writer.addpages(pdf.pages)
    writer.trailer.Root.AcroForm = pdf.Root.AcroForm
    writer.trailer.Root.AcroForm.update(PdfObject('<< /NeedAppearances true >>'))
    writer.write(output_file)

if __name__ == "__main__":
    input_files = sorted([os.path.join("input", f) for f in os.listdir("input") if f.endswith(".pdf")])
    rename_fields(input_files, os.path.join("output", "merged_unique.pdf"))

## 🛠 Troubleshooting

### 1️⃣ Error: `ModuleNotFoundError: No module named 'pdfrw'`
**Cause:** The `pdfrw` library is not installed.  

**Fix:**  
Run this command in your terminal:
pip install pdfrw

If that doesn’t work, try:
python3 -m pip install pdfrw

2️⃣ Error: python: command not found
Cause: Python is not installed or not added to your system’s PATH.

Fix:
Windows: Reinstall Python from python.org and check the box "Add Python to PATH" during setup.
Mac: Install Python via:

brew install python
or download it from python.org.

3️⃣ Error: Permission denied when running the script
Cause: You are trying to write to a protected folder.
Fix: Move your project to a folder you own, such as your Desktop or Documents.

4️⃣ PDF Doesn’t Show Updated Fields After Merging
Cause: Some PDF viewers (especially older ones) don’t refresh form appearances automatically.

Fix:
Open the merged PDF in Adobe Acrobat Reader or Chrome PDF Viewer.

Make sure the script sets /NeedAppearances to true (already included in this script).
📌 Notes
- This script works best for PDFs with editable form fields.
- If you merge without renaming field IDs, data will overwrite between pages.
- You can adapt it for batch processing by looping over student folders.

📜 License
This project is licensed under the MIT License — see the LICENSE file for details.

🤝 Contributing
Pull requests are welcome! If you’d like to improve the script or add features, feel free to fork and submit changes.

💡 Credits
Made with ❤️ using pdfrw.
---





