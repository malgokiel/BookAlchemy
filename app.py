from pyexpat.errors import messages

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert, text, create_engine
from data_models import db, Author, Book
import helper

QUERY_ALL_AUTHORS = "SELECT authors.id, authors.name FROM authors"
QUERY_ALL_BOOKS = "SELECT books.*, authors.name FROM books JOIN authors ON books.author_id = authors.id"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/malgorzata/PycharmProjects/BookAlchemy/data/library.sqlite'
db.init_app(app)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        action = request.form.get('add')
        if action == 'Add Author':
            new_author = Author(name=request.form.get('name'),
                                birth_date=request.form.get('birthdate'),
                                date_of_death=request.form.get('date_of_death'))
            db.session.add(new_author)
            db.session.commit()
        return render_template('add_author.html', message="Author added.")

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        action = request.form.get('add')
        if action == 'Add Book':
            new_book = Book(isbn=request.form.get('ISBN'),
                            title=request.form.get('title'),
                            publication_year=request.form.get('publication_year'),
                            author_id=request.form.get('author'))
            db.session.add(new_book)
            db.session.commit()
            authors = helper.get_all_results(QUERY_ALL_AUTHORS)
            return render_template('add_book.html', message="Book added.", authors=authors)
    else:
        authors = helper.get_all_results(QUERY_ALL_AUTHORS)
    return render_template('add_book.html', authors=authors)


@app.route('/home', methods=['GET'])
def home():
    books = helper.get_all_results(QUERY_ALL_BOOKS)
    return render_template('home.html', books=books)

with app.app_context():
  db.create_all()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

