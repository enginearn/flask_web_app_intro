from flask import Blueprint, render_template, request, redirect, url_for, flash
from apps.app import db
from apps.crud.models import User
from apps.crud.forms import UserForm
from flask_login import login_required

crud = Blueprint(
    'crud',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@crud.route('/')
def index() -> render_template:
    return render_template('crud/index.html')

@crud.route('/sql')
def sql() -> render_template:
    db.session.query(User).all()
    return 'Check the console'
    # return redirect(url_for('crud.index'))

@login_required
@crud.route('/users')
def users() -> render_template:
    users = User.query.all()
    return render_template('crud/users.html', users=users)

@login_required
@crud.route('/users/new', methods=['GET', 'POST'])
def create_user() -> render_template:
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )

        db.session.add(user)
        db.session.commit()

        flash('User created successfully', 'success')

        return redirect(url_for('crud.users'))
    return render_template('crud/create.html', form=form)

@login_required
@crud.route('/users/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id: int) -> render_template:
    form = UserForm()
    user = User.query.filter_by(id=user_id).first()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        flash('User updated successfully', 'success')

        return redirect(url_for('crud.users'))
    return render_template('crud/edit.html', user=user, form=form)

@login_required
@crud.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id: int) -> render_template:
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()

    flash('User deleted successfully', 'success')

    return redirect(url_for('crud.users'))

