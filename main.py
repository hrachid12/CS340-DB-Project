from flask import Flask, render_template, url_for, flash, redirect
from forms import OrderForm, ProductForm, OrderProductForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'bcfc1681028610b5892af746bfac0ba6'


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


# Orders


@app.route("/orders", methods=['GET', 'POST'])
def orders():
    form = OrderForm()
    if form.validate_on_submit():
        flash(f'Success! Database updated!', 'success')
        return redirect(url_for('orders'))
    return render_template("orders.html", form=form)

# Products


@app.route("/products", methods=['GET', 'POST'])
def products():
    form = ProductForm()
    if form.validate_on_submit():
        flash(f'Success! Database updated!', 'success')
        return redirect(url_for('products'))
    return render_template("products.html", form=form)

# Customers


@app.route("/customers")
def customers():
    return render_template("customers.html")

# Coupons


@app.route("/coupons")
def coupons():
    return render_template("coupons.html")


# Orders_Products Intersection Table

@app.route("/orders_products", methods=["GET", "POST"])
def orders_products():
    form = OrderProductForm()
    if form.validate_on_submit():
        flash(f'Success! Database updated!', 'success')
        return redirect(url_for('orders_products'))
    return render_template("orders_products.html", form=form)


# Coupons_Customers Intersection Table

@app.route("/customers_coupons")
def customers_coupons():
    return render_template("customers_coupons.html")


if __name__ == '__main__':
    app.run(debug=True)
