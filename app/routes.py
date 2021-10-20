from app import app, db, bcrypt
from flask import render_template, url_for, request, redirect, flash
from app.forms import SignInForm, SignUpForm, TodoForm
from app.models import user, todo
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route('/sign-up', methods=["GET", "POST"])
def sign_up_page():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate_on_submit():
            gender=request.form.get("gender")
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user_info = user(f_name=form.full_name.data,
                            username=form.username.data,
                            email=form.email_address.data,
                            ph_no=form.phone_number.data,
                            gender=gender,
                            password_hash=hashed_password)
            db.session.add(user_info)
            db.session.commit()
            login_user(user_info)
            flash(f"Created account for {form.username.data}!", category="success")
            return redirect(url_for('notes_page'))
        else:
            return render_template('sign-up.html', form=form)
    if request.method == "GET":
        return render_template('sign-up.html', form=form)

@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes_page():
    form = TodoForm()
    if request.method == "POST":
        if "add_todo" in request.form:
            text = form.text.data
            if text:
                current_user.add_text(text)
                flash("Added a new todo item!", category="success")
            else:
                flash("You can't add empty item!", category="danger")

        if "com_mark" in request.form:
            todo_id = request.form.get('com_mark')
            if todo_id:
                current_user.mark_as_completed(todo_id)

        if "incom_mark" in request.form:
            todo_id = request.form.get("incom_mark")
            if todo_id:
                current_user.mark_as_incomplete(todo_id)

        if "delete_note" in request.form:
            todo_id = request.form.get("delete_note")
            if todo_id:
                current_user.delete_todo(todo_id)

        return redirect(url_for('notes_page'))
    if request.method == "GET":
        incomplete_items = todo.query.filter_by(complete=False, user_id=current_user.id)
        incomplete_item = todo.query.filter_by(complete=False, user_id=current_user.id).first()
        completed_items = todo.query.filter_by(complete=True, user_id=current_user.id)
        completed_item = todo.query.filter_by(complete=True, user_id=current_user.id).first()
            
        return render_template('notes.html', form=form, incomplete_items=incomplete_items, incomplete_item=incomplete_item, completed_item=completed_item, completed_items=completed_items)

@app.route('/sign-in', methods=["GET", "POST"])
def sign_in_page():
    form = SignInForm()
    if request.method == "POST":
        if form.validate_on_submit():
            attemted_user = user.query.filter_by(username=form.username.data, email=form.email_address.data).first()
            if attemted_user:
                password_check = bcrypt.check_password_hash(attemted_user.password_hash, form.password.data)
                if password_check:
                    login_user(attemted_user)
                    flash(f"Signed-in as {attemted_user.username}!", category="success")
                    return redirect(url_for('notes_page'))
                else:
                    flash("Password doesn't match!", category="danger")
                    return render_template('sign-in.html', form=form)
            else:
                flash("Username/Email didn't match!", category="danger")
                return render_template('sign-in.html', form=form)
        else:
            return render_template('sign-in.html', form=form)
    if request.method == "GET":
        return render_template('sign-in.html', form=form)

@app.route('/sign-out')
def sign_out_page():
    logout_user()
    flash(f"Logged out!", category='success')
    return render_template('index.html')