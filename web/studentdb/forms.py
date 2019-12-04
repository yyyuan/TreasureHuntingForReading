# forms.py

from wtforms import Form, StringField, SelectField

class StudentSearchForm(Form):
    choices = [('Student', 'Student'),
               ('Teacher', 'Teacher'),
               ('Volunteer', 'Volunteer')]
    select = SelectField('Search for students:', choices=choices)
    search = StringField('')

class StudentForm(Form):
    teacher_names = [('Teacher 1', 'Teacher 1'),
                   ('Teacher 2', 'Teacher 2'),
                   ('Teacher 3', 'Teacher 3')
                   ]
    volunteer_names = [('Volunteer 1', 'Volunteer 1'),
                   ('Volunteer 2', 'Volunteer 2'),
                   ('Volunteer 3', 'Volunteer 3')
                   ]
    name = StringField('Name')
    current_points = StringField('Current Points')
    points_redeemed = StringField('Points Redeemed')
    teacher = SelectField('Teacher', choices=teacher_names)
    volunteer = SelectField('Volunteer', choices=volunteer_names)
