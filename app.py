import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date,datetime
from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///todo.db")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """Redirect to login page"""
    return redirect("/login")
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("must provide username and password", 403)

        rows = db.execute("SELECT * FROM users WHERE user_name = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["pswword"], password):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/dashboard")

    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password:
            return apology("must provide username and password", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)

        hashed_password = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (user_name, pswword) VALUES (?, ?)", username, hashed_password)
        except:
            return apology("username already exists", 400)

        return redirect("/login")

    return render_template("register.html")

@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """Display dashboard with user tasks and plans"""
    user_id = session["user_id"]
    plans = db.execute("SELECT DISTINCT plan FROM tasks WHERE user_id = ? AND plan IS NOT NULL", user_id)

    plan_name = request.args.get("plan")
    tasks = []
    status=[]
    if plan_name:
        tasks = db.execute(
            "SELECT task, due_date, CASE WHEN due_date >= DATE('now') THEN 'active' ELSE 'not-active' END AS status "
            "FROM tasks WHERE user_id = ? AND plan = ? AND task is NOT NULL AND due_date IS NOT NULL", user_id, plan_name)
        due_date=db.execute("SELECT due_date FROM tasks WHERE user_id=? AND plan=?",user_id,plan_name)
        today=date.today()
        for Date in due_date:
            value=Date['due_date']
        if value is not None:
            value = datetime.strptime(value, "%Y-%m-%d").date()
            if value >= today:
                db.execute("UPDATE tasks SET status='active' WHERE user_id=? AND due_date = ? AND plan=?",user_id,value,plan_name)
            else:
               db.execute("UPDATE tasks SET status='not-active' WHERE user_id=? AND due_date=? AND plan=?",user_id,value,plan_name)


        status = db.execute("SELECT status FROM tasks WHERE user_id = ? AND plan = ?", user_id, plan_name)

    return render_template("dashboard.html", plans=plans, selected_plan=plan_name, tasks=tasks, status=status)

@app.route("/plan", methods=["POST"])
@login_required
def plan():
    """Update or add a plan for the current user"""
    user_id = session["user_id"]
    plan_name = request.form.get("plan")

    db.execute("INSERT INTO tasks (plan, user_id) VALUES (?, ?)", plan_name, user_id)
    return redirect("/dashboard")

@app.route("/info", methods=["GET", "POST"])
@login_required
def info():
    user_id = session["user_id"]
    plan_name = request.args.get("plan")
    plans = db.execute("SELECT plan FROM tasks WHERE user_id = ?", user_id)

    tasks = db.execute("SELECT task, due_date FROM tasks WHERE user_id = ? AND plan = ?", user_id, plan_name)

    if request.method == "POST":
        task = request.form.get("task")
        due_date = request.form.get("date")

        if task and due_date:
            db.execute("INSERT INTO tasks (user_id, plan, task, due_date) VALUES (?, ?, ?, ?)", user_id, plan_name, task, due_date)

    tasks = db.execute(
        "SELECT task, due_date, CASE WHEN due_date >= DATE('now') THEN 'active' ELSE 'not-active' END AS status "
        "FROM tasks WHERE user_id = ? AND plan = ? AND task IS NOT NULL AND due_date IS NOT NULL", user_id, plan_name
    )
    plans = db.execute("SELECT DISTINCT plan FROM tasks WHERE user_id = ?", user_id)
    return render_template("dashboard.html", tasks=tasks, selected_plan=plan_name, plans=plans)
@app.route("/Delete",methods=["POST"])
@login_required
def Delete():

    plan_name= request.form.get("plan_name")
    user_id=session["user_id"]
    tasks = db.execute(
        "SELECT task, due_date, CASE WHEN due_date >= DATE('now') THEN 'active' ELSE 'not-active' END AS status "
        "FROM tasks WHERE user_id = ? AND plan = ? AND task IS NOT NULL AND due_date IS NOT NULL", user_id, plan_name
    )
    plans=db.execute("SELECT DISTINCT plan FROM tasks WHERE user_id=? AND plan=?",user_id,plan_name)
    if  plan_name:
        print(plan_name)
        print(request.form['plan_name'])
        db.execute("DELETE FROM tasks WHERE user_id=? AND plan=?",user_id,plan_name)

    return redirect("/dashboard")
@app.route("/delete",methods=["POST"])
@login_required
def delete():
    user_id=session["user_id"]
    task_name=request.form.get("task_name")
    if task_name:
        db.execute("DELETE FROM tasks WHERE user_id=? AND task=?",user_id,task_name)
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/login")
