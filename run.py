# Run this from the command line using "python run.py" to start the webapp

from fine_print import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
