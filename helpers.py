
from flask import render_template


def apology(message, code=400):
    """Render an apology message to the  user."""

    return render_template("apology.html", message=message, code=code), code
