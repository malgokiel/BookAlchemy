from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    """
    Inherits from a SQLAlchemy db model,
    allows the user to create an Author object which can then be commited to db table.
    id: primary key
    name: required, cannot be empty string
    birth_date: required, cannot be later than current day or date of death
    date_of_death: not required, cannot be in the future or before birth date
    """
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.String)
    date_of_death = db.Column(db.String)

    def __repr__(self):
        return f'Author: {self.name}, born {self.birth_date}, died {self.date_of_death}'


class Book(db.Model):
    """
    Inherits from a SQLAlchemy db model,
    allows the user to create a Book object which can then be commited to db table.
    id: primary key
    isbn: required, only numbers allowed, length either 9 or 13 chars
    title: required, cannot be empty string
    publication_year: required, cannot be later than current year
    author_id: required, must be present in authors table
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String)
    title = db.Column(db.String)
    publication_year = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return f'Book: {self.title}, ISBN {self.isbn}'
