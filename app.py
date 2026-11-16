from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)


import os

app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")


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

    posts_with_comments = []

    for post in posts:

        comments = connection.execute(
            """
            SELECT comments.content, users.username
            FROM comments
            JOIN users ON comments.user_id = users.id
            WHERE post_id=?
            """,
            (post["id"],)
        ).fetchall()

        categories = connection.execute(
            """
            SELECT categories.name
            FROM categories
            JOIN post_categories
            ON categories.id = post_categories.category_id
            WHERE post_categories.post_id=?
            """,
            (post["id"],)
        ).fetchall()


        posts_with_comments.append(
            {
                "post": post,
                "comments": comments,
                "categories": categories
            }
        )



    connection.close()

    return render_template(
        "index.html",
        posts=posts_with_comments
    )


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

    connection = get_connection()

    categories = connection.execute(
        "SELECT * FROM categories"
    ).fetchall()


    if request.method == "POST":

        title = request.form["title"].strip()
        content = request.form["content"].strip()

        if len(title) < 3:
            connection.close()
            return "Title must be at least 3 characters"

        if len(content) < 10:
            connection.close()
            return "Content must be at least 10 characters"


        cursor = connection.execute(
            """
            INSERT INTO posts (title, content, user_id)
            VALUES (?, ?, ?)
            """,
            (title, content, session["user_id"])
        )

        post_id = cursor.lastrowid


        selected_categories = request.form.getlist("categories")


        for category_id in selected_categories:

            connection.execute(
                """
                INSERT INTO post_categories (post_id, category_id)
                VALUES (?, ?)
                """,
                (post_id, category_id)
            )


        connection.commit()
        connection.close()

        return redirect("/")


    connection.close()

    return render_template(
        "create.html",
        categories=categories
    )


@app.route("/delete/<int:id>")
def delete(id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()

    post = connection.execute(
        "SELECT * FROM posts WHERE id=?",
        (id,)
    ).fetchone()

    if post is None:
        connection.close()
        return "Publication not found"

    if post["user_id"] != session["user_id"]:
        connection.close()
        return "You cannot delete this publication"

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

    if post is None:
        connection.close()
        return "Publication not found"

    if post["user_id"] != session["user_id"]:
        connection.close()
        return "You cannot edit this publication"

    if request.method == "POST":

        title = request.form["title"].strip()
        content = request.form["content"].strip()

        if len(title) < 3:
            connection.close()
            return "Title must be at least 3 characters"

        if len(content) < 10:
            connection.close()
            return "Content must be at least 10 characters"

        connection.execute(
            "UPDATE posts SET title=?, content=? WHERE id=?",
            (title, content, id)
        )

        connection.commit()
        connection.close()

        return redirect("/")

    connection.close()

    return render_template("edit.html", post=post)

@app.route("/user/<int:id>")
def user(id):

    connection = get_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE id=?",
        (id,)
    ).fetchone()

    posts = connection.execute(
        "SELECT * FROM posts WHERE user_id=?",
        (id,)
    ).fetchall()

    connection.close()

    if user is None:
        return "User not found"

    return render_template("user.html", user=user, posts=posts)



@app.route("/comment/<int:post_id>", methods=["POST"])
def comment(post_id):

    if "user_id" not in session:
        return redirect("/login")

    content = request.form["content"].strip()

    if len(content) < 2:
        return "Comment is too short"

    connection = get_connection()

    connection.execute(
        "INSERT INTO comments (content, user_id, post_id) VALUES (?, ?, ?)",
        (content, session["user_id"], post_id)
    )

    connection.commit()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
