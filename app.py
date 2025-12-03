from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "nyckel"

# Kopplar databas via Xampp
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="",        
        database="forum"
    )

#Köra sql
def query(sql, params=(), fetchone=False):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql, params)

    if sql.strip().lower().startswith("select"):
            result = cursor.fetchone() if fetchone else cursor.fetchall()
    else:
            db.commit()
            result = None

            cursor.close()
            db.close()
            return result
    
#Visa alla inlägg
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


#Logga in med de färdiga användarna
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"] #Hämta från formulär
        p = request.form["password"] #Hämta från formulär

        #Kollar om användaren som angetts finns i XAMPP databasen
        user = query(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (u, p),
            fetchone=True
        )

        #Om användaren hittas så ska man gå vidare med att logga in
        if user:
            session["user"] = user
            return redirect("/")
        #Annars om den inte finns, kommer ett error
        else:
            return render_template("login.html", error="Fel användarnamn eller lösenord!")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

#Skapa nytt topic
@app.route("/new_topic", methods=["GET", "POST"])
def new_topic():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        user_id = session["user"]["id"]


#För att kunna starta forumet(servern)
if __name__ == "__main__":
    app.run(debug=True)
