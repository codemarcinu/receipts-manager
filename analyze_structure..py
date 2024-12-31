import os

def analyze_file(file_path, extensions=None, target_directories=None):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Filtruj pliki według rozszerzenia
        if extensions:
            files_with_extensions = [
                line.strip() for line in lines
                if not line.strip().endswith('/') and any(line.strip().endswith(ext) for ext in extensions)
            ]
            print(f"Liczba plików o wybranych rozszerzeniach ({', '.join(extensions)}): {len(files_with_extensions)}")
            for file in files_with_extensions[:10]:  # Wyświetl 10 pierwszych
                print(f" - {file}")

        # Filtruj pliki w określonych katalogach
        if target_directories:
            files_in_directories = [
                line.strip() for line in lines
                if any(line.strip().startswith(dir_path) for dir_path in target_directories)
            ]
            print(f"Liczba plików w wybranych katalogach: {len(files_in_directories)}")
            for file in files_in_directories[:10]:  # Wyświetl 10 pierwszych
                print(f" - {file}")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")


# Ścieżka do pliku
file_path = "directory_structure.txt"  # Zmień na pełną ścieżkę do pliku

# Rozszerzenia plików do wyszukania
extensions = ['.html', '.js', '.css', '.txt', '.py', '.log', '.json', '.env']

# Katalogi do wyszukania (np. zaczynające się od "src/" lub "public/")
target_directories = ['src/', 'public/']

# Wywołaj funkcję analizy
analyze_file(file_path, extensions, target_directories)
