from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from bagel import manager
from bagel import db


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(128))
    resumes = db.relationship('Resume', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


CVQuestions = ['firstname', 'lastname', 'city', 'music', 'artist', 'food', 'animal', 'country', 'secret', 'hair',
               'breakfast']


class CVform(FlaskForm):
    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    music = StringField('Favorite music genre', validators=[DataRequired()])
    artist = StringField('Favorite actor/actress', validators=[DataRequired()])
    food = StringField('Favorite food', validators=[DataRequired()])
    animal = StringField('Favorite animal', validators=[DataRequired()])
    country = StringField('Dream country', validators=[DataRequired()])
    secret = StringField('Guilty pleasure', validators=[DataRequired()])
    hair = StringField('Hair color', validators=[DataRequired()])
    breakfast = StringField('What did you have for breakfast today?', validators=[DataRequired()])
    submit = SubmitField('submit form')


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    firstname = db.Column(db.String(140))
    lastname = db.Column(db.String(140))
    city = db.Column(db.String(140))
    music = db.Column(db.String(140))
    artist = db.Column(db.String(140))
    food = db.Column(db.String(140))
    animal = db.Column(db.String(140))
    country = db.Column(db.String(140))
    secret = db.Column(db.String(140))
    hair = db.Column(db.String(140))
    breakfast = db.Column(db.String(140))

    def set_fields(self, form: CVform):
        self.firstname = form.firstname.data
        self.lastname = form.lastname.data
        self.city = form.city.data
        self.music = form.music.data
        self.artist = form.artist.data
        self.food = form.food.data
        self.animal = form.animal.data
        self.country = form.country.data
        self.secret = form.secret.data
        self.hair = form.hair.data
        self.breakfast = form.breakfast.data

    def __repr__(self):
        return '<Resume {}>'.format(self.body)
