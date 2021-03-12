class Config:
    app.config.from_object("activmatesApp.default_settings")


app.config.from_envvar("APPLICATIONSETTNGS")
app.config["SQLALCHEMY_ECHO"] = False


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True


app.config["MAIL_USERNAME"] = email_user
app.config["MAIL_PASSWORD"] = email_password