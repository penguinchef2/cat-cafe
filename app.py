from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
hashing =  Bcrypt(app)

# MySQL config
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cats'
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


@app.route("/cat/<int:cat_id>")
def cat_profile(cat_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cats WHERE id = %s", (cat_id,))
    cat = cur.fetchone()
    cur.close()
    return render_template("profile.html", cat=cat)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


# ---------------- HELPERS ---------------- #

def get_available_cats():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name FROM cats WHERE available = TRUE")
    cats = cur.fetchall()
    cur.close()
    return cats


# ---------------- application form ---------------- #

@app.route("/application", methods=["GET", "POST"])
def application():
    if request.method == "POST":
        cur = mysql.connection.cursor()

        full_name = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        cat_id = request.form['cat_id']
        household = request.form['household']
        pets = request.form['pets']
        housing = request.form['housing']

        cur.execute("""
            INSERT INTO applications
            (full_name, phone, email, address, cat_id, household_size, pets, housing)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (full_name, phone, email, address, cat_id, household, pets, housing))

        # mark cat as not available once user picks them, can see change in cats table
        cur.execute("""
            UPDATE cats
            SET available = FALSE
            WHERE id = %s
        """, (cat_id,))

        mysql.connection.commit()
        cur.close()

        return "OK"
    cats = get_available_cats()
    return render_template("application.html", cats=cats)

@app.route("/register_send" , methods = ["POST"])
def register_user():
    cur = mysql.connection.cursor()

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")

    protectPwd = hashing.generate_password_hash(password)

    cur.execute("""
            INSERT INTO userinformation
            (username, emailid, password, name)
            VALUES (%s,%s,%s,%s)
        """, (username, email, protectPwd, name))
    
    mysql.connection.commit()
    cur.close()
    return jsonify(message = "succesfully stored")

@app.route("/login_send" , methods = ["POST"])
def login_user():
    cur = mysql.connection.cursor()

    email = request.form.get("email")
    password = request.form.get("password")

    #print (email, password)

    cur.execute("""
            SELECT password FROM userinformation
            WHERE emailid = %s 
        """, ( email,))
    tmp =  cur.fetchone()
    #print (tmp)
    user = tmp[0]
    #print(user)
    cur.close()
    result = hashing.check_password_hash(user, password)
    if result is False:
        return jsonify(message = "invalid password")
    return jsonify(email)




if __name__ == "__main__":
    app.run(debug=True, port=5050)