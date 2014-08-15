from flask import render_template, request
from SvsR import app

@app.route('/')
def index():
	return render_template('index.html')
