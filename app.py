"""
Caveats:
No rate-limiting has been added to the project, to mitigate server overload, and query returns aren't cached despite
the data not changing.
I also don't have the display of all data separated by pages, to limit the amount of work the browser has to do in
one go.
"""

import sqlite3
from types import NoneType
from typing import Any, Tuple

from flask import Flask, render_template, request

app = Flask(__name__)

DB_FILE = r"cards.db"
SORTABLE_VALUES: list = ["type", "rarity", "attribute", "subtype"]


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
        if params[0] is None and len(params) == 1:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        return tuple(self.cursor.fetchall())

    def get_all_fields_of_table(self, table) -> tuple:
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
        return tuple(data)


def get_entry(entry):
    """
    Get all rows that match a field.
    :param entry:
    :return:
    """
    db = Database(DB_FILE)
    query = "SELECT card_number, card_name, type, rarity, value, attribute, subtype, level, card_atk, " \
            "card_def, card_text FROM cards WHERE type = ? OR rarity = ? OR attribute = ? OR subtype = ?"
    entry_list = db.read_db(query, (entry, entry, entry, entry))
    db.connection.close()
    return entry_list


def get_raw_fields() -> list:
    """
    Returns all fields of the database, excluding the id field.
    This is a redundant function seeing as a method already exists in the class Database, but
    it's used so I don't have to open a connection and close it before using it as a parameter in the return_template function
    of flask (meaning there are more lines than necessary).
    In hindsight I should've just had it as a function, but oh well.
    :return:
    """
    db = Database(DB_FILE)
    fields = db.get_all_fields_of_table("cards")
    db.connection.close()
    return fields


def get_formatted_fields() -> list:
    """
    Format fields for display.
    :return:
    """
    fields = []
    for element in get_raw_fields():
        if element == "card_atk":
            fields.append("Card ATK")
        elif element == "card_def":
            fields.append("Card DEF")
        else:
            fields.append(element.replace("_", " ").capitalize())
    return fields


def get_all_data(sortby = "card_number") -> tuple[Any, ...]:
    """
    This function is project-specific.
    TODO: finish docstr and figure out why it's not working (oh and move the query request code here since it
    interacts with flask anyway)
    :return
    """
    query = "SELECT card_number, card_name, type, rarity, value, attribute, subtype, level, card_atk, " \
            "card_def, card_text FROM cards ORDER BY ? ASC"
    db = Database(DB_FILE)
    data = db.read_db(query, (sortby,))
    db.connection.close()
    return tuple(data)



@app.route('/')
def render_index():
    """
    Renders indexpage
    :return:
    """
    return render_template("index.html")


@app.route('/table/<sortable>')
def render_webpages(sortable):
    return render_template("datapage.html", raw_keys = get_raw_fields(), keys = get_formatted_fields(),
                           values = get_entry(sortable),
                           sortables = SORTABLE_VALUES, title = sortable)


@app.route('/table')
def render_all():
    sort = request.args.get('sort-by')
    if sort not in SORTABLE_VALUES and not isinstance(sort, NoneType):
        print("Invalid value:", sort)
        sort = None
    if isinstance(sort, NoneType):
        sort = "card_number"  # this is redundant, but I feel as though it's good practice regardless.
    return render_template("datapage.html", raw_keys = get_raw_fields(), keys = get_formatted_fields(),
                           values = get_all_data(sortby = sort),
                           sortables = SORTABLE_VALUES, title = "All")


@app.route('/card')
def render_cards():
    return render_template("card.html", keys = get_formatted_fields(), values = get_all_data(), title = "All")


@app.route('/search', methods = ['GET', 'POST'])
def render_search():
    """
    Renders searched items and handles searching functionality.
    :return:
    :rtype:
    """
    search = request.form['search']
    title = "Search for " + search
    # Search query
    query = "SELECT card_name, rarity, type, card_text FROM cards WHERE card_name like ? OR card_number like ? OR " \
            "type like ? OR rarity like ?"
    search = "%" + search + "%"
    db = Database(DB_FILE)
    tag_list = db.read_db(query, (search, search, search, search))
    db.connection.close()
    return render_template("datapage.html", raw_keys = get_raw_fields(), keys = get_formatted_fields(),
                           values = tag_list,
                           sortables = SORTABLE_VALUES, title = title)


if __name__ == '__main__':
    app.run()
