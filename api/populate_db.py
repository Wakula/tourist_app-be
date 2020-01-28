from config import DebugConfig
from app import create_app

app = create_app(DebugConfig)
db = app.db

User = app.models.User
Trip = app.models.Trip
Point = app.models.Point
Role = app.models.Role
Eq = app.models.Equipment

users = User.query
trips = Trip.query
points = Point.query
roles = Role.query
eqs = Eq.query

def create_users(from_number, amount):
    '''to create 2 new users:\n
    create_users(0, 2)\n
    function doesnt check for right naming, 
    therefore beware to choose right <from_number>'''
    created_users = []
    for i in range(from_number, from_number + amount):
        user = User.create_user(name=f'username-{i}', email=f'email-{i}@mail.com',
        	password='password321',surname=f'surname-{i}')
        user.activate_user()
        created_users.append(user)
    return created_users

# Doenst work for now
# def create_trips(from_number, amount, admin=users[0]):
#     created_trips = []
#     for i in range(from_number, from_number + amount):
#         trip = Trip.create_trip(
#             name=f'trip-{i}',
#             description="desc",
#             start_date="2014-12-22T03:12:58.019077+00:00",
#             end_date="2015-12-22T03:12:58.019077+00:00",
#             admin=admin,
#         )
#         created_trips.append(trip)
#     return created_trips


# to create 5 new users
# create_users(0, 5)

# user = User.query.first()
# trip = Trip.query.first()

