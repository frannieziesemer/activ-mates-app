set title for loop 

create forms.py and install wtforms 
- create Classes for the forms 
- add secret key 
`app.config['SECRET_KEY'] = '36678eaa6a847166122011a8472d4f21'`
    - to do this in the terminal
    `$ python3
     $ import secrets
     $ secrets.token_hex(16) `
- import forms into views.py
- create instance of form in the route function so the form can be passed into a template
- build form html in template 
`<form method="POST" action="">` action means that when the form is submitted nothing will happend we can set it to route to somewhere else when submitted *maybe i can route to profile creation when the  righister form is conpleted'
- add {{ form.hidden_tag()}} -- this has something to do with the secret key + security adds a csrtoken
- then add form fields + classes for css - the for shows an error on sumbit at this point 
- add a list of allowed methods - add `methods=['GET', 'POST'] `to the route function 
- the error notifications dont work at this point so we want to do a check that we have the post data 
- validate on submit method ` if.registrationForm.validate_on_submit()....` + flash message
-import flash `flash(f'message here')`
- to allow flash messages to show any where create a with block 
`{% with messages = get_flashed_messages(with_categories_true) %}
{% if messages %}
{% for category, message in messages %}
    <div class="alert alert-{{category}}"> 
        {{message}}
    </div>
    {% endfor %}
{% endif %}
{% endwith %}`
 - category allows class to be inserted and message is the message 



