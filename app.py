import os

from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, request, url_for

from models import db, Subject


load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite://studytrack.db",
)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "development-key",
)

db.init_app(app)


@app.route("/")
def index():
    """Display the StudyTrack homepage."""
    return render_template("index.html")


@app.route("/subjects")
def subjects():
    """Display all subjects."""
    all_subjects = Subject.query.order_by(Subject.name).all()
    return render_template(
        "subjects/list.html",
        subjects=all_subjects,
    )

@app.route("/subjects/add", methods=["GET", "POST"])
def add_subject():
    """Display the subject form and save a new subject."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        colour = request.form.get("colour", "blue")
        allowed_colours = ["blue", "green", "purple", "orange", "red"]

        if not name:
            flash("Please enter a subject name.", "error")
            return render_template("subjects/add.html")

        if len(name) > 100:
            flash("The subject name must be 100 characters or fewer.", "error")
            return render_template("subjects/add.html")

        if colour not in allowed_colours:
            flash("Please select a valid subject colour.", "error")
            return render_template("subjects/add.html")

        subject = Subject(
            name=name,
            description=description or None,
            colour=colour,
        )

        db.session.add(subject)
        db.session.commit()

        flash("Subject added successfully.", "success")
        return redirect(url_for("subjects"))

    return render_template("subjects/add.html")


@app.route("/about")
def about():
    """Display information about StudyTrack."""
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True) 
