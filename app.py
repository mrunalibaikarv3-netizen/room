from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "roomconnect_secret_key"

app.config.from_object(Config)

mysql = MySQL(app)

# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# CHOOSE ROLE
# ==========================

@app.route("/choose-role")
def choose_role():
    return render_template("choose_role.html")


# ==========================
# OWNER LOGIN
# ==========================

@app.route("/owner-login", methods=["GET", "POST"])
def owner_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM owners WHERE email=%s",
            (email,)
        )

        owner = cur.fetchone()

        cur.close()

        if owner:

            if check_password_hash(owner["password"], password):

                flash("Login Successful!", "success")

                return redirect(url_for("owner_dashboard"))

        flash("Invalid Email or Password!", "danger")

        return redirect(url_for("owner_login"))

    return render_template("owner_login.html")


# ==========================
# OWNER REGISTER
# ==========================

@app.route("/owner-register", methods=["GET", "POST"])
def owner_register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        city = request.form["city"]
        address = request.form["address"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        hashed_password = generate_password_hash(password)

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("owner_register"))

        # Connect to database
        cur = mysql.connection.cursor()

        # Check if email already exists
        cur.execute(
            "SELECT * FROM owners WHERE email=%s",
            (email,)
        )

        owner = cur.fetchone()

        if owner:
            flash("Email already registered!", "warning")
            cur.close()
            return redirect(url_for("owner_register"))

        # Insert new owner
        cur.execute("""
            INSERT INTO owners
            (full_name, email, phone, city, address, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            fullname,
            email,
            mobile,
            city,
            address,
            hashed_password
        ))

        mysql.connection.commit()

        cur.close()

        flash("Registration Successful!", "success")

        return redirect(url_for("owner_login"))

    return render_template("owner_register.html")

# ==========================
# TENANT LOGIN
# ==========================

@app.route("/tenant-login")
def tenant_login():
    return render_template("tenant_login.html")


# ==========================
# TENANT REGISTER
# ==========================

@app.route("/tenant-register")
def tenant_register():
    return render_template("tenant_register.html")


# ==========================
# ADMIN LOGIN
# ==========================

@app.route("/admin-login")
def admin_login():
    return render_template("admin_login.html")


# ==========================
# OWNER DASHBOARD
# ==========================

@app.route("/owner-dashboard")
def owner_dashboard():
    return render_template("owner_dashboard.html")


  
# ==========================
# ADD PROPERTY PAGE
# ==========================

@app.route("/add-property")
def add_property():
    return render_template("add_property.html")


# ==========================
# DATABASE TEST
# ==========================

@app.route("/test-db")
def test_db():

    try:

        cur = mysql.connection.cursor()

        cur.execute("SELECT DATABASE();")

        database = cur.fetchone()

        cur.close()

        return f"Connected Successfully! Database: {database}"

    except Exception as e:

        return f"Error: {e}"


# ==========================
# RUN APPLICATION
# ==========================

if __name__ == "__main__":
    app.run(debug=True)