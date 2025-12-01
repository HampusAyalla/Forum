from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "nyckel"

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="",        
        database="forum"
    )

def query(sql, params=(), fetchone=False):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql, params)

@app.route("/")
def index():
    topics = query("""
        SELECT topics.*, users.fullname 
        FROM topics
        JOIN users ON users.id = topics.user_id
        ORDER BY topics.created DESC
    """)
    return render_template("Index.html", topics=topics, user=session.get("user"))


@app.route("/")
def index():
    return render_template("Index.html")


