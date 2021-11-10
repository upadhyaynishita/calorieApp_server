from datetime import date
from re import sub
from flask import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from apps import App


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        app_object = App()
        mongo = app_object.mongo

        temp = mongo.db.user.find_one({'email': email.data}, {'email', 'pwd'})
        if temp:
            raise ValidationError('Email already exists!')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Food:
    result = []
    def get_food(self):
        app = App()
        mongo = app.mongo

        f = open('food_data/calories.csv', 'r', encoding = "ISO-8859-1")
        l = f.readlines()

        for i in range(1, len(l)):
            l[i] = l[i][1:len(l[i]) - 2]

        for i in range(1, len(l)):
            temp = l[i].split(",")
            mongo.db.food.insert({'food': temp[0], 'calories': temp[1]})


        cursor = mongo.db.food.find()
        get_docs = []
        for record in cursor:
            get_docs.append(record)

        self.result = []
        temp = ""
        for i in get_docs:
            temp = i['food'] + ' (' + i['calories'] + ')'
            self.result.append((temp, temp))
        return self.result
    
class CalorieForm(FlaskForm):
    burnout = StringField('Burn Out', validators=[DataRequired()])
    submit = SubmitField('Save')
    f = Food()
    result = f.get_food()
    food = SelectField('Select Food', choices=result)



class UserProfileForm(FlaskForm):
    weight = StringField(
        'Weight', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    height = StringField(
        'Height', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    goal = StringField(
        'Goal', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    target_weight = StringField(
        'Target Weight', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    submit = SubmitField('Save Profile')


class HistoryForm(FlaskForm):
    app = App()
    mongo = app.mongo
    date = DateField()
    submit = SubmitField('Fetch')


class EnrollForm(FlaskForm):
    app = App()
    mongo = app.mongo
    submit = SubmitField('Enroll')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')
