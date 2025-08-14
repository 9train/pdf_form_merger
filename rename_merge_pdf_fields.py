# rename_merge_pdf_fields.py
# Renames PDF form field IDs so they don't collide when merged,
# then writes one merged PDF per student folder.
#
# Field rename format: "{file_stem}__{original_field_name}"
# e.g. "Hansen_Ava0_page2__Final Grade"
#
# Keeps forms editable and sets /NeedAppearances = true for rendering.

import re
import sys
import argparse
from pathlib import Path
from typing import List
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, TextStringObject, DictionaryObject, BooleanObject

def natural_key(s: str):
    """
    Return a key that compares safely by tagging each token with its type:
    (0, int_value) for digits, (1, lower_string) for text.
    This avoids int<->str comparisons during sorting.
    """
    parts = re.findall(r'\d+|\D+', s)
    key = []
    for t in parts:
        if t.isdigit():
            key.append((0, int(t)))
        else:
            key.append((1, t.lower()))
    return tuple(key)

def rename_fields_on_page(page, prefix: str) -> int:
    """Rename all /T names on a page's widget annotations using a prefix."""
    count = 0
    if "/Annots" not in page:
        return count
    for annot_ref in page["/Annots"]:
        annot = annot_ref.get_object()
        # Only rename if it's a widget with a field name
        if annot.get("/Subtype") == "/Widget" and annot.get("/T"):
            old = annot["/T"]
            # Convert to plain string safely
            old_str = str(old)
            new_name = f"{prefix}__{old_str}"
            annot.update({NameObject("/T"): TextStringObject(new_name)})
            count += 1
    return count

def process_student_folder(student_dir: Path, output_dir: Path) -> Path:
    """Process all PDFs in one student's folder and produce one merged PDF."""
    pdfs = sorted([p for p in student_dir.glob("*.pdf")], key=lambda p: natural_key(p.name))
    if not pdfs:
        return None

    writer = PdfWriter()
    total_fields = 0

    for pdf_path in pdfs:
        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            total_fields += rename_fields_on_page(page, prefix=pdf_path.stem)
            writer.add_page(page)

    # Ensure NeedAppearances so field values render after merge
    acroform = writer._root_object.get("/AcroForm")
    if acroform is None:
        acroform = DictionaryObject()
        writer._root_object.update({NameObject("/AcroForm"): acroform})
    acroform.update({NameObject("/NeedAppearances"): BooleanObject(True)})

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{student_dir.name}_merged_renamed.pdf"
    with open(out_path, "wb") as f:
        writer.write(f)

    print(f"[OK] {student_dir.name}: merged {len(pdfs)} PDF(s), renamed {total_fields} field(s)")
    return out_path

def main():
    parser = argparse.ArgumentParser(description="Rename PDF form fields and merge per student folder.")
    parser.add_argument("--input", default="input", help="Folder containing one subfolder per student")
    parser.add_argument("--output", default="output", help="Folder to write merged PDFs to")
    args = parser.parse_args()

    input_root = Path(args.input)
    output_root = Path(args.output)

    if not input_root.exists():
        print(f"Input folder not found: {input_root}")
        sys.exit(1)

    # If the user put PDFs directly in input/ with no subfolders, treat input/ as one student
    student_folders: List[Path] = [d for d in input_root.iterdir() if d.is_dir()]
    if not student_folders:
        # No subfolders? Process input/ as a single "student"
        out = process_student_folder(input_root, output_root)
        if out:
            print(f"Saved: {out}")
        return

    # Process each subfolder as one student
    for student_dir in sorted(student_folders, key=lambda p: p.name.lower()):
        out = process_student_folder(student_dir, output_root)
        if out:
            print(f"Saved: {out}")

if __name__ == "__main__":
    main()
