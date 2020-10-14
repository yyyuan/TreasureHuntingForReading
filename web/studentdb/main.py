# main.py

from app import app
from db_setup import init_db, db
from forms import StudentSearchForm, StudentForm
from flask import flash, render_template, request, redirect
from models import Student
from tables import Students
from flask import jsonify

init_db()

# import serial for serial communication with Arduino
import serial
import time
import threading
import sys

## may need to modify based on the actual port info - uncomment when have the actual arduino
## ser = serial.Serial("/dev/cu.usbserial-DA00VDIZ",9600)

@app.route("/update", methods = ['GET'])
def update_points():
    ## uncomment the following when actually have the serial ports
    ## total_points = ser.readline().decode('utf-8')
    ## the dummy test
    total_points = '25\r\n'
    total_points = total_points.replace('\n', '')
    total_points = total_points.replace('\r', '')
    print(total_points, file=sys.stdout)
    return jsonify(points = [total_points])


@app.route('/', methods=['GET', 'POST'])
def index():
    # search = StudentSearchForm(request.form)
    # if request.method == 'POST':
    # return search_results(search)
    all_students = []
    qry = db.session.query(Student)
    students = qry.all()
    for student in students:
        all_students.append(student)
    std_table = Students(all_students)
    std_table.border = True
    return render_template('index.html', table=std_table)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    #if search.data['search'] != '':
    qry = db.session.query(Student)
    students = qry.all()
    #identify students matching the search string
    if search.data['search'] == '':
        for student in students:
            results.append(student)
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)
    else:
        for student in students:
            if search.data['select'] == 'Student' and student.name == search_string:
                results.append(student)
            elif search.data['select'] == 'Teacher' and student.teacher == search_string:
                results.append(student)
            elif search.data['select'] == 'Volunteer' and student.volunteer == search_string:
                results.append(student)
    if results == []:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)

@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    #Add a new student
    form = StudentForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the album
        student = Student()
        save_changes(student, form, new=True)
        flash('Student successfully added to database!')
        return redirect('/')

    return render_template('new_student.html', form=form)

def save_changes(student, form, new=False):
    #Save indicated changes to the database

    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object

    student.name = form.name.data
    student.current_points = form.current_points.data
    student.points_redeemed = form.points_redeemed.data
    student.teacher = form.teacher.data
    student.volunteer = form.volunteer.data

    if new:
        # Add the new album to the database
        db.session.add(student)

    # commit the data to the database
    db.session.commit()

@app.route('/redeem/<int:id>', methods=['GET', 'POST'])
def redeem(id):
    qry = db.session.query(Student).filter(Student.id==id)
    student = qry.first()
    if student:
        if student.current_points < 5:
            return 'Cannot redeem reward for this student'
        else:
            student.current_points -= 5
            student.points_redeemed += 5
            db.session.commit()
        return redirect('/')
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/add/<int:id>', methods=['GET', 'POST'])
def add(id):
    qry = db.session.query(Student).filter(Student.id==id)
    student = qry.first()
    if student:
        student.current_points += 5
        db.session.commit()
        return redirect('/')
    else:
        return 'Error loading #{id}'.format(id=id)

if __name__ == '__main__':
    app.debug = True
    app.run()
