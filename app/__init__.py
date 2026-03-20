from flask import Flask
from app.config import Config
from app.extensions import db, login_manager, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.views.main import main_bp
    from app.views.auth import auth_bp
    from app.views.post import post_bp
    from app.views.admin import admin_bp
    from app.views.superadmin import superadmin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(superadmin_bp)

    with app.app_context():
        db.create_all()

    return app
