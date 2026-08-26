
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "CHANGE-THIS-SECRET-KEY"

USERS = {"jirut": generate_password_hash("1234")}

CYLINDER = {
    "cylinder_id":"CYL-000001",
    "serial_number":"WT12345",
    "owner":"Jirut Industrial Co., Ltd.",
    "gas_type":"Acetylene (C2H2)",
    "capacity":"40 L",
    "tare_weight":"47.8 kg",
    "valve_type":"QF15A3 / CGA300",
    "fusible_plug":"Installed",
    "last_test":"15 Jul 2026",
    "next_test":"15 Jul 2031",
    "inspection_result":"PASS",
    "status":"Available",
    "remark":"Demo data for interface design."
}

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username","").strip()
        p = request.form.get("password","")
        if u in USERS and check_password_hash(USERS[u], p):
            session["username"] = u
            return redirect(url_for("cylinder_info"))
        flash("Username หรือ Password ไม่ถูกต้อง")
    return render_template("login.html")

@app.route("/cylinder")
def cylinder_info():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("cylinder.html", cylinder=CYLINDER)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
