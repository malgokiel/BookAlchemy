from flask import Flask, render_template, request
from data_models import db, Author, Book
import helper
import random
import sql_queries as q
import os

# Set the app up and establish db connection
current_directory = os.getcwd()
database_path = os.path.join(current_directory, 'data', 'library.sqlite')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{database_path}'
db.init_app(app)


@app.route('/', methods=['GET'])
def index():
    """
    Fetches recently added books from DB and randomly picks a next read from available titles.
    Renders a home page with recently added books and recommended reads.
    """
    recent_books = helper.get_all_results(q.QUERY_NEWEST_BOOKS)
    books = helper.get_all_results(q.QUERY_ALL_BOOKS)
    if books:
        recommended_book = random.choice(books)
    else:
        recommended_book = []
    return render_template('index.html', recommended_book=recommended_book, books=recent_books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    GET: renders a template with a relevant form.
    POST:
    Function fetches information from a form, calls a input validation helper function and if check is successful
    adds an author to the database by calling an add_new_author helper function.
    Renders an input form and displays relevant messages.
    """
    if request.method == 'POST':
        action = request.form.get('add')
        if action == 'Add Author':

            name = request.form.get('name')
            birthdate = request.form.get('birthdate')
            death = request.form.get('date_of_death')

            if helper.are_author_params_valid(name, birthdate, death) is True:
                message = helper.add_new_author(name, birthdate, death)
            else:
                _, message = helper.are_author_params_valid(name, birthdate, death)

        return render_template('add_author.html', messages=message)

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    GET: renders a template with a relevant form.
    POST:
    Function fetches information from a form, calls a input validation helper function and if check is successful
    adds a book to the database by calling an add_new_book helper function.
    Renders an input form and displays relevant messages.
    """
    authors = helper.get_all_results(q.QUERY_ALL_AUTHORS)
    if request.method == 'POST':
        action = request.form.get('add')
        if action == 'Add Book':

            isbn = request.form.get('ISBN')
            title = request.form.get('title')
            year = request.form.get('publication_year')
            author_id = request.form.get('author')

            if helper.are_book_params_valid(isbn, title, year, author_id) is True:
                message = helper.add_new_book(isbn, title, year, author_id)
            else:
                _, message = helper.are_book_params_valid(isbn, title, year, author_id)

            return render_template('add_book.html', messages=message, authors=authors)
    return render_template('add_book.html', authors=authors)





@app.route('/books', methods=['GET', 'POST'], endpoint='books')
def all_books():
    """
    GET: renders a template displaying all books fetched from a db.
    POST:
    Supports sorting, deleting and searching books by fetching action type from a form
    and calling relevant helper function.
    Renders a template with all books matching criteria and messages if any.
    """
    books = helper.get_all_results(q.QUERY_ALL_BOOKS)
    if request.method == 'POST':

        message = None
        sort = request.form.get('sort')
        delete = request.form.get('delete')
        search = request.form.get('search')


        if sort:
            sort_options = {'author': q.QUERY_SORTED_AUTHORS,
                            'title': q.QUERY_SORTED_TITLES,
                            'year': q.QUERY_SORTED_YEARS}
            books = helper.get_all_results(sort_options[sort])
        elif delete:
            book_title_form = request.form.get('book_title')
            for book in books:
                if str(book[0]) == delete and book[2] == book_title_form:
                    books, message = helper.delete_record(Book, delete, q.QUERY_ALL_BOOKS)
        elif search:
            books = helper.get_all_results(q.QUERY_BY_SEARCH_TERM,{'search_for':search})

        return render_template('books.html', books=books, messages=message)

    return render_template('books.html', books=books)


@app.route('/authors', methods=['GET', 'POST'])
def all_authors():
    """
    GET: renders a template displaying all authors fetched from a db.
    POST:
    Supports deleting an author if the author ID and NAME match and are valid.
    Deletes a record using helper function and renders the authors page, passes all relevant messages.
    """
    authors = helper.get_all_results(q.QUERY_ALL_AUTHORS_INFO)
    if request.method == 'POST':
        author_id = request.form.get('delete')
        author_name_form = request.form.get('author_name')
        for author in authors:
            if str(author[0]) == author_id and author[1] == author_name_form:
                updated_authors, message = helper.delete_record(Author, author_id, q.QUERY_ALL_AUTHORS_INFO)
                return render_template('authors.html', authors=updated_authors, messages=message)

    return render_template('authors.html', authors=authors)


# Creates DB and tables. Left in and commented out as suggested in the assignment.
# with app.app_context():
#   db.create_all()


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
