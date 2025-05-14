import os
import nbformat
import importlib
from glob import glob

def extract_imports_from_notebook(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    imports = set()
    for cell in nb.cells:
        if cell.cell_type != 'code':
            continue
        for line in cell.source.splitlines():
            line = line.strip()
            if line.startswith("import ") or line.startswith("from "):
                parts = line.replace("import", "").replace("from", "").split()
                if parts:
                    pkg = parts[0].split('.')[0]
                    imports.add(pkg)
    return imports

def get_package_version(pkg_name):
    try:
        mod = importlib.import_module(pkg_name)
        return getattr(mod, "__version__", "N/A")
    except ModuleNotFoundError:
        return "NOT INSTALLED"

def main():
    ipynb_files = glob("*.ipynb")
    all_imports = set()

    for file in ipynb_files:
        print(f"Scanning: {file}")
        imports = extract_imports_from_notebook(file)
        all_imports.update(imports)

    print("\n📦 Consolidated package versions:")
    package_versions = {}
    for pkg in sorted(all_imports):
        version = get_package_version(pkg)
        package_versions[pkg] = version
        print(f"{pkg}=={version}")

    # Optional: Save to requirements file
    with open("requirements_from_notebooks.txt", "w") as f:
        for pkg, ver in sorted(package_versions.items()):
            if ver != "NOT INSTALLED":
                f.write(f"{pkg}=={ver}\n")

    print("\n✅ Saved as requirements_from_notebooks.txt")

if __name__ == "__main__":
    main()
