from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'key'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

complete_messages = [
    "Task completed. Still you are a failure 😜",
    "Mission accomplished! Time for a victory dance, But I am an Introvert 🥺",
    "Never let a good task decide what failure you have become 😂"
]

delete_messages = [
    "It's like the task never existed. Like me 🥺 ",
    "Task deleted. Consider it your failure 😜. You Twat",
    "You think you can complete the task by deleting it 👊😡👊"
]

@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:todo_id>', methods=['GET', 'POST'])
def index(todo_id=None):
    todo = None

    if request.method == 'POST':
        title = request.form.get('title')
        if todo_id:
            todo = Todo.query.get(todo_id)
            if todo:
                todo.title = title
                db.session.commit()
                flash(random.choice(complete_messages))
        else:
            todo = Todo(title=title)
            db.session.add(todo)
            db.session.commit()

        return redirect(url_for('index'))

    if todo_id:
        todo = Todo.query.get(todo_id)
    
    todos = Todo.query.order_by(Todo.id.desc()).all()
    return render_template('index.html', todos=todos, todo=todo)

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash(random.choice(delete_messages))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
