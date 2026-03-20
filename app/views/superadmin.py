from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, Post, Board, Comment

superadmin_bp = Blueprint('superadmin', __name__, url_prefix='/superadmin')


def superadmin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        if not current_user.is_superadmin():
            abort(403)
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@superadmin_bp.route('/')
@login_required
@superadmin_required
def index():
    stats = {
        'total_users': User.query.count(),
        'total_posts': Post.query.filter_by(is_deleted=False).count(),
        'total_comments': Comment.query.filter_by(is_deleted=False).count(),
        'total_boards': Board.query.count(),
        'total_admins': User.query.filter(User.role.in_(['admin', 'superadmin'])).count(),
        'total_superadmins': User.query.filter_by(role='superadmin').count()
    }
    all_users = User.query.order_by(User.created_at.desc()).all()

    return render_template('superadmin/index.html', stats=stats, all_users=all_users)


@superadmin_bp.route('/users')
@login_required
@superadmin_required
def users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=30)
    return render_template('superadmin/users.html', pagination=pagination)


@superadmin_bp.route('/set-admin/<int:user_id>', methods=['POST'])
@login_required
@superadmin_required
def set_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_superadmin():
        flash('无法修改超级管理员权限', 'danger')
        return redirect(url_for('superadmin.users'))

    user.role = 'admin'
    db.session.commit()
    flash(f'{user.username} 已设为管理员', 'success')
    return redirect(url_for('superadmin.users'))


@superadmin_bp.route('/remove-admin/<int:user_id>', methods=['POST'])
@login_required
@superadmin_required
def remove_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_superadmin():
        flash('无法修改超级管理员权限', 'danger')
        return redirect(url_for('superadmin.users'))

    user.role = 'user'
    db.session.commit()
    flash(f'{user.username} 已移除管理员权限', 'success')
    return redirect(url_for('superadmin.users'))


@superadmin_bp.route('/toggle-user-status/<int:user_id>', methods=['POST'])
@login_required
@superadmin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_superadmin():
        flash('无法修改超级管理员状态', 'danger')
        return redirect(url_for('superadmin.users'))

    user.is_active = not user.is_active
    db.session.commit()
    flash(f'{user.username} 已{"启用" if user.is_active else "禁用"}', 'success')
    return redirect(url_for('superadmin.users'))


@superadmin_bp.route('/set-superadmin/<int:user_id>', methods=['POST'])
@login_required
@superadmin_required
def set_superadmin(user_id):
    user = User.query.get_or_404(user_id)
    user.role = 'superadmin'
    db.session.commit()
    flash(f'{user.username} 已设为超级管理员', 'success')
    return redirect(url_for('superadmin.users'))


@superadmin_bp.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
@superadmin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_superadmin():
        flash('无法删除超级管理员', 'danger')
        return redirect(url_for('superadmin.users'))

    Post.query.filter_by(user_id=user.id).update({'is_deleted': True})
    Comment.query.filter_by(user_id=user.id).update({'is_deleted': True})
    db.session.delete(user)
    db.session.commit()
    flash(f'{user.username} 已删除', 'success')
    return redirect(url_for('superadmin.users'))


@superadmin_bp.route('/boards')
@login_required
@superadmin_required
def boards():
    all_boards = Board.query.order_by(Board.created_at.desc()).all()
    return render_template('superadmin/boards.html', boards=all_boards)
