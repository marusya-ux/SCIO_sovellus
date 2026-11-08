import sqlite3

DATABASE = "database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_connection()

    with open("schema.sql") as file:
        connection.executescript(file.read())

    connection.close()


if __name__ == "__main__":
    create_database()
