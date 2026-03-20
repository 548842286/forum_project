from flask import Blueprint, render_template, request
from flask_login import current_user
from app.models import Board, Post

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    board_id = request.args.get('board_id', type=int)

    query = Post.query.filter_by(is_deleted=False).order_by(Post.is_pinned.desc(), Post.created_at.desc())

    if board_id:
        query = query.filter_by(board_id=board_id)

    pagination = query.paginate(page=page, per_page=20, error_out=False)
    posts = pagination.items

    boards = Board.query.filter_by(is_active=True).all()

    return render_template('main/index.html',
                           posts=posts,
                           boards=boards,
                           pagination=pagination,
                           board_id=board_id)
