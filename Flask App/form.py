from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, email_validator, ValidationError
from queryFunctions import query_if_already_exists


#Using WhatTheForms
class ContactForm(FlaskForm):
    charityName = StringField('Name', [DataRequired()])
    charityEmail = StringField('Email', [DataRequired(), Email()])
    category = StringField('Category', [DataRequired()])
    tagLine = StringField('Tagline')
    mission = TextAreaField('Mission', [DataRequired()])
    charityWebsite = StringField('Charity Website')

#custom validation, checks if a name is already in use
    def validate_charityName(form, field):
        print(field.data)
        result = query_if_already_exists(field.data)
        if result is True:
            raise ValidationError('There is already a charity by this name, please enter a different name.')