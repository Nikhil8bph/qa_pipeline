import os
#import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template,url_for
from werkzeug.utils import secure_filename
from qa_pipeline import elastic_search
import pandas as pd
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the files part
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
		files = request.files.getlist('files[]')
		for file in files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash('File(s) successfully uploaded')
		return redirect('/')

@app.route('/perform', methods=['POST','GET'])
def perform_nlp():
	if request.method=="POST":
		text_to_search = request.form.getlist('text_to_search')[0]
		df = elastic_search(text_to_search)
		return render_template('performer.html',tables=[df.to_html(classes='data')], titles=df.columns.values)
	return render_template('performer.html',tables="", titles="")

if __name__ == "__main__":
    app.run()