from activmatesApp import db, bcrypt
from activmatesApp.models import User, UserTypes, Profile, ActivityType, Activity


db.drop_all()

db.create_all()


#insert myself as admin user
hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
admin = User(username='frannie123', email='frances.ziesemer@gmail.com', password=hashed_password, user_type=UserTypes.Admin)
db.session.add(admin)


#insert test user 
user1 = User(username='jonas123', email='jonas@demo.com', password=hashed_password)
user2 = User(username='ted123', email='ted@demo.com', password=hashed_password)

db.session.add(user1)
db.session.add(user2)

#insert profiles for users 
profile_jonas = Profile(first_name='Jonas', last_name='Bischof', phone_number='012345678', twitter='joni123', facebook='joni123', user_id=2)
profile_ted = Profile(first_name='Ted', last_name='Ziesemer', phone_number='012345678', twitter='ted123', facebook='ted123', user_id=3)

db.session.add(profile_jonas)
db.session.add(profile_ted)

#insert activity types 
running = ActivityType(number=1, name='Running')
ping_pong = ActivityType(number=2, name='Ping Pong')
walking = ActivityType(number=3, name='Walking')
swimming = ActivityType(number=4, name='Swimming')

db.session.add(running)
db.session.add(ping_pong)
db.session.add(walking)
db.session.add(swimming)

db.session.commit()