from flask_table import Table, Col, LinkCol

class Students(Table):
    id = Col('Id', show=False)
    name = Col('Name')
    points_redeemed = Col('Points Redeemed')
    teacher = Col('Teacher')
    volunteer = Col('Volunteer')
    current_points = Col('Current Points')
    redeem = LinkCol('Redeem', 'redeem', url_kwargs=dict(id='id'))
    # add_points = LinkCol('Add Points', 'add', url_kwargs=dict(id='id'))
    update = LinkCol('Update Points', 'update_points', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))
