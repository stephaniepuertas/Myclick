from flask_app import app, render_template, redirect, request, session, flash, bcrypt
from flask_app.models.user_model import User
from pprint import pprint

# redirect user to login/reg
@app.get('/')
def redirect_user():
    return redirect ('users/login_reg')

@app.get('/users/login_reg')
def login_reg():
    return render_template('login_reg.html')

@app.post ('/users/register')
def register_user():
    #check if form is valid
    if not User.validate_registration(request.form):
        return redirect('/users/login_reg')

    #if form is valid, check to see if they are registered
    found_user = User.find_by_email(request.form)
    if found_user:
        flash ('Email already in database, Please login.', 'email')
        return redirect ('/users/login_reg')

    #hash password(encrypt with bycrypt)
    hashed = bcrypt.generate_password_hash(request.form['password'])
    # print(hashed)
    data= {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':hashed
    }
    #register(save) the user
    user_id= User.save(data)

    #log the user in and save user's id in session
    session['user_id']= user_id
    return redirect('/posts')

@app.post('/users/login')
def login_users():
    #check if the form is valid
    if not User.validate_login(request.form):
        return redirect('/users/login_reg')

    #if the form is valid, check to see if they are registered
    found_user = User.find_by_email(request.form)
    if not found_user:
        flash('Email not found, please register.','log_email')
        return redirect('/users/login_reg')

    #if they did register, 
    # check if the password is correct
    if not bcrypt.check_password_hash(found_user.password, request.form['password']):
        flash('Invalid credentials. Please check your password.','log_password')
        return redirect('/users/login_reg')

    #if they password is correct, log them in
    session['user_id']=found_user.id
    return redirect('/posts')


@app.get('/users/logout')
def logout():
        session.clear()
        return redirect('/users/login_reg')


# obtain user with posts
# display one user by id
@app.get('/users/<int:user_id>/account')
def one_user(user_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': user_id
    }
    # need to use the correct methods to obtain the correct id with model!!!!!!!!!!!
    user = User.find_by_id_with_post(data)
    print(f'**** FOUND - USER ID: {user.id} ****')
    return render_template('one_user.html', user=user)


# EDIT USER INFO
@app.post('/users/<int:user_id>/update')
def update_user(user_id):
    if not User.validate_update(request.form):
        return redirect(f'/users/{user_id}/account')
    User.find_by_id_and_update(request.form)
    return redirect(f'/users/{user_id}/account')
