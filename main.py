"""
Main launcher for the Project Analyzer tool.
Extracts a ZIP file, shows directory structure,
analyzes all Python files by generating their AST trees,
and reads Python configuration files (requirements.txt, setup.py, pyproject.toml).
"""

import os
import shutil
import zipfile
from tkinter import Tk, filedialog
from tree.rptree import DirectoryTree
from tree.astree import ASTTree


# =========================
# ZIP Extraction
# =========================
def extract_zip(zip_path, extract_to="extracted"):
    """Extracts the given ZIP file into a clean folder."""
    if os.path.exists(extract_to):
        shutil.rmtree(extract_to)
    os.makedirs(extract_to, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    print(f"\n✅ Extracted successfully to: {os.path.abspath(extract_to)}")
    return extract_to


# =========================
# Python Analysis Functions
# =========================
def find_python_entry_files(folder):
    """Searches for main Python entry files."""
    entry_candidates = [
        "main.py", "app.py", "run.py", "manage.py", "index.py", "__main__.py"
    ]
    found_entries = []

    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower() in entry_candidates:
                found_entries.append(os.path.join(root, file))

    if found_entries:
        print("\n🚀 Possible Python entry files found:")
        for f in found_entries:
            print(f"   • {f}")
    else:
        print("\n⚠️ No common Python entry file found.")

    return found_entries


def find_all_python_files(folder):
    """Finds all Python (.py) files in the folder."""
    py_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


def analyze_ast_for_files(py_files):
    """Generates and displays AST for all Python files."""
    if not py_files:
        print("\n⚠️ No Python files found to analyze.")
        return

    for path in py_files:
        print(f"\n📄 Analyzing AST for: {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            tree = ASTTree(code)
            tree.generate()
        except Exception as e:
            print(f"❌ Error analyzing {path}: {e}")



# =========================
# Main Function
# =========================
def main():
    """Main function: extract ZIP, show folder tree, analyze AST, and read Python configs."""
    Tk().withdraw()
    zip_path = filedialog.askopenfilename(
        title="Select a Python Project ZIP file",
        filetypes=[("ZIP files", "*.zip")]
    )

    if not zip_path:
        print("❌ No file selected.")
        return

    print(f"📦 Selected file: {zip_path}")

    # Step 1️⃣: Extract the ZIP
    folder = extract_zip(zip_path)

    # Step 2️⃣: Show directory tree
    print("\n🧩 Directory Structure:\n")
    try:
        tree = DirectoryTree(folder)
        tree.generate()
    except Exception as e:
        print(f"❌ Error generating directory tree: {e}")

    # Step 3️⃣: Read Python configuration files
    print("\n⚙️ Reading Python configuration/setup files...")
    read_requirements(folder)
    read_setup_py(folder)
    check_file(folder, ".py")
    print("\n✅ Configuration reading complete.")

    # Step 4️⃣: Find Python entry files
    find_python_entry_files(folder)

    # Step 5️⃣: Generate AST for all Python files
    print("\n🔍 Generating AST for all Python files...\n")
    py_files = find_all_python_files(folder)
    analyze_ast_for_files(py_files)

    print("\n✅ AST Analysis Complete!\n")


if __name__ == "__main__":
    main()
