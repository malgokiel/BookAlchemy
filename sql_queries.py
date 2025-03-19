"""SQL queries used in app.py"""

QUERY_ALL_AUTHORS = ("SELECT authors.id, authors.name "
                     "FROM authors")
QUERY_ALL_BOOKS = ("SELECT books.*, authors.name "
                   "FROM books "
                   "JOIN authors "
                   "ON books.author_id = authors.id")
QUERY_SORTED_AUTHORS = ("SELECT books.*, authors.name "
                        "FROM books "
                        "JOIN authors "
                        "ON books.author_id=authors.id "
                        "ORDER BY authors.name")
QUERY_SORTED_TITLES = ("SELECT books.*, authors.name "
                       "FROM books "
                       "JOIN authors "
                       "ON books.author_id=authors.id "
                       "ORDER BY books.title")
QUERY_SORTED_YEARS = ("SELECT books.*, authors.name "
                      "FROM books "
                      "JOIN authors "
                      "ON books.author_id=authors.id "
                      "ORDER BY books.publication_year DESC")
QUERY_BY_SEARCH_TERM = ("SELECT books.*, authors.name "
                        "FROM books "
                        "JOIN authors "
                        "ON books.author_id = authors.id "
                        "WHERE books.title "
                        "LIKE CONCAT('%', :search_for, '%') "
                        "OR authors.name "
                        "LIKE CONCAT('%', :search_for, '%')")
QUERY_ALL_AUTHORS_INFO = ("SELECT authors.*, COUNT(books.author_id) AS book_count "
                          "FROM authors "
                          "LEFT JOIN books "
                          "ON authors.id = books.author_id "
                          "GROUP BY authors.name")
QUERY_NEWEST_BOOKS = ("SELECT books.*, authors.name "
                      "FROM books "
                      "JOIN authors "
                      "ON books.author_id = authors.id "
                      "ORDER BY books.id DESC "
                      "LIMIT 3")
QUERY_VALID_AUTHOR_IDS = "SELECT authors.id FROM authors"