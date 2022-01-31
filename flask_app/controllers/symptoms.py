from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import report, symptom, user, symptom_bank
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/createSymptom')
def create_symptom():
    if 'user_id' not in session:
        return redirect('/logout')
    this_user = user.User.get_by_id({'id': session['user_id']})
    # get this report?
    return render_template("create_symptom.html", this_user = this_user)

@app.route('/newSymptom', methods = ['POST'])
def new_Symptom():
    symptom_info = {
        'name': request.form['name']
    }
    symptom_in_bank = symptom_bank.SymptomBank.add_symptom(symptom_info)
    return redirect('/create/report')

