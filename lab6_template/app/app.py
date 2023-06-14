from flask import Flask, flash, redirect, render_template, abort, send_from_directory, url_for
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_required, current_user

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from auth import bp as auth_bp, init_login_manager
# from courses import bp as courses_bp

app.register_blueprint(auth_bp)
# app.register_blueprint(courses_bp)

init_login_manager(app)

from models import Image, Book
from auth import check_rights

@app.route('/')
def index():
    info_about_books = []
    books = db.session.execute(db.select(Book)).scalars()
    for book in books:
        info = {
            'book': book,
            'genres': book.genres,
        }
        info_about_books.append(info)
    categories = []
    # categories = db.session.execute(db.select(Category)).scalars()
    return render_template(
        'index.html',
        categories=categories,
        books=info_about_books,
    )

@app.route('/images/<image_id>')
def image(image_id):
    img = db.get_or_404(Image, image_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               img.storage_filename)

@app.route('/delete_post/<int:book_id>', methods=['POST'])
@login_required
@check_rights('delete')
def delete_post(book_id):
    try:
        book = db.session.query(Book).filter(Book.id == book_id).scalar()
        book.genres = []
        db.session.query(Book).filter(Book.id == book_id).delete()
        db.session.commit()
        flash('Запись успешно удалена', 'success')
    except:
        db.session.rollback()
        flash('Ошибка при удалении', 'danger')
    return redirect(url_for('index'))