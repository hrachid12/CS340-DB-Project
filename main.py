from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


# Orders


@app.route("/orders")
def orders():
    return render_template("orders.html")

# Products


@app.route("/products")
def products():
    return render_template("products.html")

# Customers


@app.route("/customers")
def customers():
    return render_template("customers.html")

# Coupons


@app.route("/coupons")
def coupons():
    return render_template("coupons.html")


# Orders_Products Intersection Table

@app.route("/orders_products")
def orders_products():
    return render_template("orders_products.html")


if __name__ == '__main__':
    app.run(debug=True)
