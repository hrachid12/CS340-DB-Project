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
    alerts = ()

    if request.method == 'POST':

        # Fetch data from the form
        orderDate = request.form['orderDate']
        numProducts = request.form['numberOfProducts']
        cost = request.form['totalCost']
        customerID = request.form['customerID']
        couponID = request.form['couponID']

        # If no coupon is selected
        if couponID == 'NULL':
            couponID = None

            # Create query string and execute command
            query = 'INSERT INTO orders (order_date, num_products, total_cost, customer_id, coupon_id) VALUES (%s, %s, %s, %s, %s)'
            data = (orderDate, numProducts, cost, customerID, couponID)
            execute_query(db_connection, query, data)
            alerts = ("Success! Database updated!", False)

        else:
            # The following query is to check if the selected coupon is valid for the selected customer
            query = 'SELECT customer_id, coupon_id FROM coupons_customers WHERE customer_id = %s AND coupon_id = %s'
            query_params = (customerID, couponID)
            result = execute_query(db_connection, query,
                                   query_params).fetchone()

            # Check result. If it is None, then an invalid coupon was selected
            if result is None:
                # If customer can't use the indicated coupon, check to see which coupons they can use
                query = """SELECT fname, lname, promotion FROM customers c
                        LEFT JOIN coupons_customers cc ON c.customer_id = cc.customer_id
                        LEFT JOIN coupons ON cc.coupon_id = coupons.coupon_id
                        WHERE c.customer_id = %s"""
                query_params = (customerID)
                checkAvailableCoupons = execute_query(
                    db_connection, query, query_params).fetchall()

                # Retrieve the cusomer's name
                customerName = checkAvailableCoupons[0][0] + \
                    ' ' + checkAvailableCoupons[0][1]

                # If customer does not have any promotions available, then the result will be of length 1
                # and None will be present where the promotion should be
                if len(checkAvailableCoupons) == 1 and checkAvailableCoupons[0][2] is None:
                    alerts = (
                        f"Error! Database not updated! {customerName} can not apply any coupon to their orders.", True)
                else:
                    # Retrieve all promotions that a customer can use, store it in correctCoupons
                    correctCoupons = ''
                    for result in checkAvailableCoupons:
                        correctCoupons += str(result[2])
                        correctCoupons += ', '
                    alerts = (
                        f"Error! Database not updated! {customerName} can only apply the following coupon(s) to their order: {correctCoupons}", True)

            # Valid coupon selected. Insert into database
            else:
                # Create query string and execute command
                query = 'INSERT INTO orders (order_date, num_products, total_cost, customer_id, coupon_id) VALUES (%s, %s, %s, %s, %s)'
                data = (orderDate, numProducts, cost, customerID, couponID)
                execute_query(db_connection, query, data)
                alerts = ("Success! Database updated!", False)

    print('Fetching info from database')

    # Create query strings and execute to retrieve required data from database
    query = 'SELECT * FROM orders'
    result = execute_query(db_connection, query).fetchall()

    query = 'SELECT customer_id, fname, lname FROM customers'
    customerResult = execute_query(db_connection, query).fetchall()

    query = 'SELECT coupon_id, promotion FROM coupons'
    couponResult = execute_query(db_connection, query).fetchall()

    return render_template('orders.html', rows=result, customers=customerResult, coupons=couponResult, alerts=alerts)

# Products


@app.route("/products", methods=['GET', 'POST'])
def products():
    db_connection = connect_to_database()
    alerts = ()

    if request.method == 'POST':

        # Fetch data from the form
        itemName = request.form['itemName']
        price = request.form['price']
        quantityAvailable = request.form['quantityAvailable']

        # Build query string and execute
        query = 'INSERT INTO products (item_name, price, quantity_available) VALUES (%s, %s, %s)'
        data = (itemName, price, quantityAvailable)
        execute_query(db_connection, query, data)
        alerts = ("Success! Database updated!", False)

    print('Fetching info from database')

    # Create query strings and execute to product table data
    query = 'SELECT * FROM products'
    result = execute_query(db_connection, query).fetchall()

    return render_template("products.html", rows=result, alerts=alerts)

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

    # Connect to database
    db_connection = connect_to_database()
    alerts = ()

    if request.method == "POST":

        # Fetch data from the form
        orderID = request.form['orderID']
        productID = request.form['productID']

        # Build query string and execute
        query = 'INSERT INTO orders_products (order_id, product_id) VALUES (%s, %s)'
        data = (orderID, productID)
        execute_query(db_connection, query, data)
        alerts = ("Success! Database updated!", False)

    # Build query selections for intersection table, order table, and product, table
    query = 'SELECT * FROM orders_products'
    result = execute_query(db_connection, query)

    query = 'SELECT order_id, fname, lname, order_date FROM orders LEFT JOIN customers ON orders.customer_id = customers.customer_id'
    orders = execute_query(db_connection, query)

    query = 'SELECT product_id, item_name FROM products'
    products = execute_query(db_connection, query)

    return render_template("orders_products.html", rows=result, orders=orders, products=products, alerts=alerts)


