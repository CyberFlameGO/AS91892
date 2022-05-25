import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)

DB_FILE = r"webtags.db"


class Database(object):
    """
    Database class
    """

    def __init__(self, db_name: str):
        """
        Database initialization logic
        :param db_name:
        """
        try:
            # Initialize the database (if it doesn't exist, a new file is created)
            self.connection = sqlite3.connect(db_name)
            # Set the cursor variable
            self.cursor = self.connection.cursor()
            # create a db table if it doesn't exist.
            # I'm aware that the autoincrement is redundant, as with having an 'id' column at all as
            # there's a built-in rowid which the id column just aliases to (unless using 'WITHOUT ROWID', which i'm not
            # doing right now as it's not worth the effort), but I've set it up this way on purpose.
            # Switching to no rowid is something I may do if I ever come back to working on this after submitting it.
            self.cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS Tags
                (
                    'id'                INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    'type'              VARCHAR(10) NOT NULL,
                    'tag'               BLOB NOT NULL,
                    'description'       TEXT NOT NULL
                )
                '''
            )
        except sqlite3.Error as e:
            print(e)

    def read_db(self):
        query = "SELECT tag, description FROM tags WHERE type = ?"
        self.cursor.execute(query, ('HTML', ))
        return self.cursor.fetchall()

    def insert_row(self, length: float):
        """
        TODO: ADAPT FOR PROJECT IN FUTURE
        https://docs.python.org/3/library/sqlite3.html
        Inserts a new row for an attempt
        :param length:
        """
        self.cursor.execute(f"INSERT INTO Tags (attempt_length) VALUES ({length})")
        self.connection.commit()


@app.route('/meme')
def hello_world():
    """
    Prints query to thing
    :return:
    """
    return ' '.join([*request.args.to_dict()])


@app.route('/')
def render_index():
    """
    Renders indexpage
    :return:
    """
    return render_template("index.html")


@app.route('/contact')
def render_contact():
    """
    Renders contactpage
    :return:
    """
    return render_template("contact.html")


@app.route('/data')
def render_data():
    """
    dn
    :return:
    """
    db = Database(DB_FILE)
    tag_list = db.read_db()
    db.connection.close()
    return render_template("datapage.html", tags = tag_list)


if __name__ == '__main__':
    app.run()
