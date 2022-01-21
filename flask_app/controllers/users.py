from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, symptom, entry
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#pipenv install PyMySQL flask

@app.route('/')
def dashboard_page():
    return render_template("initial.html")

@app.route('/registering')
def register_transition():
    return render_template("register.html")

@app.route('/logging')
def login_transition():
    return render_template("login.html")

@app.route('/register', methods =['POST'])
def register():
    if not user.User.validate_registration(request.form):
        return redirect('/registering')
    
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    #create new user in database using user info that we create with the hashed pass
    user_info = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw,
    }
    new_user_id = user.User.create_user(user_info)
    # put the user id into a session
    session['user_id'] = new_user_id
    return redirect('/home')

@app.route('/login', methods = ['POST'])
def login():
    if not user.User.validate_login(request.form):
        return redirect('/logging')
    #check for pre-existing emails in database
    data = {
        'email': request.form['email']
    }
    user_from_db = user.User.get_by_email(data)

    if not user_from_db:
        flash("Invalid email or password", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):
        return redirect('/')
    session['user_id'] = user_from_db.id
    return redirect("/home")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/home')
def home():
    return render_template("home.html")

