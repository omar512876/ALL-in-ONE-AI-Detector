import os
import psycopg2
import psycopg2.extras
from flask import redirect, render_template, session
from functools import wraps

def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def query(sql, param="None", fetch=True):
    conn = get_connection()
    with conn:
        try:
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    if fetch and cur.description:
                        return cur.fetchall()
        finally:
            conn.close()

def apology(message, code=400):
    """Render an apology message to the  user."""

    return render_template("apology.html", message=message, code=code), code

