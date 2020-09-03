from flask import Flask


app = Flask(__name__)

from fine_print.main.routes import main 

app.register_blueprint(main)
