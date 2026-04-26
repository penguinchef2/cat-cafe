from flask import Flask, render_template, request, jsonify, session, redirect
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt   

app = Flask(__name__)
app.secret_key = "secretkey123"

hashing = Bcrypt(app)

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
    show_welcome = session.pop('just_logged_in', False)
    return render_template("home.html", show_welcome=show_welcome)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/reviews")
def reviews():
    return render_template("reviews.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


# ---------------- CATS ---------------- #

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


def get_available_cats():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name FROM cats WHERE available = TRUE")
    cats = cur.fetchall()
    cur.close()
    return cats


# ---------------- LOGIN ---------------- #

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_send", methods=["POST"])
def login_user():
    cur = mysql.connection.cursor()

    email = request.form.get("email")
    password = request.form.get("password")

    cur.execute("""
        SELECT password, name FROM userinformation
        WHERE emailid = %s
    """, (email,))

    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify(message="invalid email")

    hashed_password = user[0]
    name = user[1]

    if not hashing.check_password_hash(hashed_password, password):
        return jsonify(message="invalid password")

    # 🔥 FIX: make session reliable
    session['user'] = name
    session['email'] = email
    session['just_logged_in'] = True

    return jsonify(success=True)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- REGISTER ---------------- #

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register_send", methods=["POST"])
def register_user():
    cur = mysql.connection.cursor()

    name = request.form.get("name")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    hashed_password = hashing.generate_password_hash(password).decode('utf-8')

    cur.execute("""
        INSERT INTO userinformation (emailid, username, password, name)
        VALUES (%s, %s, %s, %s)
    """, (email, username, hashed_password, name))

    mysql.connection.commit()
    cur.close()

    return jsonify(success=True)


# ---------------- APPLICATION ---------------- #

@app.route("/application", methods=["GET", "POST"])
def application():
    if request.method == "POST":
        cur = mysql.connection.cursor()

        email = session.get("email")

        if not email:
            return jsonify(message="Not logged in")

        # always UPDATE or INSERT safely (upsert style)
        cur.execute("""
            SELECT id FROM applications WHERE email = %s
        """, (email,))
        existing = cur.fetchone()

        if existing:
            cur.execute("""
                UPDATE applications
                SET full_name=%s,
                    phone=%s,
                    address=%s,
                    cat_id=%s,
                    household_size=%s,
                    pets=%s,
                    housing=%s
                WHERE email=%s
            """, (
                request.form['full_name'],
                request.form['phone'],
                request.form['address'],
                request.form['cat_id'],
                request.form['household'],
                request.form['pets'],
                request.form['housing'],
                email
            ))
        else:
            cur.execute("""
                INSERT INTO applications
                (full_name, phone, email, address, cat_id, household_size, pets, housing)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                request.form['full_name'],
                request.form['phone'],
                email,
                request.form['address'],
                request.form['cat_id'],
                request.form['household'],
                request.form['pets'],
                request.form['housing']
            ))

        mysql.connection.commit()
        cur.close()

        return jsonify(success=True)

    return render_template("application.html", cats=get_available_cats())


# ---------------- MY APPLICATION ---------------- #

@app.route("/my_application")
def my_application():
    if not session.get("user"):
        return redirect("/login")

    email = session.get("email")

    # debug!
    if not email:
        return "Session email missing. Please log in again."

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT a.full_name, a.phone, a.email, a.address,
               c.name, a.household_size, a.pets, a.housing
        FROM applications a
        JOIN cats c ON a.cat_id = c.id
        WHERE a.email = %s
    """, (email,))

    app_data = cur.fetchone()
    cur.close()

    return render_template("my_application.html", app=app_data)


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True, port=5050)