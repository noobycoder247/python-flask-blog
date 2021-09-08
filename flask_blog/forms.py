from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileAllowed,FileField
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_blog.models import User

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    mobile=StringField('Mobile',validators=[DataRequired(),Length(min=10,max=10)])
    password=PasswordField('password',validators=[DataRequired(),Length(min=8,max=50,)])
    confirm_password=PasswordField('Confirm_pass',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign up')


    def validate_mobile(self,mobile):
        user=User.query.filter_by(mobile=mobile.data).first()
        # print(type(mobile.data))
        # print(int(mobile.data))
        if user:
            raise ValidationError('Mobile Number already exist')
        try:
            if int(mobile.data):
                pass
        except ValueError:
            raise ValidationError('Only number allowed in this field')
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already in use')
    def validate_email(self,email):
        email_id=User.query.filter_by(email=email.data).first()
        if email_id:
            raise ValidationError('This email id is already in use')


class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(min=8,max=50,)])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    mobile=StringField('Mobile',validators=[DataRequired(),Length(min=10,max=10)])
    picture=FileField('Upload picture',validators=[FileAllowed(['png','jpg','jpeg'])])
    submit=SubmitField('Update')


    def validate_mobile(self,mobile):
        print(f'mobile data ==> {mobile.data} current ==> {current_user.mobile}')
        print(f'mobile data ==> {type(mobile.data)} current ==> {type(current_user.mobile)}')
        if int(mobile.data) != current_user.mobile:
            user=User.query.filter_by(mobile=mobile.data).first()
            if user:
                raise ValidationError('Mobile Number already exist')
            try:
                if int(mobile.data):
                    pass
            except ValueError:
                raise ValidationError('Only number allowed in this field')
    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already in use')
    def validate_email(self,email):
        if email.data != current_user.email:
            email_id=User.query.filter_by(email=email.data).first()
            if email_id:
                raise ValidationError('This email id is already in use')

class PostFrom(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    submit=SubmitField('Post')