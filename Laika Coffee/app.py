from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "laika_coffee_secret_key"

# Data
products = [
    {"id": 1, "name": "Cà phê đen", "description": "Cà phê nguyên chất", "price": 20000, "image": "static/images/capheden.jpg"},
    {"id": 2, "name": "Trà sữa trân châu đường đen", "description": "Trà sữa thơm ngon", "price": 30000, "image": "static/images/trasuatranchau.jpg"},
]

orders = []
cart = []

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Menu Page
@app.route("/menu")
def menu():
    return render_template("menu.html", products=products)

# Add to Cart
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        cart.append({"id": product["id"], "name": product["name"], "price": product["price"], "quantity": 1})
    return redirect(url_for("menu"))

# View Cart
@app.route("/cart")
def view_cart():
    total_price = sum(item["price"] * item["quantity"] for item in cart)
    return render_template("cart.html", cart=cart, total_price=total_price)

# Place Order
@app.route("/place_order", methods=["POST"])
def place_order():
    if cart:
        new_order = {
            "id": len(orders) + 1,
            "customer_name": request.form["customer_name"],
            "items": cart.copy(),
            "note": request.form.get("note", ""),
            "total_price": sum(item["price"] * item["quantity"] for item in cart),
            "status": "Đang chờ xử lý"
        }
        orders.append(new_order)
        cart.clear()
    return redirect(url_for("home"))

# Admin: Manage Menu
@app.route("/admin/menu", methods=["GET", "POST"])
def manage_menu():
    global products
    if request.method == "POST":
        new_item = {
            "id": len(products) + 1,
            "name": request.form["name"],
            "description": request.form["description"],
            "price": int(request.form["price"]),
            "image": request.form["image"]
        }
        products.append(new_item)
    return render_template("manage_menu.html", products=products)

@app.route("/admin/menu/delete/<int:product_id>")
def delete_menu_item(product_id):
    global products
    products = [p for p in products if p["id"] != product_id]
    return redirect(url_for("manage_menu"))

# Admin: Manage Orders
@app.route("/admin/orders")
def manage_orders():
    return render_template("manage_orders.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True)
