from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app.models import post_model
from pprint import pprint


DATABASE = 'myclick'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts=[]
    
    def __repr__(self):
        return f'<User: {self.username}>'

    @staticmethod
    def validate_registration(form):
        is_valid= True
        if len(form['username'])<2:
            flash(' Username must be at least two characters', 'username')
            is_valid= False
        if len(form['first_name'])<3:
            flash('First name must be at least two characters', 'first_name')
            is_valid= False
        if len(form['last_name'])<3:
            flash('Last name must be at least two characters','last_name')
            is_valid= False
        if not EMAIL_REGEX.match(form['email']):
            flash ("Invalid email address!",'email')
            is_valid= False
        if len(form['password'])<8:
            flash('Password must be at least eight characters', 'password')
            is_valid=False
        else:
            if form['password'] != form['confirm_password']:
                flash('passwords must match', 'confirm_password')
                is_valid= False
        return is_valid
    @staticmethod
    def validate_update(form):
        is_valid= True
        if len(form['first_name'])<2:
            flash('First name must be at least two characters', 'first_name')
            is_valid= False
        if len(form['last_name'])<3:
            flash('Last name must be at least two characters','last_name')
            is_valid= False
        if not EMAIL_REGEX.match(form['email']):
            flash ("Invalid email address!",'email')
            is_valid= False
        return is_valid   
        
    @staticmethod
    def validate_login(form):
        is_valid= True
        if not EMAIL_REGEX.match(form['email']):
            flash ("Invalid email address!",'log_email')
            is_valid= False
        if len(form['password'])<8:
            flash('Password must be at least eight characters', 'log_password')
            is_valid=False
        return is_valid

    #find by email
    @classmethod
    def find_by_email(cls, data):   
        query = 'SELECT * FROM users WHERE email= %(email)s;'
        results =connectToMySQL(DATABASE).query_db(query, data)
        if len(results)>0:
            return User(results[0])
        return None

    # create a user
    @classmethod
    def save(cls, data):
        # dont need created_at or created_at
        query = 'INSERT INTO users (username, first_name, last_name, email, password) VALUES (%(username)s,%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        return user_id



    # find one user by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from users WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results)> 0:
            return User(results[0])
        return None


# neeeedd to review to make link work
    @classmethod
    def find_by_id_with_post(cls, data):
        query = 'SELECT * FROM users LEFT JOIN posts ON users.id = posts.user_id WHERE users.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        print('hello world')
        pprint(results)
        user = User(results[0])
        if results[0]['user_id']:
            for result in results:
                data = {
                    'id': result['id'],
                    'title': result['title'],
                    'description': result['description'],
                    'created_at': result['created_at'],
                    'updated_at': result['updated_at'],
                    'user_id': result['user_id'],
                    'user':user
                }
                user.posts.append(post_model.Post(data))
                # print (user.posts)
        return user

    # FIND AND UPDATE
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE users SET username = %(username)s,first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True