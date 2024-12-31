from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['user_role'] = user.role
            return redirect(url_for('view_menu'))
        return "Login failed"
    return render_template('login.html')

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@user_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
