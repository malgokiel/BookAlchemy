from pyexpat.errors import messages
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert, text, create_engine
from data_models import db, Author, Book
import helper
import random
import sql_queries as q

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/malgorzata/PycharmProjects/BookAlchemy/data/library.sqlite'
db.init_app(app)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        action = request.form.get('add')
        if action == 'Add Author':

            name = request.form.get('name')
            birthdate = request.form.get('birthdate')
            death = request.form.get('date_of_death')

            if helper.validate_author_params(name, birthdate, death) is True:
                message = helper.add_new_author(name, birthdate, death)
            else:
                _, message = helper.validate_author_params(name, birthdate, death)

        return render_template('add_author.html', messages=message)

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = helper.get_all_results(q.QUERY_ALL_AUTHORS)
    if request.method == 'POST':
        action = request.form.get('add')
        if action == 'Add Book':

            isbn = request.form.get('ISBN')
            title = request.form.get('title')
            year = request.form.get('publication_year')
            author_id = request.form.get('author')

            if helper.validate_book_params(isbn, title, year, author_id) is True:
                message = helper.add_new_book(isbn, title, year, author_id)
            else:
                _, message = helper.validate_book_params(isbn, title, year, author_id)

            return render_template('add_book.html', messages=message, authors=authors)
    return render_template('add_book.html', authors=authors)


@app.route('/', methods=['GET'])
def index():
    recent_books = helper.get_all_results(q.QUERY_NEWEST_BOOKS)
    books = helper.get_all_results(q.QUERY_ALL_BOOKS)
    if books:
        recommended_book = random.choice(books)
    else:
        recommended_book = []
    return render_template('index.html', recommended_book=recommended_book, books=recent_books)


@app.route('/books', methods=['GET', 'POST'], endpoint='books')
def all_books():
    books = helper.get_all_results(q.QUERY_ALL_BOOKS)
    if request.method == 'POST':

        message = None
        action = request.form.get('sort')
        delete = request.form.get('delete')
        search = request.form.get('search')

        actions = {'author': q.QUERY_SORTED_AUTHORS,
                   'title': q.QUERY_SORTED_TITLES,
                   'year': q.QUERY_SORTED_YEARS}

        if action:
            books = helper.get_all_results(actions[action])
        elif delete:
            book_title_form = request.form.get('book_title')
            for book in books:
                if str(book[0]) == delete and book[2] == book_title_form:
                    books, message = helper.delete_record(Book, delete, q.QUERY_ALL_BOOKS)
        elif search:
            books = helper.get_all_results(q.QUERY_BY_SEARCH_TERM,{'search_for':search})

        return render_template('books.html', books=books, message=message)

    return render_template('books.html', books=books)


@app.route('/authors', methods=['GET', 'POST'])
def all_authors():
    authors = helper.get_all_results(q.QUERY_ALL_AUTHORS_INFO)
    if request.method == 'POST':
        author_id = request.form.get('delete')
        author_name_form = request.form.get('author_name')
        for author in authors:
            if author[0] == author_id and author[1] == author_name_form:
                updated_authors, message = helper.delete_record(Author, author_id, q.QUERY_ALL_AUTHORS_INFO)
                return render_template('authors.html', authors=updated_authors, message=message)

    return render_template('authors.html', authors=authors)

# with app.app_context():
#   db.create_all()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

