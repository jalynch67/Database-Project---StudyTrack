import os

from dotenv import load_dotenv
from flask import Flask, render_template

from models import db


load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite://studytrack.db",
)

db.init_app(app)


@app.route("/")
def index():
    """Display the StudyTrack homepage."""
    return render_template("index.html")


@app.route("/about")
def about():
    """Display information about StudyTrack."""
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True) 
