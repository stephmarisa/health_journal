from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import user, report, symptom_bank

class Symptom:
    db_name = "healthJournalSchema"

    def __init__(self, data):
        self.id = data['id']
        self.am = data['am']
        self.pm = data['pm']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.report_id = data['report_id']
        self.symptom_bank_id = data['symptom_bank_id']
        # self.symptom_name = symptom_bank.SymptomBank.get_name_by_id(data['symptom_bank_id'])

    @classmethod
    def new_report_symptom(cls, data):
        query = "INSERT INTO daily_symptoms (am, pm, report_id, symptom_bank_id) VALUES (%(am)s, %(pm)s, %(report_id)s, %(symptom_bank_id)s);"
        new_symptom_id = connectToMySQL(cls.db_name).query_db(query, data)
        return new_symptom_id

    @classmethod
    def get_all_symptoms(cls):
        query = "SELECT * FROM symptom_bank;"
        results = connectToMySQL(cls.db_name).query_db(query)
        symptoms = []
        for row in results:
            symptoms.append(symptom_bank.SymptomBank(row))
        return symptoms

    # edit this
    @classmethod 
    def get_daily_symptoms_by_day(cls, data):
        query = "SELECT * FROM daily_symptoms WHERE report_id = %(report_id)s;" 
        results = connectToMySQL(cls.db_name).query_db(query, data)
        daily_symptoms = []
        for row in results:
            daily_symptoms.append(cls(row))
        return daily_symptoms
    
    @classmethod
    def update_daily_symptom(cls, data):
        query = "UPDATE daily_symptoms SET am = %(am)s, pm = %(pm)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    