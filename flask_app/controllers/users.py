from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import report, symptom, user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#pipenv install PyMySQL flask

@app.route('/')
def dashboard_page():
    return render_template("initial.html")

# Create User
@app.route('/registering')
def register_transition():
    return render_template("register.html")

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
    print(session['user_id'],"hiiiii")
    return redirect('/home')

#Log in User 
@app.route('/logging')
def login_transition():
    return render_template("login.html")

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
    print(session['user_id'], 'hiiiii')
    return redirect("/home")

# Logout User
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Home report dashboard
@app.route('/home')
def home():
    data = {'user_id': session['user_id']}
    reports_list = report.Report.get_all_reports_by_id(data)
    # reversed_reports_list = reverse_list(reports_list)
    return render_template("home.html", reports_list = reports_list)

# def reverse_list(some_list):
#     reversed_list = []
#     for item in some_list:
#         some_list.insert(0,item)
#     return reversed_list

@app.route('/trends')
def display_trends():
    # data = {
    #     "2022-01-22": 7.5,
    #     "2022-01-23": 1.0,
    #     "2022-01-24": 5.0
    # }

    # get list of reports
    data = {'user_id': session['user_id']}
    reports_list = report.Report.get_all_reports_by_id(data)

    #  make dictionary for overall data, morning data, and evening data
    overall_dataset = {}
    morning_dataset = {}
    evening_dataset = {}
    for this_report in reports_list:
        dateTimeObj = this_report.created_at
        timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M")
        # (%H:%M)
        overall_dataset[timestampStr] = this_report.overall_average()
        morning_dataset[timestampStr] = this_report.morning_average()
        evening_dataset[timestampStr] = this_report.night_average()
    
    # dataset 1:overview report.created_at: report.overall_average
    x1labels, y1labels, y2labels, y3labels  = list(overall_dataset.keys()), list(overall_dataset.values()), list(morning_dataset.values()), list(evening_dataset.values())

    return render_template("trends.html", x1labels = x1labels, y1labels = y1labels, y2labels = y2labels, y3labels = y3labels)
