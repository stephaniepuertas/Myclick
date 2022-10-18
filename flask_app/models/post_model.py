from flask_app import flash
from pprint import pprint
# must import user now so you can use it 
from flask_app.models import user_model

from flask_app.config.mysqlconnection import connectToMySQL

DATABASE = 'myclick'


class Post:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # must add for the foreign key
        self.user_id= data['user_id']
        # user obtained by user id(join)
        self.user=data['user']
    
    def __repr__(self):
        return f'<Post: {self.title}>'
    
    @staticmethod
    def validate_post(form):
        is_valid = True
        if len(form['title']) < 2:
            flash('title must be at least two characters.', 'title')
            is_valid = False
        if len(form['description']) < 10:
            flash('description must be at least ten characters.', 'description')
            is_valid = False
        return is_valid
    

    # create a post
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO posts (title, description, user_id) VALUES (%(title)s, %(description)s,%(user_id)s);'
        post_id = connectToMySQL(DATABASE).query_db(query, data)
        return post_id

    # find all posts (no data needed)
    @classmethod
    def find_all(cls):
        query = 'SELECT * from posts;'
        results = connectToMySQL(DATABASE).query_db(query)
        posts = []
        for result in results:
            posts.append(Post(result))
        return posts
# necessary for join!!!!!!!
    # find all post with creator (no data needed)
    @classmethod
    def find_all_with_creator(cls):
        query = 'SELECT * from posts;'
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        posts = []
        for result in results:
            data={
                'id': result['user_id']
            }
            user= user_model.User.find_by_id(data)
            post_data= {
                'id': result['id'],
                'title': result['title'],
                'description': result['description'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'user_id': result['user_id'],
                'user': user
            }
            posts.append(Post(post_data))
        return posts
    # find one post by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from posts WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        post = Post(results[0])
        return post

# find one post by id with creator
    @classmethod
    def find_by_id_with_creator(cls, data):
        query = 'SELECT * from posts WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        data={
                'id': results[0]['user_id']
        }
        user= user_model.User.find_by_id(data)
        post_data= {
            'id': results[0]['id'],
            'title': results[0]['title'],
            'description': results[0]['description'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'user_id': results[0]['user_id'],
            'user': user
        }
        post = Post(post_data)
        return post

    # update one post by id
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE posts SET title = %(title)s, description = %(description)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one post by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM posts WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True