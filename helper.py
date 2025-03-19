from sqlalchemy import create_engine, text
from app import db
from data_models import Author, Book
import datetime
import sql_queries as q
engine = create_engine('sqlite:///data/library.sqlite')

TODAY = datetime.date.today()
CURRENT_YEAR = datetime.datetime.now().strftime("%Y")

def get_all_results(query, params=None):

    try:
        with engine.connect() as connection:
            results = connection.execute(text(query), params)
            rows = results.fetchall()
        return rows
    except Exception as e:
        print(e)
        return []


def add_new_author(name, birthday, death):
    new_author = Author(name=name,
                        birth_date=birthday,
                        date_of_death=death)
    print(death <= str(TODAY))
    db.session.add(new_author)
    db.session.commit()
    return f"{new_author.name} added."


def add_new_book(isbn, title, year, author_id):
    new_book = Book(isbn=isbn,
                    title=title,
                    publication_year=year,
                    author_id=author_id)
    db.session.add(new_book)
    db.session.commit()
    return [f"{new_book.title} added."]


def delete_record(class_name, record_id, query):
    record_to_delete = db.session.get(class_name, record_id)
    db.session.delete(record_to_delete)
    db.session.commit()
    return get_all_results(query), [f"{record_to_delete.name if class_name==Author else record_to_delete.title} deleted."]


def validate_author_params(name, birthdate, death):
    messages = []
    if not name:
        messages.append("Name missing")
    if not birthdate:
        messages.append("Birthdate missing")
    else:
        if birthdate > str(TODAY) or death > str(TODAY):
            messages.append("Date in the future")
        if death and death < birthdate:
            messages.append("Death before birth")

    if messages:
        return False, messages
    else:
        return True


def validate_book_params(isbn, title, year, author_id):
    author_ids = get_all_results(q.QUERY_VALID_AUTHOR_IDS)
    valid_ids = [valid_id for id_row in author_ids for valid_id in id_row]
    messages = []

    if not isbn or len(isbn) not in [9, 13]:
        messages.append("Invalid ISBN length")
    elif isbn.isnumeric() is False:
        messages.append("ISBN should contain only numerals")

    try:
        year = int(year)
        if not year or 0 > year > int(CURRENT_YEAR):
            messages.append(f'Year must be higher than 0 and less than {CURRENT_YEAR}')
    except ValueError:
        messages.append("Year must be a number")


    if not title:
        messages.append("Title missing")

    if not author_id or int(author_id) not in valid_ids:
        messages.append("Choose available author")

    if messages:
        return False, messages
    else:
        return True

def check_if_exists(record_id):
    pass

