# System Zarządzania Paragonami - Dokumentacja Projektu

## Stan Projektu na dzień 28.12.2024

### Zrealizowane Komponenty

#### 1. Struktura Bazy Danych
- Modele: Receipt, Product, Category w `src.database.models`
- Wykorzystanie SQLAlchemy z podstawowymi relacjami
- System migracji z Flask-Migrate
- Automatyczna inicjalizacja bazy przez skrypt

#### 2. Interfejs Webowy
- Formularze Flask-WTF do weryfikacji danych
- Interfejs listy paragonów z funkcjami weryfikacji i usuwania
- Formularz uploadu nowych paragonów
- Obsługa błędów 404, 500 i 403
- Responsywny interfejs z Bootstrap 5
- Rozpoczęta implementacja Material Design
- Konfiguracja Tailwind CSS (w trakcie)

#### 3. Frontend
- Base template z Bootstrap i Font Awesome
- Szablony dla wszystkich widoków
- Style CSS dla formularzy
- Konfiguracja Tailwind CSS
- Niestandardowe komponenty Material Design

### Struktura Projektu

```
src/
├── database/
│   └── models.py              # Modele bazodanowe
├── web/
│   ├── forms.py              # Formularze Flask-WTF
│   ├── views.py              # Widoki Flask
│   ├── error_handlers.py     # Obsługa błędów
│   ├── static/
│   │   ├── css/style.css     # Style CSS
│   │   └── js/ReceiptVerificationForm.js
│   └── templates/
│       ├── base.html         # Szablon bazowy
│       ├── index.html        # Strona główna
│       ├── receipt_list.html # Lista paragonów
│       ├── upload.html       # Upload paragonów
│       ├── verify.html       # Formularz weryfikacji
│       └── errors/
│           ├── 404.html      # Błąd 404
│           └── 500.html      # Błąd 500
```

### Wymagane Zależności
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-WTF==1.2.1
google-cloud-vision==3.5.0
Pillow==10.1.0
python-dotenv==1.0.0
Werkzeug==3.0.1
pytest==8.0.0
```

## Elementy Do Implementacji

### Priorytet 1: Uporządkowanie Projektu
1. Usunięcie zduplikowanych plików i szablonów
2. Reorganizacja struktury views.py
3. Uzupełnienie brakujących testów
4. Dokończenie implementacji stylów CSS

### Priorytet 2: Podstawowe Funkcjonalności
1. Implementacja pełnego systemu uploadu plików
2. Dokończenie endpointów REST API
3. Implementacja pełnej obsługi błędów
4. System walidacji danych

### Priorytet 3: Automatyzacja
1. Integracja z Google Cloud Vision API
2. System OCR dla paragonów
3. Automatyczne przetwarzanie danych
4. System powiadomień

### Priorytet 4: System Użytkowników
1. Model User i integracja z Flask-Login
2. Formularze logowania i rejestracji
3. System uprawnień
4. Panel administracyjny

## Uwagi Techniczne

### Konfiguracja Środowiska
- Wymagany Python 3.12
- Projekt skonfigurowany jako pakiet Python (setup.py)
- Konfiguracja w `src/config.py`
- Środowisko deweloperskie z debuggerem

### Struktura Bazy Danych
- SQLite jako baza danych
- Ścieżka do bazy: `data/zakupy.db`
- Automatyczne migracje przez Flask-Migrate

### Frontend
- Bootstrap 5 jako podstawowy framework
- Material Design dla komponentów
- Tailwind CSS do stylizacji
- Font Awesome dla ikon
- JavaScript do dynamicznej obsługi formularzy

## Znane Problemy

1. Niekompletna implementacja uploadu plików
2. Brak pełnej obsługi błędów w niektórych endpointach
3. Niewystarczające pokrycie testami
4. Konieczność dokończenia integracji Tailwind CSS

## Następne Kroki

1. Uporządkowanie kodu i usunięcie duplikatów
2. Dokończenie implementacji podstawowych funkcjonalności
3. Dodanie testów jednostkowych
4. Integracja z OCR
5. Implementacja systemu użytkowników

## Rozwiązywanie problemów

### Problem z certyfikatem SSL podczas instalacji pakietów

Jeśli podczas instalacji pakietów poprzez `pip install -r requirements.txt` pojawia się błąd SSL, wykonaj następujące kroki:

1. Najpierw spróbuj zaktualizować narzędzia pip i setuptools:
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pip setuptools --upgrade
```

2. Następnie zainstaluj wymagane pakiety używając parametru trusted-host:
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### Dlaczego występuje ten problem?

Problem występuje, gdy system nie może zweryfikować certyfikatu SSL podczas połączenia z PyPI (Python Package Index). Może to być spowodowane przez:
- Przestarzałe certyfikaty w systemie
- Problemy z zaporą sieciową
- Proxy blokujące połączenia HTTPS
- Nieaktualne narzędzia pip lub setuptools

#### Rozwiązanie długoterminowe

Aby trwale rozwiązać problem z certyfikatami SSL:

1. Zaktualizuj system:
```bash
sudo apt update
sudo apt upgrade
```

2. Zainstaluj aktualne certyfikaty:
```bash
sudo apt install ca-certificates
```

3. Zaktualizuj certyfikaty:
```bash
sudo update-ca-certificates
```