from sqlalchemy import create_engine, text

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