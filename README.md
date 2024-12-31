# System Zarządzania Paragonami - Dokumentacja Projektu

## Stan Projektu na dzień 28.01.2024

### Zrealizowane Komponenty

#### 1. Frontend Framework
- Zintegrowany Tailwind CSS
- Własne komponenty Material Design
- Responsywny interfejs
- System komponentów z prefixem 'md-'

#### 2. Struktura Bazy Danych
- Modele: Receipt, Product, Category w `src.database.models`
- Wykorzystanie SQLAlchemy z podstawowymi relacjami
- System migracji z Flask-Migrate
- Automatyczna inicjalizacja bazy przez skrypt

#### 3. Interfejs Webowy
- Material Design komponenty:
  - Cards (md-card)
  - Buttons (md-button)
  - Forms (md-input)
  - Alerts (md-alert)
  - Progress indicators (md-spinner, md-progress-bar)
  - Tooltips (md-tooltip)
- Animacje i przejścia
- System powiadomień
- Dostosowania pod dark mode
- Wsparcie dla prefers-reduced-motion

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
│   │   ├── css/
│   │   │   ├── style.css     # Główne style Tailwind + Material
│   │   │   └── main.css      # Generowany plik Tailwind
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
tailwindcss==3.4.0
postcss==8.4.0
autoprefixer==10.4.0
```

## Elementy Do Implementacji

### Priorytet 1: Optymalizacja Frontend
1. Dokończenie dark mode
2. Optymalizacja bundle size CSS
3. Implementacja dodatkowych komponentów Material Design
4. Poprawa dostępności (ARIA labels)

### Priorytet 2: Uporządkowanie Projektu
1. Usunięcie zduplikowanych plików i szablonów
2. Reorganizacja struktury views.py
3. Uzupełnienie brakujących testów
4. Dokończenie implementacji stylów CSS

### Priorytet 3: Podstawowe Funkcjonalności
1. Implementacja pełnego systemu uploadu plików
2. Dokończenie endpointów REST API
3. Implementacja pełnej obsługi błędów
4. System walidacji danych

### Priorytet 4: Automatyzacja
1. Integracja z Google Cloud Vision API
2. System OCR dla paragonów
3. Automatyczne przetwarzanie danych
4. System powiadomień

### Priorytet 5: System Użytkowników
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

### Problem z kompilacją Tailwind CSS

Jeśli występują problemy z kompilacją Tailwind CSS:

1. Upewnij się, że masz zainstalowane wszystkie zależności:
```bash
npm install -D tailwindcss postcss autoprefixer
```

2. Zainicjuj konfigurację Tailwind:
```bash
npx tailwindcss init
```

3. Uruchom watch mode podczas rozwoju:
```bash
npx tailwindcss -i ./src/web/static/css/main.css -o ./src/web/static/css/style.css --watch
```