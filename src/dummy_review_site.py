from flask import Flask, render_template, request, url_for, flash, redirect
import database
import aws_analysis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'

product_ids = database.get_product_ids()

@app.route('/', methods=('GET', 'POST'))
def index():
	if request.method == 'POST':
		review = request.form['review']
		database.insert_new_review_text(review)
		return redirect(url_for('index'))
	return render_template('index.html')

@app.route('/review-insights', methods=('GET', 'POST'))
def review_insights():
	if request.method == 'POST':
		product_id = request.form['product_id']
		# preform the analysis on the product
		aws_analysis.analyze(product_id)
		
		# get all the reviews for the selected product		
		reviews = database.get_reviews(product_id)
		reviews_text = [r[1] for r in reviews]
		return render_template('review-insights.html', product_ids=product_ids, display_insights=True, reviews=reviews_text)
	return render_template('review-insights.html', product_ids=product_ids, display_insights=False)

app.run(port=80)