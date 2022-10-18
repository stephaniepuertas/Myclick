from pprint import pprint
from flask_app import app, render_template, redirect, request, session
from flask_app.models.post_model import Post
from flask_app.models.user_model import User

# # main profile page
# @app.get('/profile')
# def profile():
#     return render_template('profile.html')


# display all posts
@app.get('/posts')
def all_posts():
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data={
        'id': session['user_id']
    }
    user= User.find_by_id(data)
    # you use the find all creator to get the information of the creator
    posts = Post.find_all_with_creator()
    pprint(posts)
    return render_template('dashboard.html', posts = posts, user=user)

# display one post by id
@app.get('/posts/<int:post_id>')
def one_post(post_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': post_id
    }
    user_data = {
        'id': session['user_id']
    }
    user = User.find_by_id(user_data)
    post = Post.find_by_id_with_creator(data)
    print(f'**** FOUND - POST ID: {post.id} ****')
    return render_template('one_post.html', post = post, user = user)

# display form to create a post
@app.get('/posts/new')
def new_post():
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    return render_template('new_post.html')

# process form and create a post
@app.post('/posts')
def create_post():
    if not Post.validate_post(request.form):
        return redirect('/posts/new')
    post_id = Post.save(request.form)
    print(f'**** CREATED - POST ID: {post_id} ****')
    return redirect('/posts')

# display form to edit a post by id
@app.get('/posts/<int:post_id>/edit')
def edit_post(post_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': post_id
    }
    post = Post.find_by_id_with_creator(data)
    print(f'**** FOUND - POST ID: {post.id} ****')
    return render_template('edit_post.html', post = post)

# process form and update a post by id
@app.post('/posts/<int:post_id>/update')
def update_post(post_id):
    if not Post.validate_post(request.form):
        return redirect(f'/posts/{post_id}/edit')
    Post.find_by_id_and_update(request.form)
    print(f'**** UPDATED - POST ID: {post_id} ****')
    return redirect(f'/posts/{post_id}')

# delete one post by id
@app.get('/posts/<int:post_id>/delete')
def delete_post(post_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': post_id
    }
    Post.find_by_id_and_delete(data)
    print(f'**** DELETED - POST ID: {post_id} ****')
    return redirect('/posts')
