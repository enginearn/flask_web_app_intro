from apps.app import db
from apps.auth.forms import SignUpForm
from apps.crud.models import User
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user

auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@auth.route('/')
def index() -> render_template:
    return render_template('auth/index.html')

@auth.route('/login')
def login() -> render_template:
    return render_template('auth/login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup() -> render_template:
    form = SignUpForm()
    if form.validate_on_submit():
        if User().is_duplicate(form.username.data, form.email.data):
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('auth.signup'))
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.add(user)
            db.session.commit()
            flash('You have successfully registered! You may now login.', 'success')
            login_user(user)
            next_ = request.args.get('next')
            if next_ is None or not next_.startswith('/'):
                next_ = url_for('crud.users')

            return redirect(next_)
    return render_template('auth/signup.html', form=form)
