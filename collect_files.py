import os
import shutil
from pathlib import Path
from datetime import datetime


def collect_project_files(output_file='project_files.txt'):
    """Collect and save content of key project files."""
    key_files = [
        # Konfiguracja
        'src/config.py',
        '.env',
        'requirements.txt',
        'setup.py',
        'package.json',
        'tailwind.config.js',
        'postcss.config.js',
        
        # Backend
        'src/web/__init__.py',
        'src/database/__init__.py',
        'src/database/models.py',
        'src/web/views.py',
        'src/web/forms.py',
        'src/web/error_handlers.py',
        
        # Frontend
        'src/web/static/js/ReceiptVerificationForm.js',
        'src/web/static/js/ReceiptVerificationForm.jsx',
        'src/web/static/css/style.css',
        'src/web/static/css/main.css',
        
        # Szablony
        'src/web/templates/base.html',
        'src/web/templates/verify.html',
        'src/web/templates/receipt_list.html',
        'src/web/templates/upload.html',
        'src/web/templates/errors/404.html',
        'src/web/templates/errors/500.html',
        
        # Testy
        'tests/conftest.py',
        'tests/test_api.py',
        'tests/test_database.py',
        'tests/test_ocr.py'
    ]

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'project_files_{timestamp}.txt'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== Project Files Collection ({timestamp}) ===\n\n")

        for file_path in key_files:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"File: {file_path}\n")
            f.write(f"{'=' * 80}\n")

            try:
                with open(file_path, 'r', encoding='utf-8') as source_file:
                    content = source_file.read()
                    f.write(content)
            except FileNotFoundError:
                f.write(f"[ERROR] File not found: {file_path}\n")
            except Exception as e:
                f.write(f"[ERROR] Could not read file: {file_path}\n")
                f.write(f"Error: {str(e)}\n")

            f.write("\n")

    print(f"Files collected in: {output_file}")

    # Dodatkowo, zapisz strukturę projektu
    try:
        import subprocess
        tree_output = subprocess.check_output(['tree']).decode('utf-8')
        with open('tree', 'w', encoding='utf-8') as f:
            f.write(tree_output)
        print("Project structure saved in 'tree' file")
    except Exception as e:
        print(f"Could not save project structure: {str(e)}")


if __name__ == "__main__":
    collect_project_files()