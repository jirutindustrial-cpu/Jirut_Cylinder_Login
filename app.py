import os

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "temporary-secret-key")


# =========================
# USERS / ROLES
# =========================

USERS = {
    "admin": {
        "password": generate_password_hash(
            os.environ.get("ADMIN_PASSWORD", "")
        ),
        "role": "admin"
    },

    "staff": {
        "password": generate_password_hash(
            os.environ.get("STAFF_PASSWORD", "")
        ),
        "role": "staff"
    },

    "customer": {
        "password": generate_password_hash(
            os.environ.get("CUSTOMER_PASSWORD", "")
        ),
        "role": "customer"
    }
}


# =========================
# CYLINDER DATA
# =========================

CYLINDER = {
    "cylinder_id": "CYL-000001",
    "serial_number": "WT12345",
    "owner": "Jirut Industrial Co., Ltd.",
    "gas_type": "Acetylene (C2H2)",
    "capacity": "40 L",
    "tare_weight": "47.8 kg",
    "valve_type": "QF15A3 / CGA300",
    "fusible_plug": "Installed",
    "last_test": "15 Jul 2026",
    "next_test": "15 Jul 2031",
    "inspection_result": "PASS",
    "status": "Available",
    "remark": "Demo data for interface design."
}


# =========================
# LOGIN
# =========================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = USERS.get(username)

        if (
            user
            and password
            and check_password_hash(user["password"], password)
        ):

            session["username"] = username
            session["role"] = user["role"]

            return redirect(url_for("cylinder_info"))

        flash("Username หรือ Password ไม่ถูกต้อง")

    return render_template("login.html")


# =========================
# CYLINDER INFORMATION
# =========================

@app.route("/cylinder")
def cylinder_info():

    if "username" not in session:
        return redirect(url_for("login"))

    role = session.get("role")

    cylinder = CYLINDER.copy()


    # ADMIN
    # เห็นข้อมูลทั้งหมด
    if role == "admin":
        pass


    # STAFF
    # ซ่อนชื่อเจ้าของ / ลูกค้า
    elif role == "staff":

        cylinder["owner"] = "Restricted"


    # CUSTOMER
    # เห็นเฉพาะข้อมูลพื้นฐาน
    elif role == "customer":

        cylinder["owner"] = "Restricted"

        cylinder["tare_weight"] = "-"
        cylinder["valve_type"] = "-"
        cylinder["fusible_plug"] = "-"

        cylinder["last_test"] = "-"
        cylinder["next_test"] = "-"
        cylinder["inspection_result"] = "-"

        cylinder["remark"] = "-"


    else:
        return redirect(url_for("logout"))


    return render_template(
        "cylinder.html",
        cylinder=cylinder,
        role=role
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)
