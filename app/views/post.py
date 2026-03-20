from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Post, Board, Comment
from app.forms import PostForm, CommentForm

post_bp = Blueprint('post', __name__, url_prefix='/post')


@post_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    form.board_id.choices = [(b.id, b.name) for b in Board.query.filter_by(is_active=True).all()]

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    board_id=form.board_id.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('帖子发布成功！', 'success')
        return redirect(url_for('main.index'))

    return render_template('post/create.html', form=form)


@post_bp.route('/detail/<int:post_id>', methods=['GET', 'POST'])
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    post.view_count += 1
    db.session.commit()

    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('请先登录后再评论', 'warning')
            return redirect(url_for('auth.login'))
        comment = Comment(content=form.content.data, post_id=post.id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('评论发表成功！', 'success')
        return redirect(url_for('post.detail', post_id=post.id))

    comments = Comment.query.filter_by(post_id=post.id, is_deleted=False, parent_id=None).order_by(Comment.created_at.desc()).all()

    return render_template('post/detail.html', post=post, form=form, comments=comments)


@post_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id and not current_user.is_admin():
        abort(403)

    form = PostForm()
    form.board_id.choices = [(b.id, b.name) for b in Board.query.filter_by(is_active=True).all()]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.board_id = form.board_id.data
        db.session.commit()
        flash('帖子已更新', 'success')
        return redirect(url_for('post.detail', post_id=post.id))

    form.title.data = post.title
    form.content.data = post.content
    form.board_id.data = post.board_id

    return render_template('post/edit.html', form=form, post=post)


@post_bp.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id and not current_user.is_admin():
        abort(403)

    post.is_deleted = True
    db.session.commit()
    flash('帖子已删除', 'success')
    return redirect(url_for('main.index'))
