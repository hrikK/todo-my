from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import EqualTo, Length, DataRequired, Email, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import user


class SignUpForm(FlaskForm):

    def validate_username(self, username_to_check):
        username_check = user.query.filter_by(username=username_to_check.data).first()
        if username_check:
            raise ValidationError("This is username is already being used!")
    def validate_email_address(self, email_to_check):
        email_check = user.query.filter_by(email=email_to_check.data).first()
        if email_check:
            raise ValidationError("This is already registered!")
    def validate_phone_number(self, ph_to_check):
        ph_check = user.query.filter_by(ph_no=ph_to_check.data).first()
        if ph_check:
            raise ValidationError("This number is already being used!")


    full_name = StringField(label="Full Name", validators=[Length(min=3), DataRequired()])
    username = StringField(label="Username", validators=[Length(min=2, max=8), DataRequired()])
    email_address = StringField(label="Email", validators=[Email(), DataRequired()])
    phone_number = IntegerField(label="Phone Number", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=8), DataRequired()])
    confirm_pass = PasswordField(label="Confirm Password", validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label="Sign-Up")

class SignInForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    email_address = StringField(label="Email", validators=[Email(), DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign-In")
class TodoForm(FlaskForm):
    text = StringField(validators=[Length(max=200)])
    add_todo = SubmitField(label="+")
