from pyexpat.errors import messages

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert
from data_models import db, Author, Book

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


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

# with app.app_context():
#   db.create_all()