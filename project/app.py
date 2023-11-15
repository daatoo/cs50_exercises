import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify

from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
    # raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def inbox():
    """Show all recived messages"""
    user_id = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = usernameDB[0]["username"]
    messages = db.execute(
        "SELECT * FROM messages WHERE recipient = ?", username)
    return render_template("index.html", messages=messages)



@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    """message to someone"""
    if request.method == "GET":
        user_id = session["user_id"]
        senderDb = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        sender = senderDb[0]["username"]
        return render_template("compose.html", sender=sender)
    else:
        sender = request.form.get("sender")
        recipient = request.form.get("recipient")
        subject = request.form.get("subject")
        body = request.form.get("body")
        if not sender:
            return apology("Must Give sender")
        if not recipient:
            return apology("Must Give recipient")
        if not subject:
            return apology("Must Give subject")
        if not body:
            return apology("Must Give body")
        db.execute("INSERT INTO messages (sender, recipient, subject, body) VALUES (?, ?, ?, ?)", sender, recipient, subject, body)
        return redirect("/")
@app.route("/sent")
@login_required
def sent():
    """Show sent messages"""
    user_id = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = usernameDB[0]["username"]
    messages = db.execute("SELECT * FROM messages WHERE sender = ?", username)
    return render_template("index.html", messages = messages)
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")
@app.route("/message", methods=["GET", "POST"])
@login_required
def message():
    """view message details"""
    if request.method == "POST":
        message_id = request.form.get("message_id")
        message_detail = db.execute("SELECT * FROM messages WHERE id = ?", message_id)
        return render_template("message.html", message_detail = message_detail[0])
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm")
        if not username:
            return apology("Must Give Username")
        if not password:
            return apology("Must Give Password")
        if not confirmation:
            return apology("Must Give Confirmation")
        if password != confirmation:
            return apology("Passwords Do Not Match")
        hash = generate_password_hash(password)
        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Username already exist")
        session["user_id"] = new_user
        return redirect("/")
@app.route("/reply", methods=["POST"])
@login_required
def relpy():
    """reply the message on message detail view"""
    if request.method == "POST":
        message_id = request.form.get("message_id")
        messageDB = db.execute("SELECT * FROM messages WHERE id = ?", message_id)
        message_detail = messageDB[0]
        return render_template("reply.html", message_detail = message_detail)