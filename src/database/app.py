from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import main
from database.manager import DatabaseManager
from database.models import db, Base

app = Flask(__name__)
app.config.from_object(config_class)
app.config['SQLALCHEMY_DATABASE_URI'] = config_class
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(main)

if __name__ == "__main__":
    app.run()