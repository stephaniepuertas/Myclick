from flask_app import app

# Remember to import controllers
from flask_app.controllers import post_controller, user_controller

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
