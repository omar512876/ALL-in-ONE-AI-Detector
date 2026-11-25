import os
from dotenv import load_dotenv

from flask import Flask, flash, render_template, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from helpers import query, login_required, apology
from detectors.perplexity import Perplexity
from detectors.bert_classifier import DistilBertDetector

# reads .env and loads it into your program's environment variables.
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"] # add secret key to env


app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

DETECTORS = [Perplexity(), DistilBertDetector()]
MAX_CHARS = 5000



@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # variables
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        pass_conf = request.form.get("confirmation")

        # verify input (blanck and paswoord match)
        if not name or not email or not password or not pass_conf:
            return apology("please fill all the boxes")
        if not password == pass_conf:
            return apology("password dosent match")

        # verify email with RE
        # TODO 

        # add the user to the db
        try:
            hash = generate_password_hash(password, method='scrypt', salt_length=16)
            query("INSERT into teatchers (email, username, hash) VALUES (?, ?, ?)", email, name, hash)
        except ValueError:
            # verify "a duplicate name error raised "
            return apology("the name already existe")
        flash(f"Successfully registerd !")
        return redirect("/login")

    # the user reatch by git
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
                
        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for email
        rows = query(
            "SELECT * FROM teatchers WHERE email = ?", request.form.get("email")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash(f"Success !")
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
    flash(f"Success !")
    return redirect("/")



@app.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    if request.method == "POST":
        # get and check user input
        input_text = (request.form.get("input_text") or "").strip()
        if not input_text:
            return apology("please provide a text first")
        if len(input_text) > MAX_CHARS:
            return apology(f"Maximum characters allowed is {MAX_CHARS}")

        # analyzing process
        results = []
        for detector in DETECTORS:
            results.append(detector.safe_analyze(input_text))

        return render_template("results.html", text=input_text, results=results)

    return render_template("analyze.html")
