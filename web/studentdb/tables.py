from flask_table import Table, Col, LinkCol

class Students(Table):
    id = Col('Id', show=False)
    name = Col('Name')
    points_redeemed = Col('Points Redeemed')
    teacher = Col('Teacher')
    volunteer = Col('Volunteer')
    current_points = Col('Current Points')
    redeem = LinkCol('Redeem', 'redeem', url_kwargs=dict(id='id'))
    add_points = LinkCol('Add Points', 'add', url_kwargs=dict(id='id'))
