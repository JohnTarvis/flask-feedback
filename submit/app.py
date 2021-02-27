from typing import AsyncGenerator
from flask import *
from flask_debugtoolbar import *
from models import *
from forms import *
from werkzeug.utils import *

from sqlalchemy.exc import *

import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
toolbar = DebugToolbarExtension(app)
app.debug = True

db.app=(app)
db.init_app(app)
db.create_all()

connect_db(app)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

@app.route('/')
def home():
    return redirect('/register')

'''
============================================================================================USERS
'''

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        try:
            db.session.commit() 
        except:
            form.username.errors.append('Username Taken.  Please pick another.')
            return render_template('/users/register.html',form=form)
        return redirect('/secret')
    else:
        return render_template('/users/register.html',form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        # authenticate will return a user or False
        user = User.authenticate(name, pwd)
        if user:
            session["user_username"] = user.username  # keep logged in
            return redirect(f"/user/{user.username}")
        else:
            form.username.errors = ["Bad name/password"]
    return render_template("/users/login.html", form=form)
# end-login    


@app.route("/users/<username>")
def user_details(username):
    """Example hidden page for logged-in users only."""
    viewing_self = False
    feedback = Feedback.query.filter_by(username=username)
    if "user_username" in session:
        if session['user_username'] == username:
            viewing_self = True       
    user = User.query.get_or_404(username) 
    return render_template("/users/details.html", user = user, viewing_self = viewing_self, feedback=feedback)

@app.route("/users/<username>/delete")
def user_delete(username):
    """Example hidden page for logged-in users only."""
    if "user_username" in session and session['user_username'] == username:
        user = User.query.get_or_404(username) 
        db.session.delete(user)
        db.session.commit()
    return redirect('/login')

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""
    session.pop("user_username")
    return redirect("/")

'''
============================================================================================FEEDBACK
'''

@app.route('/users/<username>/feedback/add',methods=["GET", "POST"])
def add_feedback(username):
    '''add feedback'''
    form = PostFeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # authenticate will return a user or False
        if session["user_username"] == username:
            feedback = Feedback(title=title,content=content,username=username)
            db.session.add(feedback)
            db.session.commit()
    return render_template("/feedback/add-feedback.html", form=form)

@app.route('/feedback/<int:feedback_id>/update',methods=['GET','POST'])
def edit_feedback(feedback_id):
    '''edit feedback'''
    form = EditFeedbackForm()
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username
    if 'user_username' in session and session["user_username"] == username:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title,content=content,username=username)
            db.session.add(feedback)
            db.session.commit()
        return render_template("/feedback/edit-feedback.html", form=form, username=username)    
    else:
        return redirect('/')

@app.route('/feedback/<int:feedback_id>/delete')
def delete_feedback(feedback_id):
    '''delete feedback'''
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username
    if 'user_username' in session and session["user_username"] == username:
        db.session.delete(feedback)
        db.session.commit()   

def big_print(message, description = ''):
    print(f''' 

    >>>>>>>>>>>>>>>>{description}<<<<<<<<<<<<<<<<<<<<<

    //////////////////////////////////////////////////
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
                      {message}
    
    //////////////////////////////////////////////////
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
    ''')



# @app.route("/secret")
# def secret():
#     """Example hidden page for logged-in users only."""

#     if "user_username" not in session:
#         flash("You must be logged in to view!")
#         return redirect("/")

#     else:
#         return render_template("/users/secret.html")

# @app.route("/user/<username>")
# def user_details(username):
#     """Example hidden page for logged-in users only."""

#     if "user_username" not in session:
#         flash("You must be logged in to view!")
#         return redirect("/")

#         # alternatively, can return HTTP Unauthorized status:
#         #
#         # from werkzeug.exceptions import Unauthorized
#         # raise Unauthorized()

#     else:
#         user = User.query.get_or_404(username) #db.session.query(username=username).first()
#         return render_template("/users/details.html", user=user)