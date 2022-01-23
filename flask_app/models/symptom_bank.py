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
