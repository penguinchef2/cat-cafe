from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_available_cats():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cat_cafe"
    )
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM cats WHERE available = 1")
    cats = cursor.fetchall()
    db.close()
    return cats

@app.route("/application")
def application():
    cats = get_available_cats()
    return render_template("application.html", cats=cats)

if __name__ == "__main__":
    app.run(debug=True)
