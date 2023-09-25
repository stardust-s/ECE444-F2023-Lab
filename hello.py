from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

from datetime import datetime
from hashlib import sha256


app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = sha256("ECE444".encode('utf-8')).hexdigest()

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/", methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        ## process name
        old_name = session.get('name')
        name = form.name.data
        if old_name is not None and old_name != name:
            flash("Looks like you have changed your name!")
        session['name'] = name

        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'))

@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name = name, current_time = datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', msg = repr(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', msg = repr(e)), 500