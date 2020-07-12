from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class ContactForm(FlaskForm):
    charityName = StringField('Name', [DataRequired()])
    charityEmail = StringField('Email', [DataRequired()])
    category = StringField('Category', [DataRequired()])
    tagLine = StringField('Tagline', [DataRequired()])
    mission = StringField('Mission', [DataRequired()])
    charityWebsite = StringField('Charity Website', [DataRequired()])
    submit = SubmitField('Submit')