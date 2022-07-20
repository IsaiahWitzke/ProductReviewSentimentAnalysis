from flask import Flask, render_template, request, url_for, flash, redirect
import database
import aws_analysis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'


@app.route('/delete-reviews')
def delete_reviews():
	database.delete_reviews(123)
	return redirect(url_for('index'))
	
@app.route('/', methods=('GET', 'POST'))
def index():
	if request.method == 'POST':
		review = request.form['review']
		database.insert_new_review_text(review)
		return redirect(url_for('index'))
	return render_template('index.html')

@app.route('/review-insights', methods=('GET', 'POST'))
def review_insights():
	product_ids = database.get_product_ids()
	if request.method == 'POST':
		product_id = request.form['product_id']
		# preform the analysis on the product
		aws_analysis.analyze(product_id)
		
		# get the insights
		review_insights = database.get_aws_insights(product_id)
		print(review_insights)
		return render_template('review-insights.html', product_ids=product_ids, display_insights=True, review_insights=review_insights)
	return render_template('review-insights.html', product_ids=product_ids, display_insights=False)

app.run(port=80)