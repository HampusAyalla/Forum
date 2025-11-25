from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.secret_key = "nyckel"

def db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="",        
        database="forum"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s",
                   (username, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        session["user_id"] = user[0]
        session["username"] = username
        return redirect("/topics")
    else:
        return "Fel användarnamn eller lösenord"


