from flask import Flask, render_template, url_for, request
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


# Orders


@app.route("/orders", methods=['GET', 'POST'])
def orders():

    # connect to database
    db_connection = connect_to_database()

    if request.method == 'POST':

        # Fetch data from the form
        orderDate = request.form['orderDate']
        numProducts = request.form['numberOfProducts']
        cost = request.form['totalCost']
        customerID = request.form['customerID']
        couponID = request.form['couponID']

        # connect to database
        db_connection = connect_to_database()

        # Create query string and execute
        query = 'INSERT INTO orders (order_date, num_products, total_cost, customer_id, coupon_id) VALUES (%s, %s, %s, %s, %s)'
        query_params = (orderDate, numProducts, cost, customerID, couponID)
        execute_query(db_connection, query, query_params)

    print('Fetching info from database')

    # Create query strings and execute to retrieve required data from database
    query = 'SELECT * FROM orders'
    result = execute_query(db_connection, query).fetchall()

    query = 'SELECT customer_id, fname, lname FROM customers'
    customerResult = execute_query(db_connection, query)

    query = 'SELECT coupon_id, promotion FROM coupons'
    couponResult = execute_query(db_connection, query)

    print(result)
    return render_template('orders.html', rows=result, customers=customerResult, coupons=couponResult)

# Products


@app.route("/products", methods=['GET', 'POST'])
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

@app.route("/orders_products", methods=['GET', 'POST'])
def orders_products():
    return render_template("orders_products.html")


# Coupons_Customers Intersection Table

@app.route("/customers_coupons")
def customers_coupons():
    return render_template("customers_coupons.html")


if __name__ == '__main__':
    app.run(debug=True)
