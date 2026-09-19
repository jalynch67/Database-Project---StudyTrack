import os
from datetime import date, datetime

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from models import StudyTask, Subject, db


load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    os.environ.get("DATABASE_URL") or "sqlite:///studytrack.db"
)
app.config["SECRET_KEY"] = (
    os.environ.get("SECRET_KEY") or "development-key"
)

db.init_app(app)


@app.route("/")
def index():
    """Display dashboard statistics and upcoming study tasks."""
    today = date.today()

    total_subjects = Subject.query.count()
    total_tasks = StudyTask.query.count()
    open_tasks = StudyTask.query.filter_by(is_complete=False).count()
    completed_tasks = StudyTask.query.filter_by(is_complete=True).count()
    overdue_tasks = StudyTask.query.filter(
        StudyTask.is_complete.is_(False),
        StudyTask.due_date < today,
    ).count()
    upcoming_tasks = StudyTask.query.filter(
        StudyTask.is_complete.is_(False),
        StudyTask.due_date >= today,
    ).order_by(StudyTask.due_date).limit(5).all()

    return render_template(
        "index.html",
        total_subjects=total_subjects,
        total_tasks=total_tasks,
        open_tasks=open_tasks,
        completed_tasks=completed_tasks,
        overdue_tasks=overdue_tasks,
        upcoming_tasks=upcoming_tasks,
        today=today,
    )


@app.route("/subjects")
def subjects():
    """Display all subjects."""
    all_subjects = Subject.query.order_by(Subject.name).all()
    return render_template("subjects/list.html", subjects=all_subjects)


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


@app.route("/subjects/<int:subject_id>")
def subject_detail(subject_id):
    """Display one subject and its related tasks."""
    subject = Subject.query.get_or_404(subject_id)
    subject_tasks = StudyTask.query.filter_by(subject_id=subject.id).order_by(
        StudyTask.due_date
    ).all()

    return render_template(
        "subjects/detail.html",
        subject=subject,
        tasks=subject_tasks,
    )


