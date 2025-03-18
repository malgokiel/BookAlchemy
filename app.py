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
            message = helper.add_new_author(request.form.get('name'),
                                            request.form.get('birthdate'),
                                            request.form.get('date_of_death'))
        return render_template('add_author.html', message=message)

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = helper.get_all_results(q.QUERY_ALL_AUTHORS)
    if request.method == 'POST':
        action = request.form.get('add')
        if action == 'Add Book':
            message = helper.add_new_book(request.form.get('ISBN'),
                                          request.form.get('title'),
                                          request.form.get('publication_year'),
                                          request.form.get('author') )
            return render_template('add_book.html', message=message, authors=authors)
    return render_template('add_book.html', authors=authors)


@app.route('/', methods=['GET'])
def index():
    recent_books = helper.get_all_results(q.QUERY_NEWEST_BOOKS)
    books = helper.get_all_results(q.QUERY_ALL_BOOKS)
    recommended_book = random.choice(books)
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
        updated_authors, message = helper.delete_record(Author, author_id, q.QUERY_ALL_AUTHORS_INFO)

        return render_template('authors.html', authors=updated_authors, message=message)

    return render_template('authors.html', authors=authors)

# with app.app_context():
#   db.create_all()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

