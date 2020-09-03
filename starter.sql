-- Create customer, coupons, and coupons_customers
CREATE TABLE customers (
    customer_id SERIAL NOT NULL,
    fname varchar(255) NOT NULL,
    lname varchar(255) NOT NULL,
    signup_date date NOT NULL,
    birthdate date NOT NULL,
    PRIMARY KEY (customer_id)
);

CREATE TABLE coupons (
    coupon_id SERIAL NOT NULL,
    percent_off int NOT NULL,
    promotion varchar(255) NOT NULL,
    PRIMARY KEY (coupon_id)
);

CREATE TABLE coupons_customers (
    id SERIAL NOT NULL,
    coupon_id int,
    customer_id int,
    PRIMARY KEY (id),
    FOREIGN KEY (coupon_id) REFERENCES coupons(coupon_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);


-- Create orders, products, and orders_products tables
CREATE TABLE orders (
    order_id SERIAL NOT NULL,
    order_date date NOT NULL,
    num_products int NOT NULL,
    total_cost decimal(7, 2) NOT NULL,
    customer_id int NOT NULL,
    coupon_id int,
    PRIMARY KEY (order_id),
    CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON UPDATE CASCADE,
    CONSTRAINT fk_order_coupon FOREIGN KEY (coupon_id) REFERENCES coupons (coupon_id) ON UPDATE CASCADE
);

CREATE TABLE products (
    product_id SERIAL NOT NULL,
    item_name varchar(255) NOT NULL,
    price decimal(7, 2) NOT NULL,
    quantity_available int NOT NULL,
    PRIMARY KEY (product_id)
);

CREATE TABLE orders_products (
    id SERIAL NOT NULL,
    order_id int NOT NULL,
    product_id int NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_order_id FOREIGN KEY (order_id) REFERENCES orders (order_id) ON UPDATE CASCADE,
    CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES products (product_id) ON UPDATE CASCADE
);


-- -- Insert some data into tables
INSERT INTO customers (fname, lname, signup_date, birthdate) VALUES
    ('Zack', 'Clarke', '2020-06-20', '1977-04-10'),
    ('Patricia', 'Rogers', '2020-07-07', '1985-10-08'),
    ('Steve', 'White', '2019-12-19', '1982-08-16'),
    ('Jacob', 'Peters', '2020-01-27', '2002-10-31'),
    ('Molly', 'Hamilton', '2020-02-19', '1954-09-17'),
    ('Karen', 'Newman', '2019-11-22', '1971-05-01'),
    ('John', 'Lincoln', '2020-04-30', '1990-06-29'),
    ('Taylor', 'Day', '2020-05-02', '1989-12-12'),
    ('Philip', 'Lee', '2019-12-09', '1995-03-09'),
    ('Samuel', 'Kim', '2020-01-26', '1993-07-21');

INSERT INTO coupons (percent_off, promotion) VALUES
    (20, 'Birthday Bonus'),
    (25, 'July 4th Deals'),
    (29, 'Leap Year Spectacular'),
    (15, 'New Year, New Books'),
    (30, 'Black Friday');

INSERT INTO coupons_customers (coupon_id, customer_id) VALUES
    (1, 7),
    (1, 10),
    (2, 1),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 8),
    (2, 9),
    (3, 3),
    (3, 4),
    (3, 5),
    (3, 6),
    (3, 9),
    (3, 10),
    (4, 3),
    (4, 6),
    (4, 9);

INSERT INTO products (item_name, price, quantity_available) VALUES
    ('The Way of Kings: Book One of The Stormlight Archive', 15, 10),
    ('A Game of Thrones: A Song of Ice and Fire, Book 1', 19.99, 13),
    ('A Short History of Nearly Everything', 22.49, 9),
    ('Where the Crawdads Sing', 22.99, 4),
    ('The Guest List', 24.99, 14),
    ('Camino Winds', 20, 20),
    ('The Summer House', 19.50, 12),
    ('Mexican Gothic', 23.99, 7),
    ('If It Bleeds', 21, 10),
    ('Fair Warning', 20, 11),
    ('The Woman in the Window', 13.99, 22),
    ('The Nightingale', 13.99, 22),
    ('All the Light We Cannot See', 14.99, 5);


INSERT INTO orders (order_date, num_products, total_cost, customer_id, coupon_id) VALUES
    ('2020-03-11', 2, 28, 3, 1),
    ('2020-03-18', 1, 22.49, 1, NULL),
    ('2020-03-22', 3, 45.98, 2, 1),
    ('2020-04-01', 1, 19.50, 9, NULL),
    ('2020-04-24', 3, 64.49, 5, NULL),
    ('2020-04-24', 1, 11.59, 4, 1),
    ('2020-05-05', 2, 27.98, 10, NULL),
    ('2020-05-21', 1, 24.99, 3, NULL),
    ('2020-06-13', 3, 51.20, 7, 1),
    ('2020-07-04', 3, 36.75, 8, 2);




INSERT INTO orders_products (order_id, product_id) VALUES
    (1, 1),
    (1, 2),
    (2, 3), 
    (3, 1), 
    (3, 2), 
    (3, 3), 
    (4, 7), 
    (5, 4),
    (5, 7),
    (5, 9),
    (6, 13), 
    (7, 11), 
    (7, 12), 
    (8, 5),
    (9, 6),
    (9, 8), 
    (9, 10),
    (10, 1),
    (10, 6), 
    (10, 12);





