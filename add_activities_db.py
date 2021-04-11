from activmatesApp import db, bcrypt, create_app
from activmatesApp.models import User, UserTypes, Profile, ActivityType, Activity


app = create_app()
app.app_context().push()

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

activity_ted = Activity(title="Running Training", 
            description="I am an intermediate runner looking for someone to train with on Wednesdays",
            address="Savinyplatz, Berlin, Germany",
            location='0101000020E6100000FD0BA947BF404A40571696896CA52A40',
            activity_type_id=1,
            profile_id=2,
            image_file="default_activity.jpg"
        )

db.session.add(activity_ted)




db.session.commit()