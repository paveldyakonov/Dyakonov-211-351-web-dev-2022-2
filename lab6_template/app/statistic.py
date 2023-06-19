import math
import io
from datetime import date, datetime, timedelta
from flask import Blueprint, render_template, request, send_file
from auth import check_rights
from flask_login import login_required
from models import Book, Visit
from app import db
from flask import Blueprint
from sqlalchemy import desc, func

PER_PAGE = 10

bp = Blueprint('statistic', __name__, url_prefix='/statistic')

@bp.route('/')
@login_required
@check_rights('statistic')
def index():
    return render_template('statistic/index.html')

@bp.route('/users')
@login_required
@check_rights("statistic")
def users():
    page = request.args.get('page', 1, type=int)
    per_page = PER_PAGE
    visits_counter = Visit.query.count()
    page_count = math.ceil(visits_counter / per_page)
    download_status = False
    if request.args.get('download_csv'):
        download_status = True

    if download_status:
        visits = db.session.execute(db.select(Visit).order_by(desc(Visit.created_at))).scalars()
        f = io.BytesIO()
        f.write("N,User,Book,DateTime\n".encode("utf-8"))
        for i, row in enumerate(visits):
            login = row.get_user_name()
            if login:
                login = login.login
            else:
                login = "Non-authenticated user"
            f.write(f'{i+1},{login},{row.get_book_name()},{row.created_at}\n'.encode("utf-8"))
        f.seek(0)
        today = date.today()
        return send_file(f, as_attachment=True, download_name=f"stat_users{today}.csv", mimetype="text/csv")
    
    visits = db.session.execute(db.select(Visit).order_by(desc(Visit.created_at)).limit(per_page).offset(per_page * (page - 1))).scalars()
        
    return render_template('statistic/users.html', stats=visits, page=page, page_count=page_count)

def get_books(all = False, page = 1):
    visits = []
    per_page = PER_PAGE
    if request.method == "POST":
        date_from = request.form.get('date_from')
        date_before = request.form.get('date_before')
        if date_from:
            visits = db.session.execute(db.select(Visit.book_id).filter(Visit.user_id != None, Visit.created_at >= datetime.strptime(date_from, '%Y-%m-%d')).order_by(desc(func.count(Visit.book_id))).group_by(Visit.book_id).limit(per_page).offset(per_page * (page - 1))).scalars()
        elif date_before:
            visits = db.session.execute(db.select(Visit.book_id).filter(Visit.user_id != None, Visit.created_at <= datetime.strptime(date_before, '%Y-%m-%d') + timedelta(days=1)).order_by(desc(func.count(Visit.book_id))).group_by(Visit.book_id).limit(per_page).offset(per_page * (page - 1))).scalars()
        else:
            visits = db.session.execute(db.select(Visit.book_id).filter(Visit.user_id != None).order_by(desc(func.count(Visit.book_id))).group_by(Visit.book_id).limit(per_page).offset(per_page * (page - 1))).scalars()
    elif all:
        visits = db.session.execute(db.select(Visit.book_id).filter(Visit.user_id != None).order_by(desc(func.count(Visit.book_id))).group_by(Visit.book_id)).scalars()
    else:
        visits = db.session.execute(db.select(Visit.book_id).filter(Visit.user_id != None).order_by(desc(func.count(Visit.book_id))).group_by(Visit.book_id).limit(per_page).offset(per_page * (page - 1))).scalars()

    books = []
    for visit in visits:
        book = db.session.query(Book).filter(Book.id == int(visit)).scalar()
        books.append(book)
        
    return books

@bp.route('/books', methods=['GET', 'POST'])
@login_required
@check_rights("statistic")
def books():
    date_from = ""
    date_before = ""
    visits_counter = db.session.query(Visit.book_id).filter(Visit.user_id != None).group_by(Visit.book_id).count()
    if request.method == "POST":
        date_from = request.form.get('date_from')
        date_before = request.form.get('date_before')
        if date_from:
            visits_counter = db.session.query(Visit.book_id).filter(Visit.user_id != None, Visit.created_at >= datetime.strptime(date_from, '%Y-%m-%d')).group_by(Visit.book_id).count()
        elif date_before:
            visits_counter = db.session.query(Visit.book_id).filter(Visit.user_id != None, Visit.created_at <= datetime.strptime(date_before, '%Y-%m-%d') + timedelta(days=1)).group_by(Visit.book_id).count()
    page = request.args.get('page', 1, type=int)
    per_page = PER_PAGE
    page_count = math.ceil(visits_counter / per_page)
    download_status = False
    if request.args.get('download_csv'):
        download_status = True

    if download_status:
        books = get_books(True)
        f = io.BytesIO()
        f.write("N,Book,Count\n".encode("utf-8"))
        for i, row in enumerate(books):
            f.write(f'{i+1},{row.name},{row.get_visits_count()}\n'.encode("utf-8"))
        f.seek(0)
        today = date.today()
        return send_file(f, as_attachment=True, download_name=f"stat_books{today}.csv", mimetype="text/csv")
    books = get_books(False, page)
        
    return render_template('statistic/books.html', stats=books, page=page, page_count=page_count, date_from=date_from, date_before=date_before)