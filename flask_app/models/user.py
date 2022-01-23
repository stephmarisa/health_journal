from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name = "healthJournalSchema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    def full_name(self):
        return self.first_name + " " + self.last_name
    
    @classmethod
    def create_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        new_user_id = connectToMySQL(cls.db_name).query_db(query, data)
        return new_user_id

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)==0:
            return False
        return cls(results[0])

    @staticmethod
    def validate_registration(data):
        is_valid = True
        users_with_email = User.get_by_email({'email': data['email']})
        if len(data['first_name']) ==0:
            flash("please input a first name", "register")
            is_valid = False
        if len(data['last_name']) ==0:
            flash("please input a last name", "register")
            is_valid = False
        if len(data['email']) ==0:
            flash("please input an email", "register")
        elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        elif users_with_email != False:
            flash("Email already exists", "register")
            is_valid = False
        if len(data['password']) ==0:
            flash("please input a password", "register")
            is_valid = False
        elif data['password'] != data['confirm_password']:
            flash("password must match confirmed password", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        if len(data['email']) ==0:
            flash("please input an email", "login")
            is_valid = False
        if len(data['password']) ==0:
            flash("please input a password", "login")
            is_valid = False
        return is_valid


