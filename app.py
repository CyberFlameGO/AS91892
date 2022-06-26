"""
TODO: Potentially make a table_name variable, and make the database class handle as much as possible

Caveats:
No rate-limiting has been added to the project, to mitigate server overload, and query returns aren't cached despite
the data not changing.
"""

import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)

DB_FILE = r"cards.db"


class Database(object):
    """
    Database class for SQLite3.
    TODO: Potentially make a variable for table creation query
    """

    def __init__(self, db_name: str, query_file: str = r"query.sql") -> None:
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
            # todo: when i update these comments for this project, explain why i'm using real as opposed to
            #  double/float (the reason is that i don't need double precision decimals)
            self.cursor.executescript(open(query_file, 'r', encoding = "utf8").read())
        except sqlite3.Error as e:
            print(e)

    def read_db(self, query, params: tuple = (None,)):
        """
        Runs a query then fetches and returns output of the query.
        :param query:
        :param params:
        :return:
        """
        if params[0] is not None or len(params) >= 1:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_fields_of_table(self, table) -> list:
        """
        Gets all columns (fields) excluding the id field, of a table using SQLite's PRAGMA command.
        Having this as a Python is more convenient than having it as a sqlite3 function
        :param table:
        :return:
        """
        self.cursor.execute(f"PRAGMA table_info({table});")
        row_info = self.cursor.fetchall()
        del row_info[0]
        data = []
        for val in row_info:
            data.append(val[1])
        return data


def get_tags(tag_type):
    """
    Get the tags for a particular type of web tag
    :param tag_type:
    :return:
    """
    db = Database(DB_FILE)
    query = "SELECT first_name, last_name, gender, address FROM MOCK_DATA WHERE dob=?"
    tag_list = db.read_db(query, (tag_type,))
    db.connection.close()
    print(tag_list)
    return tag_list


def get_all_data():
    """
    This function is project-specific.
    """
    query = "SELECT card_number, card_name, type, rarity, value, attribute, subtype, level, card_atk, " \
            "card_def, card_text FROM cards"
    db = Database(DB_FILE)
    fields = []
    for element in db.get_all_fields_of_table("cards"):
        if element == "card_atk":
            fields.append("Card ATK")
        elif element == "card_def":
            fields.append("Card DEF")
        else:
            fields.append(element.replace("_", " ").capitalize())
    data = db.read_db(query)
    db.connection.close()
    return fields, data

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


@app.route('/tags/<tag_type>')
def render_webpages(tag_type):
    return render_template("datapage.html", values = get_tags(tag_type), title = tag_type)


@app.route('/all')
def render_all():
    #todo: change variable names
    val1, val2 = get_all_data()
    return render_template("datapage.html", keys = val1, values = val2, title = "All")


@app.route('/all2')
def render_all2():
    #todo: change variable names
    val1, val2 = get_all_data()
    return render_template("card.html", keys = val1, values = val2, title = "All")


@app.route('/search', methods = ['GET', 'POST'])
def render_search():
    search = request.form['search']
    title = "Search for " + search
    # Search query
    query = "SELECT first_name, last_name FROM MOCK_DATA WHERE " \
            "gender like ? OR dob like ?"
    search = "%" + search + "%"
    db = Database(DB_FILE)
    tag_list = db.read_db(query, (search, search))
    db.connection.close()
    return render_template("datapage.html", values = tag_list, title = title)


if __name__ == '__main__':
    app.run()
