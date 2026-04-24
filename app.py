from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL config
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cat_cafe'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)


# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/cats")
def cats():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cats")
    cats_list = cur.fetchall()
    cur.close()

    return render_template("cats.html", cats=cats_list)

@app.route("/reviews")
def reviews():
    return render_template("reviews.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/cat/<int:cat_id>")
def cat_profile(cat_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cats WHERE id = %s", (cat_id,))
    cat = cur.fetchone()
    cur.close()

    return render_template("profile.html", cat=cat)

if __name__ == "__main__":
    app.run(debug=True, port=5050)