from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, Post, Board, Comment
from app.forms import BoardForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def index():
    stats = {
        'total_users': User.query.count(),
        'total_posts': Post.query.filter_by(is_deleted=False).count(),
        'total_comments': Comment.query.filter_by(is_deleted=False).count(),
        'total_boards': Board.query.count()
    }
    recent_posts = Post.query.filter_by(is_deleted=False).order_by(Post.created_at.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()

    return render_template('admin/index.html', stats=stats, recent_posts=recent_posts, recent_users=recent_users)


@admin_bp.route('/posts')
@login_required
@admin_required
def posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(is_deleted=False).order_by(Post.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/posts.html', pagination=pagination)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/users.html', pagination=pagination)


@admin_bp.route('/toggle-pin/<int:post_id>', methods=['POST'])
@login_required
@admin_required
def toggle_pin(post_id):
    post = Post.query.get_or_404(post_id)
    post.is_pinned = not post.is_pinned
    db.session.commit()
    flash(f'帖子{"置顶" if post.is_pinned else "取消置顶"}成功', 'success')
    return redirect(request.referrer or url_for('admin.posts'))


@admin_bp.route('/boards', methods=['GET', 'POST'])
@login_required
@admin_required
def boards():
    form = BoardForm()
    if form.validate_on_submit():
        board = Board(name=form.name.data, description=form.description.data)
        db.session.add(board)
        db.session.commit()
        flash('板块创建成功', 'success')
        return redirect(url_for('admin.boards'))

    all_boards = Board.query.order_by(Board.created_at.desc()).all()
    return render_template('admin/boards.html', form=form, boards=all_boards)


@admin_bp.route('/delete-board/<int:board_id>', methods=['POST'])
@login_required
@admin_required
def delete_board(board_id):
    board = Board.query.get_or_404(board_id)
    board.is_active = False
    db.session.commit()
    flash('板块已删除', 'success')
    return redirect(url_for('admin.boards'))
