from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "scio_secret_key"

DATABASE = "database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/", methods=["GET", "POST"])
def index():

    connection = get_connection()

    search = request.args.get("search")

    if search:
        posts = connection.execute(
            """
            SELECT * FROM posts
            WHERE title LIKE ? OR content LIKE ?
            """,
            (f"%{search}%", f"%{search}%")
        ).fetchall()

    else:
        posts = connection.execute(
            "SELECT * FROM posts"
        ).fetchall()

    connection.close()

    return render_template("index.html", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()

        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        connection.commit()
        connection.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        connection.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect("/")

        return "Wrong username or password"

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
@app.route("/create", methods=["GET", "POST"])
def create():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        connection = get_connection()

        connection.execute(
            "INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)",
            (title, content, session["user_id"])
        )

        connection.commit()
        connection.close()

        return redirect("/")

    return render_template("create.html")

@app.route("/delete/<int:id>")
def delete(id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()

    connection.execute(
        "DELETE FROM posts WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()

    post = connection.execute(
        "SELECT * FROM posts WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        connection.execute(
            "UPDATE posts SET title=?, content=? WHERE id=?",
            (title, content, id)
        )

        connection.commit()
        connection.close()

        return redirect("/")

    connection.close()

    return render_template("edit.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
