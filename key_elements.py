import os
import json

def clean_path(line):
    # Usuwa niepotrzebne znaki, takie jak "├──" i białe spacje
    return line.replace("├──", "").replace("│", "").replace("└──", "").strip()

def extract_key_files_content(file_path, output_format="txt"):
    # Kluczowe pliki do wyciągnięcia zawartości
    key_files = [
        "run.py", "error_handlers.py", "config.py", ".env", ".env.example", "index.html", "receipts.db",
        "app.log", "pytest.log"
    ]

    output_data = {}

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Przeglądanie zawartości kluczowych plików
        for line in lines:
            clean_line = clean_path(line)
            if any(clean_line.endswith(key_file) for key_file in key_files):
                if os.path.isfile(clean_line):
                    try:
                        if clean_line.endswith(".db"):
                            output_data[clean_line] = "Binary file - skipped content extraction"
                        else:
                            with open(clean_line, "r", encoding="utf-8") as key_file:
                                content = key_file.read()
                                output_data[clean_line] = content
                    except Exception as e:
                        print(f"Nie udało się odczytać pliku {clean_line}: {e}")
                else:
                    print(f"Plik nie istnieje: {clean_line}")

        # Zapis danych do pliku
        if output_format == "txt":
            with open("key_files_content.txt", "w", encoding="utf-8") as output_file:
                for key, value in output_data.items():
                    output_file.write(f"--- {key} ---\n")
                    output_file.write(value + "\n\n")
        elif output_format == "json":
            with open("key_files_content.json", "w", encoding="utf-8") as output_file:
                json.dump(output_data, output_file, indent=4, ensure_ascii=False)

        print(f"Zawartość kluczowych plików została zapisana do key_files_content.{output_format}")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")


# Ścieżka do pliku zawierającego strukturę katalogów
file_path = "directory_tree.txt"
extract_key_files_content(file_path, output_format="txt")
