from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Comment, Book
from app import db
from flask import Blueprint
import bleach

bp = Blueprint('comments', __name__, url_prefix='/comments')

@bp.route('/<int:book_id>', methods=['GET', 'POST'])
@login_required
def comment_post(book_id):
    comment = db.session.query(Comment).filter(Comment.book_id == book_id, Comment.user_id == current_user.id).scalar()
    book = db.session.query(Book).filter(Book.id == book_id).scalar()
    if comment:
        flash("Можно добавить только одну рецензию", "warning")
        return redirect(url_for('show', book_id=book_id))
    if request.method == 'POST':
        mark = request.form.get('mark')
        params = {
            "mark": mark,
            "text": request.form.get('short_desc'),
            "user_id": current_user.id,
            "book_id": book_id
        }
        for param in params:
            param = bleach.clean(param)
        try:
            comment = Comment(**params)
            db.session.add(comment)
            book.rating_sum = book.rating_sum + int(mark)
            book.rating_num = book.rating_num + 1
            db.session.commit()
            flash("Рецензия успешно добавлена", "success")
            return redirect(url_for('show', book_id=book_id))
        except:
            db.session.rollback()
            flash('Ошибка при добавлении рецензии', 'danger')
            return redirect(url_for('comments.comment_post', book_id=book_id))
    return render_template('comment_post.html', book_id=book_id)
