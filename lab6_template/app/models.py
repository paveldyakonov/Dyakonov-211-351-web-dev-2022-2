import os
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import current_app, url_for
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
    genres = db.relationship('Genre', secondary=book_genre, backref=db.backref('books'), cascade="all,delete")

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
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

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

    # user = db.relationship('User')
    # book = db.relationship('Book')

    def __repr__(self):
        return '<Comment %r>' % self.text



# class Category(db.Model):
#     __tablename__ = 'categories'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

#     def __repr__(self):
#         return '<Category %r>' % self.name


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
        return True
        #return self.role_id == current_app.config["ADMIN_ROLE_ID"]
    
    def is_moder(self):
        return True
        #return self.role_id == current_app.config["MODER_ROLE_ID"]
    
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


# class Course(db.Model):
#     __tablename__ = 'courses'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     short_desc = db.Column(db.Text, nullable=False)
#     full_desc = db.Column(db.Text, nullable=False)
#     rating_sum = db.Column(db.Integer, nullable=False, default=0)
#     rating_num = db.Column(db.Integer, nullable=False, default=0)
#     category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     background_image_id = db.Column(db.String(100), db.ForeignKey('images.id'))
#     created_at = db.Column(db.DateTime,
#                            nullable=False,
#                            server_default=sa.sql.func.now())

#     author = db.relationship('User')
#     category = db.relationship('Category', lazy=False)
#     bg_image = db.relationship('Image')

#     def __repr__(self):
#         return '<Course %r>' % self.name

#     @property
#     def rating(self):
#         if self.rating_num > 0:
#             return self.rating_sum / self.rating_num
#         return 0

# class Image(db.Model):
#     __tablename__ = 'images'

#     id = db.Column(db.String(100), primary_key=True)
#     file_name = db.Column(db.String(100), nullable=False)
#     mime_type = db.Column(db.String(100), nullable=False)
#     md5_hash = db.Column(db.String(100), nullable=False, unique=True)
#     created_at = db.Column(db.DateTime,
#                            nullable=False,
#                            server_default=sa.sql.func.now())
#     object_id = db.Column(db.Integer)
#     object_type = db.Column(db.String(100))

#     def __repr__(self):
#         return '<Image %r>' % self.file_name

#     @property
#     def storage_filename(self):
#         _, ext = os.path.splitext(self.file_name)
#         return self.id + ext

#     @property
#     def url(self):
#         return url_for('image', image_id=self.id)