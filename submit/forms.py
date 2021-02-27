from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from re import *
from flask_wtf.file import * 
from models import *

class RegisterUserForm(FlaskForm):
    '''register a new user'''

    email = StringField('Email', validators=[InputRequired(),Length(min=4,max=50)])
    first_name = StringField('First Name', validators=[InputRequired(),Length(min=4,max=50)])
    last_name = StringField('Last Name', validators=[InputRequired(),Length(min=4,max=50)])
    username = StringField('User Name', validators=[InputRequired(),Length(min=4,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    '''login'''

    username = StringField('User Name', validators=[InputRequired(),Length(min=4,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])    

class PostFeedbackForm(FlaskForm):
    '''submit feedback'''

    title = StringField('Title', validators=[InputRequired(),Length(max=100)])
    content = StringField('Content', validators=[InputRequired()])


class EditFeedbackForm(FlaskForm):
    '''edit feedback'''

    title = StringField('Title', validators=[InputRequired(),Length(max=100)])
    content = StringField('Content', validators=[InputRequired()])



