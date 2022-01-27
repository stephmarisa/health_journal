from flask_app import app
from flask import render_template, redirect, request, session, flash


@app.route('/test')
def test_page():
    return render_template("test.html")