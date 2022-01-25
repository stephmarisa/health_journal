from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import report, symptom, user
from flask_bcrypt import Bcrypt

#Display
# @app.route('/show/entry/<int:entry_id>')
# def show_entry(entry_id):
#     return render_template('display_report.html')


# why does /create/report not load the css?
#Create New report/Report
@app.route('/create/report')
def create_report():
    if 'user_id' not in session:
        return redirect('/logout')
    this_user = user.User.get_by_id({'id': session['user_id']})
    # get list of symptoms?
    symptoms_list = symptom.Symptom.get_all_symptoms()
    return render_template("create_report.html", this_user = this_user, symptoms_list = symptoms_list)

@app.route('/newReport', methods = ['POST'])
def new_report():
    # add report validations here to require every symptom to be filled out
    report_info = {
        'notes': request.form['notes'],
        # 'flagged': request.form['flagged'],
        'user_id': session['user_id']
    }
    new_report_id = report.Report.new(report_info)

    #create symptoms here
    symptoms_list = symptom.Symptom.get_all_symptoms()
    for this_symptom in symptoms_list:
        am_name = "am-" + str(this_symptom.id)
        pm_name = "pm-" + str(this_symptom.id)
        # create daily symptom
        symptom_info = {
            'am': request.form[am_name],
            'pm': request.form[pm_name],
            'report_id': new_report_id,
            'symptom_bank_id': this_symptom.id
        }
        new_symptom_id = symptom.Symptom.new_report_symptom(symptom_info)

    return redirect('/home')

# Edit Report
@app.route('/edit/<int:report_id>')
def edit_report(report_id):
    symptoms_list = symptom.Symptom.get_all_symptoms()
    this_report = report.Report.get_by_id({'report_id': report_id})
    return render_template("update_report.html", this_report = this_report, symptoms_list = symptoms_list)

@app.route('/update/<int:report_id>', methods=["POST"])
def update_report(report_id):
    report_info = {
        'id': report_id,
        'notes': request.form['notes'],
        # 'flagged': request.form['flagged'],
        'user_id': session['user_id']
    }
    updated_report = report.Report.update_report(report_info)
    this_report = report.Report.get_by_id({'report_id': report_id})

    symptoms_list = this_report.daily_symptoms
    for this_symptom in symptoms_list:
        print("hiiiiiiii symptom id", this_symptom.id)
        am_name = "am-" + str(this_symptom.id)
        pm_name = "pm-" + str(this_symptom.id)
        # create daily symptom
        symptom_info = {
            'am': request.form[am_name],
            'pm': request.form[pm_name],
            'report_id': report_id,
            'symptom_bank_id': this_symptom.symptom_bank_id,
            'id': this_symptom.id
        }
        updated_daily_symptom = symptom.Symptom.update_daily_symptom(symptom_info)

    return redirect('/home')