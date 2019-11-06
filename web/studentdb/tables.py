from flask_table import Table, Col

class Results(Table):
    id = Col('Id', show=False)
    name = Col('Name')
    rewards_redeemed = Col('Number of Redeemed Rewards')
    teacher = Col('Teacher')
    volunteer = Col('Volunteer')
