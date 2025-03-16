from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///data/library.sqlite')

def get_all_authors():
    QUERY_ALL_AUTHORS = ("SELECT authors.id, authors.name "
                         "FROM authors")
    try:
        with engine.connect() as connection:
            results = connection.execute(text(QUERY_ALL_AUTHORS))
            authors = results.fetchall()
        return authors
    except Exception as e:
        print(e)
        return []