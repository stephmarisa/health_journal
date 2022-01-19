from flask_app import app
from flask import render_template, redirect, request, session, flash
# from flask_app.models import user, painting

# bcrypt = Bcrypt(app)

#pipenv install PyMySQL flask

@app.route('/')
def dashboard_page():
    return render_template("home.html")