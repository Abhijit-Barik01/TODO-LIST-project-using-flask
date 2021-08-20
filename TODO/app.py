from flask import Flask,render_template,request ,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy # this is for database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"  # this is for database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False  # this is for database
db=SQLAlchemy(app)  # this is for database

class ToDo(db.Model):
     sno=db.Column(db.Integer , primary_key=True)
     title=db.Column(db.String(200),nullable=False)
     desc=db.Column(db.String(500),nullable=False)
     date_created=db.Column(db.DateTime , default=datetime.utcnow)
     def __repr__(self):
        return f"{self.sno} - {self.title}"

     

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=ToDo(title=title, desc= desc) #creating instance oftodo
        db.session.add(todo)
        db.session.commit()
    allTodo = ToDo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>',methods=['GET', 'POST'])
def update(sno):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo=ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True )