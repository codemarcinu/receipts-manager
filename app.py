from flask import Flask
import os

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Basic configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///receipts.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=os.path.join(app.root_path, 'uploads')
    )

    if test_config is not None:
        app.config.update(test_config)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize database
    from src.database.models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints
    from src.views import bp as receipts_bp, register_error_handlers
    app.register_blueprint(receipts_bp)
    register_error_handlers(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