# Coupons_Customers Intersection Table

@app.route("/customers_coupons")
def customers_coupons():
    return render_template("customers_coupons.html")


# Update order page

@app.route("/orders/update", methods=['POST'])
def update_order():
    db_connection = connect_to_database()

    orderID = request.form["updateOrder"]

    # Build Select query to populate form
    query = """SELECT DISTINCT order_id, order_date, num_products, total_cost, fname, lname, c.customer_id, cc.coupon_id, promotion FROM orders
            LEFT JOIN customers c ON orders.customer_id = c.customer_id
            LEFT JOIN coupons_customers ON c.customer_id = coupons_customers.coupon_id
            LEFT JOIN coupons cc ON coupons_customers.coupon_id = cc.coupon_id
            WHERE order_id = %s"""
    data = [orderID]
    result = execute_query(db_connection, query, data).fetchone()
    print(result)

    # Get all customers except for one from initial query
    query = f'SELECT customer_id, fname, lname FROM customers WHERE NOT customer_id = {result[6]}'
    customerResult = execute_query(db_connection, query).fetchall()

    # Get all coupons except for one from initial query
    if result[7] is not None:
        query = f'SELECT coupon_id, promotion FROM coupons WHERE NOT coupon_id = {result[7]}'
        couponResult = execute_query(db_connection, query).fetchall()
    else:
        query = f'SELECT coupon_id, promotion FROM coupons WHERE NOT coupon_id is NULL'
        couponResult = execute_query(db_connection, query).fetchall()

    return render_template("update_order.html", data=result, customers=customerResult, coupons=couponResult)


@app.route("/update_order", methods=["POST"])
def update():
    db_connection = connect_to_database()
    alerts = ()

    # Fetch data from the form
    orderID = request.form["orderID"]
    orderDate = request.form['orderDate']
    numProducts = request.form['numberOfProducts']
    cost = request.form['totalCost']
    customerID = request.form['customerID']
    couponID = request.form['couponID']

    # If no coupon is selected
    if couponID == 'NULL':
        couponID = None

        # Run update query
        query = "UPDATE orders SET order_date = %s, num_products = %s, total_cost = %s, customer_id = %s, coupon_id = %s WHERE order_id = %s"
        data = (orderDate, numProducts, cost, customerID, couponID, orderID)
        execute_query(db_connection, query, data)
        alerts = ("Update successful!", False)

    else:
        # The following query is to check if the selected coupon is valid for the selected customer
        query = 'SELECT customer_id, coupon_id FROM coupons_customers WHERE customer_id = %s AND coupon_id = %s'
        query_params = (customerID, couponID)
        result = execute_query(db_connection, query,
                               query_params).fetchone()

        # Check result. If it is None, then an invalid coupon was selected
        if result is None:
            # If customer can't use the indicated coupon, check to see which coupons they can use
            query = """SELECT fname, lname, promotion FROM customers c
                    LEFT JOIN coupons_customers cc ON c.customer_id = cc.customer_id
                    LEFT JOIN coupons ON cc.coupon_id = coupons.coupon_id
                    WHERE c.customer_id = %s"""
            query_params = (customerID)
            checkAvailableCoupons = execute_query(
                db_connection, query, query_params).fetchall()

            # Retrieve the cusomer's name
            customerName = checkAvailableCoupons[0][0] + \
                ' ' + checkAvailableCoupons[0][1]

            # If customer does not have any promotions available, then the result will be of length 1
            # and None will be present where the promotion should be
            if len(checkAvailableCoupons) == 1 and checkAvailableCoupons[0][2] is None:
                alerts = (
                    f"Error! Order not updated! {customerName} can not apply any coupon to their orders. Please try again.", True)
            else:
                # Retrieve all promotions that a customer can use, store it in correctCoupons
                correctCoupons = ''
                for result in checkAvailableCoupons:
                    correctCoupons += str(result[2])
                    correctCoupons += ', '
                alerts = (
                    f"Error! Order not updated! {customerName} can only apply the following coupon(s) to their order: {correctCoupons}. Please try again.", True)

        else:
            query = "UPDATE orders SET order_date = %s, num_products = %s, total_cost = %s, customer_id = %s, coupon_id = %s WHERE order_id = %s"
            data = [orderDate, numProducts, cost,
                    customerID, couponID, orderID]
            execute_query(db_connection, query, data)
            alerts = ("Update successful!", False)

    # Create query strings and execute to retrieve required data from database
    query = 'SELECT * FROM orders'
    result = execute_query(db_connection, query).fetchall()

    query = 'SELECT customer_id, fname, lname FROM customers'
    customerResult = execute_query(db_connection, query).fetchall()

    query = 'SELECT coupon_id, promotion FROM coupons'
    couponResult = execute_query(db_connection, query).fetchall()

    return render_template('orders.html', rows=result, customers=customerResult, coupons=couponResult, alerts=alerts)


if __name__ == '__main__':
    app.run(debug=True)
