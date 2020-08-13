from flask import Flask, render_template, url_for, request, redirect
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
                query_params = (customerID,)
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

    search_request = request.args.get('searchBar')

    # Check if user uses the search bar
    if search_request is not None:
        search_request.strip()
        query = f"SELECT * FROM products WHERE item_name LIKE '%{search_request}%'"
        result = execute_query(db_connection, query).fetchall()

    else:
        # Create query strings and execute to product table data
        query = 'SELECT * FROM products'
        result = execute_query(db_connection, query).fetchall()

    return render_template("products.html", rows=result, alerts=alerts, search=search_request)

# Customers


@app.route("/customers", methods=['POST', 'GET'])
def customers():
    db_connection = connect_to_database()
    alerts = ()

    if request.method == 'POST':
        # Store data from form
        fname = request.form['fname']
        lname = request.form['lname']
        signupDate = request.form['signupDate']
        birthdate = request.form['birthdate']

        # Query data to insert into table
        query = 'INSERT INTO customers (fname, lname, signup_date, birthdate) VALUES (%s, %s, %s, %s)'
        data = (fname, lname, signupDate, birthdate)
        execute_query(db_connection, query, data)
        alerts = ("Success! Database updated!", False)

    # Query data to display in table
    query = 'SELECT * FROM customers'
    result = execute_query(db_connection, query).fetchall()

    return render_template("customers.html", rows=result, alerts=alerts)

# Coupons


@app.route("/coupons", methods=['POST', 'GET'])
def coupons():
    db_connection = connect_to_database()
    alerts = ()

    if request.method == 'POST':
        # Store data from form
        promotion = request.form['promotion']
        percentOff = request.form['percentOff']

        # Query data to insert into table
        query = 'INSERT INTO coupons (promotion, percent_off) VALUES (%s, %s)'
        data = (promotion, percentOff)
        execute_query(db_connection, query, data)
        alerts = ("Success! Database updated!", False)

    # Query data to display in table
    query = 'SELECT * FROM coupons'
    result = execute_query(db_connection, query).fetchall()

    return render_template("coupons.html", rows=result, alerts=alerts)


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
    result = execute_query(db_connection, query).fetchall()

    query = 'SELECT order_id, fname, lname, order_date FROM orders LEFT JOIN customers ON orders.customer_id = customers.customer_id'
    orders = execute_query(db_connection, query).fetchall()

    query = 'SELECT product_id, item_name FROM products'
    products = execute_query(db_connection, query).fetchall()

    return render_template("orders_products.html", rows=result, orders=orders, products=products, alerts=alerts)


# Coupons_Customers Intersection Table

@app.route("/coupons_customers", methods=['POST', 'GET'])
def coupons_customers():
    db_connection = connect_to_database()
    alerts = ()

    if request.method == 'POST':
        # Store data from form
        couponID = request.form['couponID']
        customerID = request.form['customerID']

        query = 'INSERT IGNORE INTO coupons_customers (coupon_id, customer_id) VALUES (%s, %s)'
        data = (couponID, customerID)
        execute_query(db_connection, query, data)
        alerts = ("Success! Database updated!", False)

    # Query data for form dropdowns
    query = 'SELECT coupon_id, promotion FROM coupons'
    coupons = execute_query(db_connection, query).fetchall()

    query = 'SELECT customer_id, fname, lname FROM customers'
    customers = execute_query(db_connection, query).fetchall()

    # Query data to display in table
    query = 'SELECT coup.promotion, cust.fname, cust.lname FROM coupons_customers cc LEFT JOIN coupons coup ON cc.coupon_id = coup.   coupon_id LEFT JOIN customers cust ON cc.customer_id = cust.customer_id'
    result = execute_query(db_connection, query).fetchall()

    return render_template("coupons_customers.html", rows=result, coupons=coupons, customers=customers, alerts=alerts)


# Delete coupon from coupon table and coupons_customers table

@app.route("/delete_coupon/<int:id>")
def delete_coupon(id):
    db_connection = connect_to_database()
    alerts = ()

    # Delete from coupons_customers first
    query = 'DELETE FROM coupons_customers WHERE coupon_id = %s'
    data = (id,)
    execute_query(db_connection, query, data)

    # Delete from coupons
    query = 'DELETE FROM coupons WHERE coupon_id = %s'
    data = (id,)
    execute_query(db_connection, query, data)

    alerts = (
        "Coupon successfully deleted from coupons and coupons/customers!", False)

    # Query data to display in table
    query = 'SELECT * FROM coupons'
    result = execute_query(db_connection, query).fetchall()

    return render_template("coupons.html", rows=result, alerts=alerts)


# Update order page

@app.route("/orders/update/<int:id>", methods=['POST', "GET"])
def update_order(id):
    db_connection = connect_to_database()
    alerts = ()

    # Build Select query to populate form
    query = """SELECT DISTINCT order_id, order_date, num_products, total_cost, fname, lname, c.customer_id, o.coupon_id, promotion FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.customer_id
            LEFT JOIN coupons ON o.coupon_id = coupons.coupon_id
            WHERE o.order_id = %s"""
    data = (id,)
    old_order_data = execute_query(db_connection, query, data).fetchone()

    if request.method == "POST":

        # Fetch data from the form
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
            data = (orderDate, numProducts, cost,
                    customerID, couponID, id)
            execute_query(db_connection, query, data)
            alerts = (
                "Update successful! Please refresh or return to the order page to see the updated order.", False)

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
                query_params = (customerID,)
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
                        customerID, couponID, id]
                execute_query(db_connection, query, data)
                alerts = (
                    "Update successful! Please refresh or return to the order page to see the updated order.", False)

    # Get all customers except for one from initial query
    query = f'SELECT customer_id, fname, lname FROM customers WHERE NOT customer_id = {old_order_data[6]}'
    customerResult = execute_query(db_connection, query).fetchall()

    # Get all coupons except for one from initial query
    if old_order_data[7] is not None:
        query = f'SELECT coupon_id, promotion FROM coupons WHERE NOT coupon_id = {old_order_data[7]}'
        couponResult = execute_query(db_connection, query).fetchall()
    else:
        query = f'SELECT coupon_id, promotion FROM coupons WHERE NOT coupon_id is NULL'
        couponResult = execute_query(db_connection, query).fetchall()

    return render_template("update_order.html", data=old_order_data, customers=customerResult, coupons=couponResult, alerts=alerts)


if __name__ == '__main__':
    app.run(debug=True)
