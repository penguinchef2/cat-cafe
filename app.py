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


@app.route("/menu")
def menu():
    return render_template("menu.html")


# ---------------- REVIEWS ---------------- #

@app.route("/reviews")
def reviews():
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT r.rating, r.review_text, r.created_at, u.name
        FROM reviews r
        JOIN userinformation u ON r.userid = u.userid
        ORDER BY r.created_at DESC
    """)

    reviews = cur.fetchall()
    cur.close()

    return render_template("reviews.html", reviews=reviews)


@app.route("/add_review", methods=["POST"])
def add_review():
    if not session.get("userid"):
        return jsonify(message="Not logged in")

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO reviews (userid, rating, review_text)
        VALUES (%s, %s, %s)
    """, (
        session["userid"],
        request.form.get("rating"),
        request.form.get("review_text")
    ))

    mysql.connection.commit()
    cur.close()

    return jsonify(success=True)


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

    cur.execute("""
        SELECT id, name FROM cats
        WHERE id NOT IN (
            SELECT cat_id FROM applications WHERE status = 'approved'
        )
    """)

    cats = cur.fetchall()
    cur.close()
    return cats


# ---------------- REGISTER ---------------- #

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register_send", methods=["POST"])
def register_user():
    cur = mysql.connection.cursor()

    hashed_password = hashing.generate_password_hash(
        request.form.get("password")
    ).decode('utf-8')

    cur.execute("""
        INSERT INTO userinformation (emailid, username, password, name)
        VALUES (%s, %s, %s, %s)
    """, (
        request.form.get("email"),
        request.form.get("username"),
        hashed_password,
        request.form.get("name")
    ))

    mysql.connection.commit()
    cur.close()

    return jsonify(success=True)


# ---------------- LOGIN ---------------- #

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_send", methods=["POST"])
def login_user():
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT userid, password, name
        FROM userinformation
        WHERE emailid = %s
    """, (request.form.get("email"),))

    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify(message="invalid email")

    userid, hashed_password, name = user

    if not hashing.check_password_hash(hashed_password, request.form.get("password")):
        return jsonify(message="invalid password")

    session['user'] = name
    session['email'] = request.form.get("email")
    session['userid'] = userid
    session['just_logged_in'] = True

    return jsonify(success=True)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- APPLICATION ---------------- #

@app.route("/application", methods=["GET", "POST"])
def application():
    if not session.get("userid"):
        return redirect("/login")

    cur = mysql.connection.cursor()

    # get selected cat from URL
    selected_cat = request.args.get("cat_id")

    # check if existing application
    cur.execute("""
        SELECT id, status FROM applications
        WHERE email = %s
    """, (session["email"],))

    existing_app = cur.fetchone()

    # ---------------- POST ---------------- #
    if request.method == "POST":

        if existing_app:
            cur.close()
            return jsonify({
                "success": False,
                "message": f"You already have a {existing_app[1]} application 🐾"
            })

        cat_id = request.form.get("cat_id")

        cur.execute("""
            SELECT id FROM applications
            WHERE cat_id = %s AND status = 'approved'
        """, (cat_id,))
        taken = cur.fetchone()

        if taken:
            cur.close()
            return jsonify({
                "success": False,
                "message": "This cat has already been adopted!"
            })

        cur.execute("""
            INSERT INTO applications
            (full_name, phone, email, address, cat_id, household_size, pets, housing, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'pending')
        """, (
            request.form['full_name'],
            request.form['phone'],
            session["email"],
            request.form['address'],
            cat_id,
            request.form['household'],
            request.form['pets'],
            request.form['housing']
        ))

        mysql.connection.commit()
        cur.close()

        return jsonify(success=True)

    # ---------------- AUTOFILL ---------------- #

    cur.execute("""
        SELECT name, emailid
        FROM userinformation
        WHERE userid = %s
    """, (session["userid"],))

    user = cur.fetchone()
    cur.close()

    return render_template(
        "application.html",
        cats=get_available_cats(),
        user=user,
        already_applied=existing_app is not None,
        existing_status=existing_app[1] if existing_app else None,
        selected_cat=selected_cat   # 👈 NEW
    )


# ---------------- APPROVE ---------------- #

@app.route("/approve/<int:app_id>")
def approve(app_id):
    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE applications
        SET status = 'approved'
        WHERE id = %s
    """, (app_id,))

    mysql.connection.commit()
    cur.close()

    return "Application approved!"


# ---------------- MY APPLICATION ---------------- #

@app.route("/my_application")
def my_application():
    if not session.get("user"):
        return redirect("/login")

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT a.full_name, a.phone, a.email, a.address,
               c.name, a.household_size, a.pets, a.housing, a.status
        FROM applications a
        JOIN cats c ON a.cat_id = c.id
        WHERE a.email = %s
    """, (session.get("email"),))

    app_data = cur.fetchone()
    cur.close()

    return render_template("my_application.html", app=app_data)


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True, port=5050)