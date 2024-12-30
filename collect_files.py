import os
from pathlib import Path
from datetime import datetime

def scan_project_structure(root_dir):
    """Zwraca słownik, w którym kluczami są katalogi, a wartościami listy plików."""
    project_structure = {}
    for root, _, files in os.walk(root_dir):
        root_path = Path(root)
        if files:
            project_structure[root_path] = [root_path / file for file in files]
    return project_structure

def save_files_by_directory(project_structure, output_dir):
    """Zapisuje zawartość plików do osobnych plików dla każdego katalogu."""
    for directory, files in project_structure.items():
        relative_dir = directory.relative_to(root_dir)
        output_file_path = output_dir / f"{relative_dir.as_posix().replace('/', '_')}_files.txt"
        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        with output_file_path.open('w', encoding='utf-8') as f:
            f.write(f"=== Directory: {directory} ===\n\n")

            for file_path in files:
                f.write(f"\n{'=' * 80}\n")
                f.write(f"File: {file_path}\n")
                f.write(f"{'=' * 80}\n\n")

                try:
                    with file_path.open('r', encoding='utf-8') as source_file:
                        f.write(source_file.read())
                except Exception as e:
                    f.write(f"[ERROR] Could not read file: {file_path}\n")
                    f.write(f"Error: {str(e)}\n")

        print(f"Saved: {output_file_path}")

def save_project_structure_to_file(project_structure, output_file_path):
    """Zapisuje strukturę projektu do jednego pliku."""
    with output_file_path.open('w', encoding='utf-8') as f:
        for directory, files in project_structure.items():
            f.write(f"Directory: {directory}\n")
            for file in files:
                f.write(f"    {file}\n")
            f.write("\n")
    print(f"Project structure saved in: {output_file_path}")

if __name__ == "__main__":
    # Parametry
    root_dir = Path("C:/Users/marci/Documents/GitHub/receipts-manager")
    output_dir = Path("exports")
    
    # Tworzenie katalogu wyjściowego
    output_dir.mkdir(parents=True, exist_ok=True)

    # Skanowanie struktury projektu
    print(f"Scanning project directory: {root_dir}")
    project_structure = scan_project_structure(root_dir)

    # Zapisanie zawartości plików do osobnych plików dla każdego katalogu
    save_files_by_directory(project_structure, output_dir)

    # Zapisanie struktury projektu
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_project_structure_to_file(project_structure, output_dir / f'project_structure_{timestamp}.txt')
