from app.views.main import main_bp
from app.views.auth import auth_bp
from app.views.post import post_bp
from app.views.admin import admin_bp
from app.views.superadmin import superadmin_bp

__all__ = ['main_bp', 'auth_bp', 'post_bp', 'admin_bp', 'superadmin_bp']