@app.route("/subjects/<int:subject_id>/edit", methods=["GET", "POST"])
def edit_subject(subject_id):
    """Display the edit form and update a subject."""
    subject = Subject.query.get_or_404(subject_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        colour = request.form.get("colour", "blue")
        allowed_colours = ["blue", "green", "purple", "orange", "red"]

        if not name:
            flash("Please enter a subject name.", "error")
            return render_template("subjects/edit.html", subject=subject)

        if len(name) > 100:
            flash("The subject name must be 100 characters or fewer.", "error")
            return render_template("subjects/edit.html", subject=subject)

        if colour not in allowed_colours:
            flash("Please select a valid subject colour.", "error")
            return render_template("subjects/edit.html", subject=subject)

        subject.name = name
        subject.description = description or None
        subject.colour = colour
        db.session.commit()

        flash("Subject updated successfully.", "success")
        return redirect(url_for("subject_detail", subject_id=subject.id))

    return render_template("subjects/edit.html", subject=subject)


@app.route("/subjects/<int:subject_id>/delete", methods=["GET", "POST"])
def delete_subject(subject_id):
    """Display a confirmation page and delete a subject."""
    subject = Subject.query.get_or_404(subject_id)

    if request.method == "POST":
        db.session.delete(subject)
        db.session.commit()
        flash("Subject deleted successfully.", "success")
        return redirect(url_for("subjects"))

    return render_template("subjects/delete.html", subject=subject)


@app.route("/tasks")
def tasks():
    """Display study tasks using the selected status filter."""
    status = request.args.get("status", "all")
    task_query = StudyTask.query

    if status == "open":
        task_query = task_query.filter_by(is_complete=False)
    elif status == "completed":
        task_query = task_query.filter_by(is_complete=True)
    else:
        status = "all"

    all_tasks = task_query.order_by(StudyTask.due_date).all()

    return render_template(
        "tasks/list.html",
        tasks=all_tasks,
        current_status=status,
    )


@app.route("/tasks/add", methods=["GET", "POST"])
def add_task():
    """Display the task form and save a new study task."""
    all_subjects = Subject.query.order_by(Subject.name).all()

    if not all_subjects:
        flash("Add a subject before creating a study task.", "error")
        return redirect(url_for("add_subject"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        due_date_text = request.form.get("due_date", "")
        priority = request.form.get("priority", "medium")
        subject_id = request.form.get("subject_id", type=int)
        allowed_priorities = ["low", "medium", "high"]

        if not title:
            flash("Please enter a task title.", "error")
            return render_template("tasks/add.html", subjects=all_subjects)

        if len(title) > 150:
            flash("The task title must be 150 characters or fewer.", "error")
            return render_template("tasks/add.html", subjects=all_subjects)

        try:
            due_date = datetime.strptime(due_date_text, "%Y-%m-%d").date()
        except ValueError:
            flash("Please enter a valid due date.", "error")
            return render_template("tasks/add.html", subjects=all_subjects)

        if priority not in allowed_priorities:
            flash("Please select a valid priority.", "error")
            return render_template("tasks/add.html", subjects=all_subjects)

        subject = db.session.get(Subject, subject_id)
        if subject is None:
            flash("Please select a valid subject.", "error")
            return render_template("tasks/add.html", subjects=all_subjects)

        task = StudyTask(
            title=title,
            description=description or None,
            due_date=due_date,
            priority=priority,
            subject_id=subject.id,
        )
        db.session.add(task)
        db.session.commit()

        flash("Study task added successfully.", "success")
        return redirect(url_for("tasks"))

    return render_template("tasks/add.html", subjects=all_subjects)


@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    """Display the edit form and update a study task."""
    task = StudyTask.query.get_or_404(task_id)
    all_subjects = Subject.query.order_by(Subject.name).all()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        due_date_text = request.form.get("due_date", "")
        priority = request.form.get("priority", "medium")
        subject_id = request.form.get("subject_id", type=int)
        allowed_priorities = ["low", "medium", "high"]

        if not title:
            flash("Please enter a task title.", "error")
            return render_template(
                "tasks/edit.html",
                task=task,
                subjects=all_subjects,
            )

        if len(title) > 150:
            flash("The task title must be 150 characters or fewer.", "error")
            return render_template(
                "tasks/edit.html",
                task=task,
                subjects=all_subjects,
            )

        try:
            due_date = datetime.strptime(due_date_text, "%Y-%m-%d").date()
        except ValueError:
            flash("Please enter a valid due date.", "error")
            return render_template(
                "tasks/edit.html",
                task=task,
                subjects=all_subjects,
            )

        if priority not in allowed_priorities:
            flash("Please select a valid priority.", "error")
            return render_template(
                "tasks/edit.html",
                task=task,
                subjects=all_subjects,
            )

        subject = db.session.get(Subject, subject_id)
        if subject is None:
            flash("Please select a valid subject.", "error")
            return render_template(
                "tasks/edit.html",
                task=task,
                subjects=all_subjects,
            )

        task.title = title
        task.description = description or None
        task.due_date = due_date
        task.priority = priority
        task.subject_id = subject.id
        db.session.commit()

        flash("Study task updated successfully.", "success")
        return redirect(url_for("tasks"))

    return render_template(
        "tasks/edit.html",
        task=task,
        subjects=all_subjects,
    )


@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    """Change a study task between open and complete."""
    task = StudyTask.query.get_or_404(task_id)
    task.is_complete = not task.is_complete
    db.session.commit()

    if task.is_complete:
        flash("Study task marked as complete.", "success")
    else:
        flash("Study task returned to open.", "success")

    return redirect(request.referrer or url_for("tasks"))


@app.route("/tasks/<int:task_id>/delete", methods=["GET", "POST"])
def delete_task(task_id):
    """Display a confirmation page and delete a study task."""
    task = StudyTask.query.get_or_404(task_id)

    if request.method == "POST":
        db.session.delete(task)
        db.session.commit()

        flash("Study task deleted successfully.", "success")
        return redirect(url_for("tasks"))

    return render_template("tasks/delete.html", task=task)


@app.route("/about")
def about():
    """Display information about StudyTrack."""
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
