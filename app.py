from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#initialize flask app
app = Flask(__name__)

#point to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#initialize database
db = SQLAlchemy(app)

#Todo model definition
class Todo(db.Model):
    #table column definitions
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

#activate sqlite database
#with app.app_context():
#    db.create_all()

#home route
@app.route('/', methods=['POST', 'GET'])
#define route funcion
def index():
    if request.method == "POST":
        task_conent = request.form['content']
        new_task = Todo(content=task_conent)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error during task addition"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)
    
#delete task route
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error during task deletion'

#update task route
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error while updating task"
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)