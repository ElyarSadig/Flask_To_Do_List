from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Task
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def task_list():
    count = Task.query.filter_by(user_id=current_user.id, complete=False).count()
    plural = True if count > 1 else False
    tasks = current_user.tasks
    search_input = ''

    if request.method == "POST":
        search = request.form.get('search-area')
        search_input = search
        result = Task.query.filter(Task.title.like(f'%{search}%'), Task.user_id == current_user.id).all()
        tasks = result

    return render_template("task_list.html", user=current_user, plural=plural, count=count, tasks=tasks,
                           search_input=search_input)


@views.route('/task-create', methods=['GET', 'POST'])
@login_required
def task_form():

    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        complete = request.form.get('complete')

        if complete:
            complete = True

        new_task = Task(title=title, description=description, complete=complete, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task created!", category='success')
        return redirect(url_for('views.task_list'))

    return render_template("task_form.html", user=current_user)


@views.route('/task-delete/<int:id>', methods=['GET', 'POST'])
@login_required
def task_delete(id):
    task = Task.query.filter_by(id=id).first()
    if request.method == "POST":
        db.session.delete(task)
        db.session.commit()
        flash("Task Deleted!", category='success')
        return redirect(url_for("views.task_list"))

    return render_template("task_confirm_delete.html", task=task)


@views.route('/task-update/<int:id>', methods=['GET', 'POST'])
@login_required
def task_update(id):
    task = Task.query.filter_by(id=id).first()
    if request.method == "POST":
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        complete = request.form.get('complete')

        if complete:
            complete = True
        else:
            complete = False

        task.complete = complete
        db.session.commit()
        flash("Task Updated!", category='success')
        return redirect(url_for("views.task_list"))

    return render_template("task_update.html", task=task)


