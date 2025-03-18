from pyexpat.errors import messages

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert, text, create_engine
from data_models import db, Author, Book
import helper
import random

QUERY_ALL_AUTHORS = "SELECT authors.id, authors.name FROM authors"
QUERY_ALL_BOOKS = "SELECT books.*, authors.name FROM books JOIN authors ON books.author_id = authors.id"
QUERY_SORTED_AUTHORS = "SELECT books.*, authors.name FROM books JOIN authors ON books.author_id=authors.id ORDER BY authors.name"
QUERY_SORTED_TITLES = "SELECT books.*, authors.name FROM books JOIN authors ON books.author_id=authors.id ORDER BY books.title"
QUERY_SORTED_YEARS = "SELECT books.*, authors.name FROM books JOIN authors ON books.author_id=authors.id ORDER BY books.publication_year DESC"
QUERY_BY_SEARCH_TERM = "SELECT books.*, authors.name FROM books JOIN authors ON books.author_id = authors.id WHERE books.title LIKE CONCAT('%', :search_for, '%') OR authors.name LIKE CONCAT('%', :search_for, '%')"
QUERY_ALL_AUTHORS_INFO = "SELECT authors.*, COUNT(books.author_id) AS book_count FROM authors LEFT JOIN books ON authors.id = books.author_id GROUP BY authors.name"
QUERY_NEWEST_BOOKS = "SELECT books.*, authors.name FROM books JOIN authors ON books.author_id = authors.id ORDER BY books.id DESC LIMIT 3"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/malgorzata/PycharmProjects/BookAlchemy/data/library.sqlite'
db.init_app(app)


engine = create_engine('sqlite:///data/library.sqlite')

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

@app.route('/', methods=['GET'])
def index():
    recent_books = helper.get_all_results(QUERY_NEWEST_BOOKS)
    books = helper.get_all_results(QUERY_ALL_BOOKS)
    recommended_book = random.choice(books)
    return render_template('index.html', recommended_book=recommended_book, books=recent_books)

@app.route('/books', methods=['GET', 'POST'], endpoint='books')
def all_books():
    books = helper.get_all_results(QUERY_ALL_BOOKS)
    if request.method == 'POST':
        action = request.form.get('sort')
        delete = request.form.get('delete')
        search = request.form.get('search')
        if action:
            if action == 'author':
                books = helper.get_all_results(QUERY_SORTED_AUTHORS)
            elif action == 'title':
                books = helper.get_all_results(QUERY_SORTED_TITLES)
            elif action == 'year':
                books = helper.get_all_results(QUERY_SORTED_YEARS)
        elif delete:
            book_id = delete
            book_to_delete = db.session.get(Book, book_id)
            db.session.delete(book_to_delete)
            db.session.commit()
            books = helper.get_all_results(QUERY_ALL_BOOKS)
        elif search:
            books = helper.get_all_results(QUERY_BY_SEARCH_TERM,{'search_for':search})

        return render_template('books.html', books=books)

    return render_template('books.html', books=books)

@app.route('/authors', methods=['GET', 'POST'])
def all_authors():
    authors = helper.get_all_results(QUERY_ALL_AUTHORS_INFO)
    if request.method == 'POST':
        delete = request.form.get('delete')
        author_id = delete
        author_to_delete = db.session.get(Author, author_id)
        db.session.delete(author_to_delete)
        db.session.commit()
        authors = helper.get_all_results(QUERY_ALL_AUTHORS_INFO)

        return render_template('authors.html', authors=authors, message="Author deleted")

    return render_template('authors.html', authors=authors)

# with app.app_context():
#   db.create_all()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

