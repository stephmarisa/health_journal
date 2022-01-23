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

    @classmethod
    def new(cls, data):
        # query = "INSERT INTO reports (notes, flagged, user_id) VALUES (%(notes)s, %(flagged)s, %(user_id)s);"
        query = "INSERT INTO reports (notes, user_id) VALUES (%(notes)s, %(user_id)s);"
        new_report_id = connectToMySQL(cls.db_name).query_db(query, data)
        return new_report_id