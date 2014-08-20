import os
from flask import Flask, render_template, redirect
from flask.ext.mail import Mail, Message
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['DEFAULT_MAIL_SUBJECT'] = '[Politburo Voting Results]'
app.config['DEFAULT_MAIL_SENDER'] = 'Admin <admin@example.com>'
app.config['SECRET_KEY'] = 'random_string'
app.config['DEFAULT_ADMIN'] = 'Admin <admin@example.com>'

mail = Mail(app)


class PolitburoForm(Form):
    name = StringField('Who is your favorite member of the Politburo circa 1980?')
    submit = SubmitField('Submit')


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['DEFAULT_MAIL_SUBJECT'] + ' ' + subject,
        sender=app.config['DEFAULT_MAIL_SENDER'], recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


@app.route('/', methods=('GET', 'POST'))
def submit():
    form = PolitburoForm()
    if form.validate_on_submit():
        name = form.name.data
        send_email(app.config['DEFAULT_ADMIN'], 'Button clicked', 'mail/favorite', name=name)
        return redirect('/')
    return render_template('index.html', form=form)

if __name__ == '__main__':
    manager.run()