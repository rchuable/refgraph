'''
Project:    CS50 Week 10 - Reference Graph
Author:     Regina Chua
Notes:      The project guidelines can be found at https://cs50.harvard.edu/x/2024/project/
            The project files live on https://github.com/code50/19302573/tree/main/project

References (see why I need this app???)
- finance <- week 9 pset, it's a handy framework for this!
- https://flask.palletsprojects.com/en/stable/quickstart/
'''

import os
import sqlite3
from flask import Flask, render_template, g, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'
app.secret_key = "ReginaChua!369damnshefine"


## Establish connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

## Homepage
@app.route("/")
def index():
    return render_template("index.html")

## Testing: Making sure that it lists the tables
@app.route('/test_db')
def test_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    return f"Tables in the database: {tables}"

## Upload
@app.route("/upload", methods=["GET", "POST"])
def upload():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        file = request.files.get("file")
        url = request.form.get("url")

        # save file
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join("uploads", filename))
            cursor.execute("INSERT INTO files (filename, filetype) VALUES (?, ?)", (filename, 'file'))
            conn.commit()
            flash("File uploaded successfully.")

        # validate url
        elif url:
            if url.startswith("http"):
                cursor.execute("INSERT INTO urls (url) VALUES (?)", (url,))
                conn.commit()
                flash("URL added successfully.")
            else:
                flash("Invalid URL. Please enter a valid link.")

        else:
            flash("Please upload a file or enter a URL.")

        return redirect(url_for("upload"))

    return render_template("upload.html")

# Ayo RUN
if __name__ == "__main__":
    app.run(debug=True)
