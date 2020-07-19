from flask import Flask, render_template, url_for, redirect, request
from form import ContactForm
import os
from queryFunctions import register_nonProfit, GetNextId

application = Flask(__name__)

# methods=['GET', 'POST']
@application.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        newId = GetNextId("CharityInfo")
        print(form.charityName.data)
        print(form.charityEmail.data)
        print(form.category.data)
        print(form.tagLine.data)
        print(form.mission.data)
        print(form.charityWebsite.data)
        register_nonProfit(newId, str(form.charityName.data), str(form.charityEmail.data), str(form.category.data), str(form.tagLine.data), str(form.mission.data), str(form.charityWebsite.data))
        submission_successful = True
        return redirect(url_for('index'))
    return render_template('home.html', form=form)



SECRET_KEY = os.urandom(32)
application.config['SECRET_KEY'] = SECRET_KEY

if __name__ == '__main__':
    application.run(debug=True)

