from sqlalchemy import create_engine, text
from app import db
from data_models import Author, Book
import sql_queries as q

engine = create_engine('sqlite:///data/library.sqlite')

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
    return f"{new_book.title} added."


def delete_record(class_name, record_id, query):
    record_to_delete = db.session.get(class_name, record_id)
    db.session.delete(record_to_delete)
    db.session.commit()
    return get_all_results(query), f"{record_to_delete.name if class_name==Author else record_to_delete.title} deleted."