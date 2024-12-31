import os

# Zdefiniuj oczekiwaną strukturę projektu
expected_structure = {
    'src': {
        'app.py': 'file',
        'database': {
            '__init__.py': 'file',
            'config.py': 'file',
            'models.py': 'file'
        },
        'web': {
            '__init__.py': 'file',
            'views.py': 'file',
            'forms.py': 'file'
        },
        'templates': {
            'index.html': 'file',
            'receipt_list.html': 'file',
            'upload.html': 'file',
            'verify.html': 'file',
            'errors': {
                '404.html': 'file',
                '403.html': 'file',
                '500.html': 'file'
            }
        }
    },
    'migrations': 'dir',
    'requirements.txt': 'file',
    'run.py': 'file'
}

def check_structure(base_path, structure, missing_items, prefix=''):
    """
    Rekurencyjnie sprawdza strukturę katalogów i plików.

    :param base_path: Ścieżka bazowa do sprawdzenia.
    :param structure: Oczekiwana struktura jako słownik.
    :param missing_items: Lista do przechowywania brakujących elementów.
    :param prefix: Prefiks dla ścieżki (używane w rekurencji).
    """
    for name, type_ in structure.items():
        path = os.path.join(base_path, name)
        full_path = os.path.join(prefix, name)
        if type_ == 'file':
            if not os.path.isfile(path):
                missing_items.append(f'Brakujący plik: {full_path}')
        elif type_ == 'dir':
            if not os.path.isdir(path):
                missing_items.append(f'Brakujący katalog: {full_path}')
        elif isinstance(type_, dict):
            if not os.path.isdir(path):
                missing_items.append(f'Brakujący katalog: {full_path}')
            else:
                check_structure(path, type_, missing_items, full_path)
        else:
            missing_items.append(f'Nieznany typ dla: {full_path}')

def main():
    # Ustaw ścieżkę bazową na aktualny katalog
    base_path = os.getcwd()
    missing_items = []

    print("Sprawdzanie struktury katalogów projektu...\n")
    check_structure(base_path, expected_structure, missing_items)

    if not missing_items:
        print("Struktura katalogów jest poprawna. Wszystkie pliki i katalogi są na miejscu.")
    else:
        print("Znaleziono brakujące elementy:")
        for item in missing_items:
            print(f" - {item}")

if __name__ == "__main__":
    main()