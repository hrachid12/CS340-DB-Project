from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.fields.html5 import DateField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email, Length, NumberRange, InputRequired


class OrderForm(FlaskForm):
    order_date = DateField('Order Date', [DataRequired()])
    num_products = IntegerField('Number of Products', [
                                DataRequired(), NumberRange(min=1, max=None)])
    total_cost = DecimalField('Total Cost (in dollars)', [
                              InputRequired(), NumberRange(min=0, max=None)], places=2)
    customer_id = IntegerField('Customer ID Number', [
                               DataRequired(), NumberRange(min=1, max=None)])
    coupon_id = IntegerField('Coupon ID', [NumberRange(min=1, max=None)])
    submit = SubmitField('Submit')


class ProductForm(FlaskForm):
    item_name = StringField('Item Name', [DataRequired()])
    price = DecimalField('Price (in dollars)', [
        InputRequired(), NumberRange(min=0, max=None)], places=2)
    quantity = IntegerField('Quantity Available', [
        InputRequired(), NumberRange(min=1, max=None)])
    submit = SubmitField('Submit')


class OrderProductForm(FlaskForm):
    order_id = IntegerField(
        "Order ID", [DataRequired(), NumberRange(min=1, max=None)])
    product_id = IntegerField(
        "Product ID", [DataRequired(), NumberRange(min=1, max=None)])
    submit = SubmitField('Submit')
