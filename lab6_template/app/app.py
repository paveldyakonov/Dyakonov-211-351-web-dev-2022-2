import math
from flask import Flask, flash, redirect, render_template, abort, request, send_from_directory, url_for
from sqlalchemy import MetaData, desc
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_required, current_user
import bleach
import markdown

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

PERMITTED_PARAMS = ["name", "short_desc", "year", "pub_house", "author", "volume"]
from auth import bp as auth_bp, init_login_manager
from comments import bp as comment_bp
# from courses import bp as courses_bp

app.register_blueprint(auth_bp)
app.register_blueprint(comment_bp)
# app.register_blueprint(courses_bp)

init_login_manager(app)

from models import Image, Book, Genre, Comment
from auth import check_rights

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = app.config['PER_PAGE']
    info_about_books = []
    books_counter = Book.query.count()
    books = db.session.execute(db.select(Book).order_by(desc(Book.year)).limit(per_page).offset(per_page * (page - 1))).scalars()
    #books_counter = db.session.execute(db.select(Book)).count()
    for book in books:
        books_counter += 1
        info = {
            'book': book,
            'genres': book.genres,
        }
        info_about_books.append(info)
    page_count = math.ceil(books_counter / per_page)
    print("rrrrr", books_counter)
    categories = []
    # categories = db.session.execute(db.select(Category)).scalars()
    return render_template(
        'index.html',
        categories=categories,
        books=info_about_books,
        page=page,
        page_count=page_count
    )

@app.route('/images/<image_id>')
def image(image_id):
    img = db.get_or_404(Image, image_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               img.storage_filename)

def params(names_list):
    result = {}
    for name in names_list:
        result[name] = request.form.get(name) or None
    return result

@app.route('/books/new')
@login_required
@check_rights("create")
def new_book():
    genres = db.session.execute(db.select(Genre)).scalars()
    return render_template('books/new.html', genres=genres, book={}, new_genres=[])

@app.route('/books/create', methods=['POST'])
@login_required
@check_rights("create")
def create_book():
    if not current_user.can("create"):
        flash("Недостаточно прав для доступа к странице", "warning")
        return redirect(url_for("index"))
    cur_params = params(PERMITTED_PARAMS)
    for param in cur_params:
        param = bleach.clean(param)
    new_genres = request.form.getlist('genre_id')
    genres = db.session.execute(db.select(Genre)).scalars()
    try:
        book = Book(**cur_params)
        for genre in new_genres:
            new_genre = db.session.execute(db.select(Genre).filter_by(id=genre)).scalar()
            book.genres.append(new_genre)
        db.session.add(book)
        db.session.commit()
        flash(f"Книга '{book.name}' успешно добавлена", "success")
    except:
        db.session.rollback()
        flash("При сохранении возникла ошибка", "danger")
        return render_template("books/new.html", genres = genres, book=cur_params, new_genres=new_genres)
    return redirect(url_for('show', book_id=book.id))

@app.route('/delete_post/<int:book_id>', methods=['POST'])
@login_required
@check_rights('delete')
def delete_post(book_id):
    try:
        book = db.session.query(Book).filter(Book.id == book_id).scalar()
        book.genres = []
        db.session.query(Comment).filter(Comment.book_id == book_id).delete()
        db.session.query(Book).filter(Book.id == book_id).delete()
        db.session.commit()
        flash('Запись успешно удалена', 'success')
    except:
        db.session.rollback()
        flash('Ошибка при удалении', 'danger')
    return redirect(url_for('index'))


@app.route('/books/<int:book_id>/edit', methods=['GET'])
@login_required
@check_rights("edit")
def edit_book(book_id):
    book = db.session.query(Book).filter(Book.id == book_id).scalar()
    genres = db.session.execute(db.select(Genre)).scalars()
    edited_genres = [ str(genre.id) for genre in book.genres]
    return render_template("books/edit.html", genres = genres, book=book, new_genres=edited_genres)

@app.route('/books/<int:book_id>/update', methods=['POST'])
@login_required
@check_rights("edit")
def update_book(book_id):
    if not current_user.can("edit"):
        flash("Недостаточно прав для доступа к странице", "warning")
        return redirect(url_for("index"))
    print("sverbetrb", book_id)
    cur_params = params(PERMITTED_PARAMS)
    for param in cur_params:
        param = bleach.clean(param)
    new_genres = request.form.getlist('genre_id')
    genres = db.session.execute(db.select(Genre)).scalars()
    book = db.session.query(Book).filter(Book.id == book_id).scalar()
    try:
        genres_list = []
        for genre in new_genres:
            if int(genre) != 0:
                new_genre = db.session.execute(db.select(Genre).filter_by(id=genre)).scalar()
                genres_list.append(new_genre)
        book.genres = genres_list
        book.name = cur_params['name']
        book.short_desc = cur_params['short_desc']
        book.year = cur_params['year']
        book.pub_house = cur_params['pub_house']
        book.author = cur_params['author']
        book.volume = cur_params['volume']
        db.session.commit()
        flash(f"Книга '{book.name}' успешно обновлена", "success")
    except:
        db.session.rollback()
        flash("При сохранении возникла ошибка", "danger")
        return render_template("books/edit.html", genres = genres, book=book, new_genres=new_genres)
    return redirect(url_for('show', book_id=book.id))

@app.route('/books/<int:book_id>')
def show(book_id):
    try:
        book = db.session.query(Book).filter(Book.id == book_id).scalar()
        book.short_desc = markdown.markdown(book.short_desc)
        comment = None
        if current_user.is_authenticated:
            comment = db.session.query(Comment).filter(Comment.book_id == book_id, Comment.user_id == current_user.id).scalar()
        genres = book.genres
        return render_template('books/show.html', book=book, genres=genres, comment=comment)
    except:
        flash('Ошибка при загрузке данных', 'danger')
        return redirect(url_for('index'))