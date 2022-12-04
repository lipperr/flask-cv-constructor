from flask import render_template, redirect, url_for, request, flash, session, send_file
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from bagel.models import *
from bagel import app, db
import pdfkit


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('base.html')


@app.route('/cvform', methods=['GET', 'POST'])
def cvform():
    form = CVform()
    if not current_user.is_authenticated:
        flash('Please log in first!')
        return redirect(url_for('hello_world'))

    if form.validate_on_submit():
        resume = Resume(user_id=current_user.id)
        resume.set_fields(form)
        db.session.add(resume)
        db.session.commit()
        return redirect(url_for('hello_world'))

    return render_template('cvform.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if request.method == 'POST':
        if form.username and form.password:
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('hello_world'))
            else:
                flash('username or password is not correct')
        else:
            flash('Please fill username and password fields')

        if form.validate_on_submit():
            flash('username requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
            return redirect(url_for('hello_world'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pwd = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hash_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login_page'))
    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response


@app.route('/user')
def user():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first_or_404()
        resumes = Resume.query.filter_by(author=user).all()
        return render_template('user.html', user=user, resumes=resumes, topics=CVQuestions)
    else:
        flash('Please log in to see your personal page!')
        return redirect(url_for('hello_world'))


@app.route('/download/<file_id>')
def download(file_id):
    resume = Resume.query.get(file_id)
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    text = render_template('cv.html', resume=resume, topics=CVQuestions)
    pdfkit.from_string(text, output_path='/Users/annal/cv_constructor/flcvcon/out.pdf', configuration=config)
    try:
        exact_path = '/Users/annal/cv_constructor/flcvcon/out.pdf'
        return send_file(exact_path, as_attachment=True)
    except Exception as e:
        return str(e)
