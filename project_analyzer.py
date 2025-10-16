"""
Project Analyzer — Extracts a Python project ZIP, 
shows its directory tree, and detects entry Python files.
"""

import os
import shutil
import zipfile
from tkinter import Tk, filedialog
from tree.rptree import DirectoryTree  

def extract_zip(zip_path, extract_to="extracted"):
    """
    Extracts the given ZIP file to a clean folder.
    If an old extracted folder exists, it will be deleted first.
    """
    # 🧹 Clean previous extracted folder if it exists
    if os.path.exists(extract_to):
        shutil.rmtree(extract_to)

    os.makedirs(extract_to, exist_ok=True)

    # 📦 Extract the ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    print(f"\n✅ Extracted successfully to: {os.path.abspath(extract_to)}")
    return extract_to


def find_python_entry_files(folder):
    """
    Searches for main Python entry files like main.py, app.py, etc.
    Returns a fresh list each time.
    """
    entry_candidates = [
        "main.py", "app.py", "run.py", "manage.py", "index.py", "__main__.py"
    ]
    found_entries = []  # ✅ Always start with a clean list

    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower() in entry_candidates:
                full_path = os.path.join(root, file)
                found_entries.append(full_path)

    if found_entries:
        print("\n🚀 Possible Python entry files found:")
        for f in found_entries:
            print(f"   • {f}")
    else:
        print("\n⚠️ No common Python entry file found.")

    return found_entries


def main():
    """
    Main function: lets user pick a ZIP file, extracts it,
    shows its folder structure, and identifies entry Python files.
    """
    # 🗂️ Open file picker dialog
    Tk().withdraw()  # Hide the root tkinter window
    zip_path = filedialog.askopenfilename(
        title="Select a Python Project ZIP file",
        filetypes=[("ZIP files", "*.zip")]
    )

    if not zip_path:
        print("❌ No file selected.")
        return

    print(f"\n📦 Selected file: {zip_path}")

    # 🧳 Extract project
    folder = extract_zip(zip_path)

    print("\n🧩 Directory Structure:\n")

    # 🗂️ Show directory tree (RP Tree)
    try:
        tree = DirectoryTree(folder)
        tree.generate()
    except Exception as e:
        print(f"❌ Error generating directory tree: {e}")

    # 🧭 Identify Python entry files
    find_python_entry_files(folder)


if __name__ == "__main__":
    main()
