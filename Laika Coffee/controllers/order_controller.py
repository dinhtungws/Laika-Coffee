from flask import Blueprint, render_template, request, session, redirect, url_for
from models import db, Order, Menu

order_blueprint = Blueprint('order', __name__)

@order_blueprint.route('/order/<int:menu_id>', methods=['POST'])
def place_order(menu_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    quantity = int(request.form['quantity'])
    note = request.form['note']
    menu_item = Menu.query.get(menu_id)
    if menu_item:
        order = Order(
            customer_id=session['user_id'],
            menu_id=menu_id,
            quantity=quantity,
            price=menu_item.price * quantity,
            note=note
        )
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('view_menu'))

@order_blueprint.route('/admin/orders')
def admin_orders():
    if 'user_role' in session and session['user_role'] == 'manager':
        orders = Order.query.all()
        return render_template('order.html', orders=orders)
    return redirect(url_for('view_menu'))
