from flask import Flask, render_template, url_for
from app import app

@app.route('/')
def index():
	return render_template('index.html')
