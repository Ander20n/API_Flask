from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    nationality = db.Column(db.String(255))

    books = db.relationship('Book', backref='author', cascade='delete')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    number_pages = db.Column(db.Integer)
    authors_id = db.Column(db.Integer, db.ForeignKey('author.id', ondelete='CASCADE'), nullable=False)