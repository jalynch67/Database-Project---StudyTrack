# StudyTrack

StudyTrack is a database-driven study planner built with Flask and
PostgreSQL. It allows users to organise subjects, create study tasks,
set deadlines and priorities, and track progress from a dashboard.

The main aim of the project was to design a relational database and connect
it to a Flask application with full CRUD functionality.

## Live Application

The deployed application is available here:

https://studytrack-f56l.onrender.com

https://github.com/jalynch67/Database-Project---StudyTrack


## Features

### Subjects

Users can:

- View all subjects
- Add a new subject
- Choose a colour for each subject
- Add an optional description
- View the tasks linked to a subject
- Edit an existing subject
- Delete a subject

Deleting a subject also deletes the study tasks that belong to it. A
confirmation page warns the user before the deletion is completed.

### Study Tasks

Users can:

- View all study tasks
- Add a new task
- Link each task to a subject
- Add an optional description
- Set a due date
- Select a low, medium, or high priority
- Edit an existing task
- Mark a task as complete or return it to open
- Filter tasks by all, open, or completed
- Delete a task

When a task is added from a subject details page, the relevant subject
is selected automatically.

### Dashboard

The dashboard displays:

- Total number of subjects
- Total number of tasks
- Number of open tasks
- Number of completed tasks
- Number of overdue tasks
- Overall completion percentage
- The next five upcoming open tasks

Completed tasks are excluded from the overdue and upcoming task
calculations.

### Other Features

- Responsive layouts for desktop, tablet, and mobile screens
- Flash messages following successful or unsuccessful actions
- Server-side form validation
- Confirmation pages before deleting records
- Custom 404 and 500 error pages
- Visible keyboard focus indicators
- Persistent PostgreSQL data storage

## Database Design

StudyTrack uses two related database tables:

- `subjects`
- `study_tasks`

Each subject can have many study tasks, while every study task must
belong to one subject. This is a one-to-many relationship.

The `subject_id` field in `study_tasks` is a foreign key that references
the `id` field in `subjects`.

The SQLAlchemy relationship uses cascade deletion. This means that
deleting a subject also removes the tasks linked to that subject.

## How to Deploy StudyTrack

StudyTrack can be deployed using Render with a hosted PostgreSQL database.

### 1. Create a Copy of the Repository

Fork this repository on GitHub, or clone it and push it to a new GitHub repository.

The repository must contain the main application files and folders:

```text
app.py
models.py
init_db.py
requirements.txt
templates/
static/
```

### 2. Create a PostgreSQL Database

1. Sign in to Render.
2. Select **New** and then **Postgres**.
3. Enter a name for the database.
4. Choose a region.
5. Select a suitable database plan.
6. Create the database.
7. Wait until the database status changes to **Available**.
8. Copy the **Internal Database URL** from the database information page.

The PostgreSQL database and Web Service should use the same Render region.

### 3. Create a Render Web Service

1. Select **New** and then **Web Service**.
2. Connect the GitHub repository containing StudyTrack.
3. Select the branch containing the application, normally `main`.
4. Choose **Python** as the runtime.
5. Choose the same region as the PostgreSQL database.

Use the following build command:

```bash
pip install -r requirements.txt
```

Use the following start command:

```bash
python init_db.py && gunicorn app:app
```

The `init_db.py` script creates the database tables if the tables do not already exist. Running the script again does not delete existing records.

### 4. Configure Environment Variables

Add the following environment variables to the Render Web Service:

```text
DATABASE_URL
SECRET_KEY
```

Set `DATABASE_URL` to the **Internal Database URL** copied from the Render PostgreSQL database.

Generate a secure value for `SECRET_KEY` locally with:

```bash
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

Copy the generated value into the `SECRET_KEY` environment variable in Render.

### 5. Deploy the Application

Create the Web Service and wait for the build to finish.

A successful deployment log should confirm that:

- The packages in `requirements.txt` were installed
- The database tables were created
- Gunicorn started successfully
- The Web Service changed to **Live**

Render will provide a public URL for the deployed application.

### 6. Test the Deployment

Open the public Render URL and test the following:

- Dashboard, Subjects, Tasks, and About pages
- Creating, viewing, editing, and deleting a subject
- Creating, editing, completing, filtering, and deleting a task
- Adding a task from a subject details page
- Dashboard totals and progress calculations
- Subject deletion with related tasks
- The custom 404 page
- Mobile and keyboard navigation

### 7. Confirm Database Persistence

Create a temporary subject and task through the hosted application.

Redeploy or restart the Render Web Service and confirm that both records are still available. This verifies that the application is using the persistent PostgreSQL database rather than temporary local storage.