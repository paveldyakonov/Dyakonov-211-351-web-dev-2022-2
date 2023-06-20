from datetime import datetime, timedelta
import os
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import current_app, request, url_for
from app import db
from users_policy import UsersPolicy

book_genre = db.Table('book_genre',
                       db.Column('book_id',db.Integer,db.ForeignKey('books.id'),primary_key=True),
                       db.Column('genre_id',db.Integer,db.ForeignKey('genres.id'),primary_key=True))

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_desc = db.Column(db.Text, nullable=False)
    year = db.Column(db.String(4), nullable=False)
    pub_house = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    rating_sum = db.Column(db.Integer, nullable=False, default=0)
    rating_num = db.Column(db.Integer, nullable=False, default=0)
    image_id = db.Column(db.String(100), db.ForeignKey('images.id'))
    genres = db.relationship('Genre', secondary=book_genre, backref=db.backref('books'), cascade="all,delete")
    image = db.relationship('Image', cascade="all,delete")

    def get_visits_count(self):
        if request.method == "POST":
            date_from = request.form.get('date_from')
            date_before = request.form.get('date_before')
            if date_from:
                return db.session.query(Visit).filter(Visit.book_id == self.id, Visit.user_id != None, Visit.created_at >= datetime.strptime(date_from, '%Y-%m-%d')).count()
            elif date_before:
                return db.session.query(Visit).filter(Visit.book_id == self.id, Visit.user_id != None, Visit.created_at <= datetime.strptime(date_before, '%Y-%m-%d') + timedelta(days=1)).count()                
        return db.session.query(Visit).filter(Visit.book_id == self.id, Visit.user_id != None).count()

    def __repr__(self):
        return '<Book %r>' % self.name
    
    @property
    def rating(self):
        if self.rating_num > 0:
            return self.rating_sum / self.rating_num
        return 0

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Genre %r>' % self.name

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.String(100), primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    md5_hash = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return '<Image %r>' % self.file_name

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

    @property
    def url(self):
        return url_for('image', image_id=self.id)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', cascade="all,delete")
    book = db.relationship('Book', cascade="all,delete")

    def get_user(self):
        return db.session.execute(db.select(User).filter_by(id=self.user_id)).scalar().login

    def __repr__(self):
        return '<Comment %r>' % self.text

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role_id == current_app.config["ADMIN_ROLE_ID"]
    
    def is_moder(self):
        return self.role_id == current_app.config["MODER_ROLE_ID"]
    
    def can(self, action, record=None):
        users_policy = UsersPolicy(record)
        method = getattr(users_policy, action, None)
        if method:
            return method()
        return False

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])

    def __repr__(self):
        return '<User %r>' % self.login

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Role %r>' % self.name


class Visit(db.Model):
    __tablename__ = 'visits'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())

    def get_book_name(self):
        return db.session.execute(db.select(Book).filter_by(id=self.book_id)).scalar().name
    
    def get_user_name(self):
        return db.session.execute(db.select(User).filter_by(id=self.user_id)).scalar()
    
    def __repr__(self):
        return '<Visit %r>' % self.book_id