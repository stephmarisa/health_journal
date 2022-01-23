from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import symptom, user

class Report:
    db_name = "healthJournalSchema"

    def __init__(self, data):
        self.id = data['id']
        self.notes = data['notes']
        self.flagged = data['flagged']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.daily_symptoms = symptom.Symptom.get_daily_symptoms_by_day({'report_id': data['id']})

    def morning_average(self):
        total = 0
        for this_symptom in self.daily_symptoms:
            total += this_symptom.am 
        return total/(len(self.daily_symptoms))

    def night_average(self):
        total = 0
        for this_symptom in self.daily_symptoms:
            total+= this_symptom.pm
        return total/(len(self.daily_symptoms))
    
    def overall_average(self):
        overall = (self.morning_average() + self.night_average())/2
        return overall

    @classmethod
    def new(cls, data):
        # query = "INSERT INTO reports (notes, flagged, user_id) VALUES (%(notes)s, %(flagged)s, %(user_id)s);"
        query = "INSERT INTO reports (notes, user_id) VALUES (%(notes)s, %(user_id)s);"
        new_report_id = connectToMySQL(cls.db_name).query_db(query, data)
        return new_report_id


    # edit this query so report contains the day's symptoms
    @classmethod
    def get_all_reports_by_id(cls, data):
        query = "SELECT * FROM reports WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        reports = []
        for row in results:
            reports.append(cls(row))
        return reports