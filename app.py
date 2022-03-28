
from email import message
# from sqlalchemy_utils import EmailType
from unicodedata import name
from flask import Flask, render_template, request, redirect , flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///all.db"
app.config["SQLALCHEMY_BINDS"] = {
    'todo' : 'sqlite:///todo.db',
    'contactme': 'sqlite:///contactme.db'
}
app.config.from_object(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "my super secret key"







class Todo(db.Model):
    __bind_key__ = 'todo'
 
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


class Contact(db.Model):
    __bind_key__ = 'contactme'
    id = db.Column('id',db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), nullable=False)
    email = db.Column(db.String(50) , nullable = False)
    phone = db.Column(db.Unicode(20) , nullable = False)
    message = db.Column(db.String(520), nullable=False)





@app.route("/todo", methods=['GET', 'POST'])
def todoo():
    if request.method == 'POST':
        flash("Task Saved Successfully")  
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('todo.html', alltodo=alltodo)


@app.route("/show", methods=['GET', 'POST'])
def showtodo():
    alltodo = Todo.query.all()
    return render_template('table.html', alltodo=alltodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    flash("TODO Deleted Successfully") 
    return redirect('/show')


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.route('/about')
def about_me():
    return render_template('index2.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact' ,methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # print("Posted")
        flash('All fields are required.')
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        contact = Contact(name = name , email = email , phone = phone , message = message)
        db.session.add(contact)
        db.session.commit()
        flash('Submited')
        return redirect("/contact")
    conntact = Contact.query.all()
    return render_template('contact.html')

@app.route('/projects')
def projects():
    return render_template('project.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')



if __name__ == "__main__":

    app.run(debug=True, port=9000)
 