from flask import Flask, render_template, request, url_for, flash, redirect
from database import insert_new_review_text

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'

@app.route('/', methods=('GET', 'POST'))
def index():
	if request.method == 'POST':
		review = request.form['review']
		print(review)
		insert_new_review_text(review)
		return redirect(url_for('index'))
	return render_template('index.html')

app.run(port=80)