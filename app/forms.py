from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, FileField
from wtforms.validators import InputRequired, EqualTo

class SignUpForm(FlaskForm):

    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    state = StringField('State', validators=[InputRequired()])
    zipcode = IntegerField('Zip Code', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class AddArtForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    width = IntegerField('Width', validators=[InputRequired()])
    height = IntegerField('Height', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    price = IntegerField('Price', validators=[InputRequired()])
    submit = SubmitField('Add Artwork')

class UploadForm(FlaskForm):
    image = FileField('Image', validators=[InputRequired()])
    submit = SubmitField('Add Artwork')

class CopyPasteForm(FlaskForm):
    submit = SubmitField('Share Portfolio')