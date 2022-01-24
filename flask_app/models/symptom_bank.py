from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import user, report, symptom

class SymptomBank:
    db_name = "healthJournalSchema"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

    @classmethod
    def add_symptom(cls, data):
        query = "INSERT INTO symptom_bank (name) VALUES (%(name)s);"
        new_symptom_in_bank = connectToMySQL(cls.db_name).query_db(query, data)
        return new_symptom_in_bank

