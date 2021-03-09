<<<<<<< HEAD
##ActivMates - an app to connect through sports
=======
## ActivMates - an app to connect through sports 
>>>>>>> f8557318927d335bb73cc839d7fedb457a92bd84

this app is a project completed with FrauenLoop end-2-end web developlemt cohort Jan-March 2021

The task is to build a geolocation based CRUD application. My idea is a tinder-like application to connect with others in your areas to do sports. For example running or table tennis. 

Canva [Design/ Prototype and Style Guide](https://www.canva.com/design/DAEVXlzmXRM/Rrg_pX-BC3oKyAjXxPYjkQ/view?utm_content=DAEVXlzmXRM&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink) | 
Lucid Chart - [User Flow Diagram](https://lucid.app/lucidchart/invitations/accept/d87177c9-e05c-4a50-8a4d-d8f033d47cc6) | 
Lucid Chart - [Database ER Diagram ](https://lucid.app/lucidchart/invitations/accept/17227268-9646-4fd9-b794-4b4613432e88)

##### Start the app locally

1. Activate virtual environment:
   `. venv/bin/activate`
2. Set evn variable pointing to local settings file:
   `export APPLICATIONSETTNGS=local_settings.py`
3. Run the Flask app:
   `python run.py`

###### What did I learn?

- local settings and secure password / API key storage
-

#### Current status of project as of 08.03.2021
- not deployed i.e. still in production 
- The backend component of this application is almost complete. 
  -  Models and most routes are finalised. 
  -  API functionality between db and googleMaps API is complete.
  -  routes and connection to all pages and templates is complete. 
###### To do:
- FRONT END - I have not started working on the front end and UI component of this app yet. Until now all work has been focused on ensuring the backend and database functionality is completed 
- NEXT STEPS: integrate react onto the application and start to build efficient front end compontents

###### Skills Demonstrated
- build of python Flask application 
- SQL Alchemy - construction of Models, how to handle data from database tables 
- WTForms - construction of forms to receive data to then input into database, user validation   
- API routing 
- API use - google maps 
- Spatialite and the use of SQL Geoalchemy to to store geometry points and manipulate data
- 


###### Major key learning points 
- local settings and secure password / API key storage 
- backend - models, SQL and database 


###### Challenges and reflections 
- this is the first time working with databases. Initially, I found it challenging to grasp the concepts of retreiving data from form interfaces and connecting the information with routes, and databases. With patience, I was able to implement user registration, profile creation and post creation - with interconnectivity fucntioning well. 
- it was very interesting to use the google maps API, autocorrect to store location inputs. This feature also improves the user experience in making it easier and quicker to find the users address. Furthermore the next step of displaying data from my tables onto a googleMaps interface was also a great learning curve. And very cool to see the results. 
