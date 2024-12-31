from flask import Blueprint, render_template, request, session, redirect, url_for
from models import db, Menu

menu_blueprint = Blueprint('menu', __name__)

@menu_blueprint.route('/menu')
def view_menu():
    products = Menu.query.all()
    return render_template('menu.html', products=products)

@menu_blueprint.route('/admin/menu', methods=['GET', 'POST'])
def admin_menu():
    if 'user_role' in session and session['user_role'] == 'manager':
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            price = float(request.form['price'])
            menu = Menu(name=name, description=description, price=price)
            db.session.add(menu)
            db.session.commit()
        products = Menu.query.all()
        return render_template('admin_menu.html', products=products)
    return redirect(url_for('view_menu'))
