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


@app.route("/become_member")
def become_member():
    if not session.get("userid"):
        return redirect("/login")
    return render_template("already_member.html")


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
        SELECT id, name
        FROM cats
        WHERE available = TRUE
    """)
    cats = cur.fetchall()
    cur.close()
    return cats


# ---------------- REGISTER ---------------- #

@app.route("/register")
def register():
    if session.get("userid"):
        return redirect("/")
    return render_template("register.html")


@app.route("/register_send", methods=["POST"])
def register_user():
    if session.get("userid"):
        return jsonify(message="Already logged in"), 403

    cur = mysql.connection.cursor()

    email = request.form.get("email")

    cur.execute("SELECT userid FROM userinformation WHERE emailid = %s", (email,))
    if cur.fetchone():
        cur.close()
        return jsonify(message="Email already exists"), 400

    hashed_password = hashing.generate_password_hash(
        request.form.get("password")
    ).decode('utf-8')

    cur.execute("""
        INSERT INTO userinformation (emailid, username, password, name)
        VALUES (%s, %s, %s, %s)
    """, (
        email,
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

    session["user"] = name
    session["email"] = request.form.get("email")
    session["userid"] = userid
    session["just_logged_in"] = True

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

    # ---------------- POST ---------------- #
    if request.method == "POST":

        # already applied?
        cur.execute("""
            SELECT id FROM applications
            WHERE userid = %s
        """, (session["userid"],))

        if cur.fetchone():
            cur.close()
            return jsonify({
                "success": False,
                "message": "You already have an application 🐾"
            })

        cat_id = request.form.get("cat_id")

        # cat already adopted?
        cur.execute("""
            SELECT id FROM applications
            WHERE cat_id = %s AND status = 'approved'
        """, (cat_id,))

        if cur.fetchone():
            cur.close()
            return jsonify({
                "success": False,
                "message": "This cat has already been adopted!"
            })

        cur.execute("""
            INSERT INTO applications
            (userid, full_name, phone, email, address, cat_id,
             household_size, pets, housing, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'pending')
        """, (
            session["userid"],
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

    # ---------------- GET ---------------- #

    cur.execute("""
        SELECT id, status
        FROM applications
        WHERE userid = %s
        ORDER BY id DESC
        LIMIT 1
    """, (session["userid"],))

    app_row = cur.fetchone()

    already_applied = False
    already_adopted = False
    existing_status = None

    if app_row:
        already_applied = True
        existing_status = app_row[1]

        if app_row[1] == "approved":
            already_adopted = True

    cur.execute("""
    SELECT name, emailid
    FROM userinformation
    WHERE userid = %s
""", (session["userid"],))

    user_info = cur.fetchone()
    cur.close()


    return render_template(
        "application.html",
        cats=get_available_cats(),
        already_applied=already_applied,
        already_adopted=already_adopted,
        existing_status=existing_status,
        user=user_info 
    )


# ---------------- APPROVE ---------------- #

@app.route("/approve/<int:app_id>")
def approve(app_id):
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT cat_id FROM applications
        WHERE id = %s
    """, (app_id,))
    result = cur.fetchone()

    if not result:
        cur.close()
        return "Application not found"

    cat_id = result[0]

    cur.execute("""
        UPDATE applications
        SET status = 'approved'
        WHERE id = %s
    """, (app_id,))

    cur.execute("""
        UPDATE cats
        SET available = FALSE
        WHERE id = %s
    """, (cat_id,))

    mysql.connection.commit()
    cur.close()

    return "Application approved and cat marked unavailable!"


# ---------------- REJECTION ---------------- #

@app.route("/reject/<int:app_id>")
def reject(app_id):
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM applications WHERE id = %s", (app_id,))

    mysql.connection.commit()
    cur.close()

    session["rejected_popup"] = True
    return redirect("/my_application")


# ---------------- MY APPLICATION ---------------- #

@app.route("/my_application")
def my_application():
    if not session.get("userid"):
        return redirect("/login")

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT a.full_name, a.phone, a.email, a.address,
               c.name, a.household_size, a.pets, a.housing, a.status
        FROM applications a
        JOIN cats c ON a.cat_id = c.id
        WHERE a.userid = %s
    """, (session["userid"],))

    app_data = cur.fetchone()
    cur.close()

    rejected_popup = session.pop("rejected_popup", False)

    return render_template(
        "my_application.html",
        app=app_data,
        rejected_popup=rejected_popup
    )


# ---------------- RUN ---------------- #

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