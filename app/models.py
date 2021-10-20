from app import db, login_manager
from flask_login import  UserMixin


@login_manager.user_loader
def load_user(user_id):
    return user.query.get(user_id)
class user(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    f_name = db.Column(db.String(length=18), nullable=False)
    username = db.Column(db.String(length=8), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    ph_no = db.Column(db.String(), nullable=False, unique=True)
    gender = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=False, default="default.png")
    todos = db.relationship('todo', lazy=True, backref="user_todos")

    def __repr__(self):
        return self.username + str(self.id)
    
    def add_text(self, text):
        new_todo = todo(text=text, user_id=self.id)
        db.session.add(new_todo)
        db.session.commit()

    def mark_as_completed(self, todo_id):
        todo_to_mark = todo.query.filter_by(id=todo_id).first()
        todo_to_mark.complete = True
        db.session.add(todo_to_mark)
        db.session.commit()

    def mark_as_incomplete(self, todo_id):
        todo_to_mark = todo.query.filter_by(id=todo_id).first()
        todo_to_mark.complete = False
        db.session.add(todo_to_mark)
        db.session.commit()
    
    def delete_todo(self, todo_id):
        todo_to_delete = todo.query.filter_by(id=todo_id).first()
        db.session.delete(todo_to_delete)
        db.session.commit()


class todo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(length=200), default="todos")
    complete = db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))


    def __repr__(self):
        return self.text + str(self.id)

    