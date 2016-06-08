from flask import Flask, render_template, request, redirect, session, flash

from connection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'my_secret_key'
mydb = MySQLConnector(app, "classespy2")

@app.route('/')
def index():
    query = "SELECT * FROM users"
    values = {}
    users = mydb.query_db(query,values)
    query2 = "SELECT * FROM classes"
    values2 = {}
    classes = mydb.query_db(query2,values2)
    print (users)
    print (classes)
    return render_template('index.html', classes = classes, users = users)

@app.route('/users', methods = ['POST'])
def createusers():
    print (request.form)
    query = "Insert into users (first_name, last_name, created_at, updated_at) values (:first_name, :last_name, NOW(), NOW())"
    values = {
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
    }
    mydb.query_db(query,values)
    return redirect('/')

@app.route('/classes', methods = ['POST'])
def createclasses():
    print (request.form)
    query = "Insert into classes (title, description, created_at, updated_at) values (:title, :description, NOW(), NOW())"
    values = {
        "title":request.form['title'],
        "description":request.form['description'],
    }
    mydb.query_db(query,values)
    return redirect('/')

@app.route('/users_have_classes', methods = ['POST'])
def createuserhasclass():
    print (request.form)
    query = "Insert into users_has_classes (user_id, class_id, level, created_at, updated_at) values (:user_id, :class_id,:level, NOW(), NOW())"
    values = {
        "user_id":request.form['user_id'],
        "class_id":request.form['course_id'],
        "level":request.form['level']
    }
    mydb.query_db(query,values)
    return redirect('/classes')

@app.route('/classes')
def classes_index():
    query = "select * from classes"
    values = {}
    classes = mydb.query_db(query,values)
    return render_template('courses.html', courses = classes)

@app.route('/courses/<int:id>')
def show_class(id):
    print (id)
    query = "SELECT users.first_name FROM users_has_classes LEFT JOIN users ON users.id = users_has_classes.user_id where users_has_classes.class_id = :id"
    values = {
        "id":id
    }
    classes = mydb.query_db(query,values)
    print (classes)
    return render_template('course.html', classes = classes)
if __name__ == '__main__':
  app.run(debug = True)
