# messaging app
#### Video Demo:  https://www.youtube.com/watch?v=mmxNiEhLLNA
#### Description:
## CS50
>This was my final project for conclude the CS50 Introduction to Computer Sciense course.

>CS, python, flask, flask web framework, web development, CS50

## Explaining the project and the database
This is simple messaging app where you can create your account with username and password.
In compose page you can send message with username, and reciever can see this message in his/her inbox page. he/she also can relpy on your message.

### Sqlachemy and sqlite3:
For all of this I use database where I create two table. One for users and one for messages. Tere are 3 fields in users table: id, username and hash password. In messages table: id, sender, recipient, subject, body and timestamp.

### Register, Login and etc.. and validations.
I made several route path for: compose, sent, login, logout, message, register and reply. For each route, I also create html templates where I am using jinja to get data from backend.
In a route of main page(index) I am taking all messages from database which recipient is logined username.
```python
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


```

In compose I am making form to send message. I take sender and recipient usernames, subject, timestamp and body with post method.
```python
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


```
In a sent roude I render template where is sended messages.
```python
@app.route("/sent")
@login_required
def sent():
    """Show sent messages"""
    user_id = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = usernameDB[0]["username"]
    messages = db.execute("SELECT * FROM messages WHERE sender = ?", username)
    return render_template("index.html", messages = messages)

```

IN a message route I take detailed info about message and display with message.html.
```python
@app.route("/message", methods=["GET", "POST"])
@login_required
def message():
    """view message details"""
    if request.method == "POST":
        message_id = request.form.get("message_id")
        message_detail = db.execute("SELECT * FROM messages WHERE id = ?", message_id)
        return render_template("message.html", message_detail = message_detail[0])
```
In a relpy I am making form to reply message.
```python
@app.route("/reply", methods=["POST"])
@login_required
def relpy():
    """reply the message on message detail view"""
    if request.method == "POST":
        message_id = request.form.get("message_id")
        messageDB = db.execute("SELECT * FROM messages WHERE id = ?", message_id)
        message_detail = messageDB[0]
        return render_template("reply.html", message_detail = message_detail)
```
All of form have validation in both sides(front and back). so I anybody changes input type in inspect, I can reject this submit from beckend:)

### Template
For front end I am using week 9 finance templates. I just cange few things.


## About CS50
CS50 is a openware course from Havard University and taught by David J. Malan

Introduction to the intellectual enterprises of computer science and the art of programming. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, and software engineering. Languages include C, Python, and SQL plus students’ choice of: HTML, CSS, and JavaScript (for web development).

Thank you for all CS50.

- Where I get CS50 course?
https://cs50.harvard.edu/x/2020/