import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('dreams.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS dreams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


@app.route("/", methods=["GET"])
def home():
    conn = get_db_connection()
    dreams = conn.execute('SELECT * FROM dreams').fetchall()
    conn.close()
    return render_template("home.html", dreams=dreams)



app.secret_key = 'supersecretkey'  # add near the app = Flask(__name__)

@app.route("/submit", methods=["POST"])
def submit():
    dream_text = request.form["dream"].strip()
    if not dream_text:
        flash("Oops! Your dream can't be empty.", "error")
        return redirect(url_for("home"))
    conn = get_db_connection()
    conn.execute('INSERT INTO dreams (content) VALUES (?)', (dream_text,))
    conn.commit()
    conn.close()
    flash("Dream saved successfully!", "success")
    return redirect(url_for("home"))

@app.route("/delete/<int:dream_id>", methods=["POST"])
def delete(dream_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM dreams WHERE id = ?', (dream_id,))
    conn.commit()
    conn.close()
    flash("Dream deleted successfully!", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)


