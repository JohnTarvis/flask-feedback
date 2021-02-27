from flask_sqlalchemy import *
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User'''

    __tablename__ = "users"

    username = db.Column(db.String(20), unique = True, primary_key = True)
    password = db.Column(db.Text)
    email = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    feedback = db.relationship('Feedback', backref='User')

    # start_register
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (un\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name = first_name, last_name = last_name)
    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
    # end_authenticate    

class Feedback(db.Model):
    '''feedback'''

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, unique = True, primary_key = True, autoincrement=True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.Text, nullable = False)

    username = db.Column('username', db.Text, db.ForeignKey('users.username'))

    #user = db.relationship("User", backref= "feedback", cascade="all, delete-orphan")    


