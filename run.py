# filepath: /C:/Users/marci/Documents/GitHub/receipts-manager/run.py
from src.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)