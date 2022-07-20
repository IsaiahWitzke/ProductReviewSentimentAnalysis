import sqlite3
import wordcloud_generator


def insert_aws_sentiment(data, review_id):
	conn = sqlite3.connect("reviews.db")

	# insert the values into the database
	sql = """
	INSERT INTO aws_sentiment(sentiment, sentimentScorePositive, sentimentScoreNegative, sentimentScoreNeutral, sentimentScoreMixed, userReview)
	VALUES(?, ?, ?, ?, ?, ?)
	"""
	cur = conn.cursor()
	values = (
		data.get('Sentiment'),
		data['SentimentScore']['Positive'],
		data['SentimentScore']['Negative'],
		data['SentimentScore']['Neutral'],
		data['SentimentScore']['Mixed'],
		review_id
	)
	cur.execute(sql, values)
	conn.commit()
	conn.close()

def insert_aws_key_phrases(data, review_id):
	conn = sqlite3.connect("reviews.db")

	sql = """
	INSERT INTO aws_key_phrases(text, score, beginOffset, endOffset, userReview)
	VALUES(?, ?, ?, ?, ?)
	"""
	cur = conn.cursor()
	for key_phrase_data in data.get('KeyPhrases'):
		values = (
			key_phrase_data.get('Text'),
			key_phrase_data.get('Score'),
			key_phrase_data.get('BeginOffset'),
			key_phrase_data.get('EndOffset'),
			review_id
		)
		cur.execute(sql, values)
	conn.commit()
	conn.close()

def insert_new_review_text(text):
	insert_reviews([{
			"asin": 123,
			"reviewText": text
		}])

def insert_reviews(data):
	conn = sqlite3.connect("reviews.db")

	# column names
	cur = conn.execute('select * from user_reviews')
	col_names = [description[0] for description in cur.description]

	for review in data:
		# insert the values into the database
		columns = ', '.join(col_names)
		placeholders = ', '.join('?' * len(col_names))
		sql = "INSERT INTO user_reviews({}) VALUES({})".format(columns, placeholders)
		cur = conn.cursor()
		values = []
		for c in col_names:
			if c == 'datetime': # datetime is the only column that has a different associated data key than the other columns
				values.append(review.get('unixReviewTime'))
			else:
				values.append(review.get(c))
		cur.execute(sql, tuple(values))
		conn.commit()

	conn.close()

def get_aws_sentiments(asin = None):
	conn = sqlite3.connect("reviews.db")
	if asin == None:
		rows = conn.execute("""
		SELECT id, sentiment, sentimentScorePositive, sentimentScoreNegative, sentimentScoreNeutral, sentimentScoreMixed, userReview
		FROM aws_sentiment
		""").fetchall()
	else:
		rows = conn.execute("""
		SELECT id, sentiment, sentimentScorePositive, sentimentScoreNegative, sentimentScoreNeutral, sentimentScoreMixed, userReview
		FROM aws_sentiment as2 join user_reviews ur on as.userReview = ur.id where ur.asin = ?;
		""", (asin,)).fetchall()

	conn.close()
	return rows

def get_aws_key_phrases(asin = None):
	conn = sqlite3.connect("reviews.db")
	if asin == None:
		rows = conn.execute("SELECT akp.id, akp.\"text\", akp.score ur.id from aws_key_phrases akp inner join user_reviews ur on ur.id = akp.userReview where ur.asin = ?;", (asin,)).fetchall()
	else:
		rows = conn.execute("SELECT id, text, \"text\" score FROM aws_key_phrases").fetchall()
	conn.close()
	return rows

def get_non_analyzed_reviews(asin = None):
	conn = sqlite3.connect("reviews.db")
	sentiments_review_ids = set([s[6] for s in get_aws_sentiments()])
	reviews = [r for r in get_reviews(asin) if not r[0] in sentiments_review_ids]
	return reviews

def get_reviews(asin = None):
	conn = sqlite3.connect("reviews.db")
	if asin == None:
		rows = conn.execute("SELECT id, reviewText FROM user_reviews").fetchall()
	else:
		rows = conn.execute("SELECT id, reviewText FROM user_reviews WHERE asin = ?", (asin,)).fetchall()
	conn.close()
	return rows

def get_product_ids():
	conn = sqlite3.connect("reviews.db")
	cur = conn.execute("SELECT DISTINCT asin from user_reviews ur ORDER BY asin ASC;")
	rows = [row[0] for row in cur.fetchall()]
	conn.close()
	return rows

def get_aws_insights(asin):
	key_phrases = get_aws_key_phrases(asin)
	sentiments = get_aws_sentiments(asin)
	reviews = get_reviews(asin)

	reviews_joined = []
	

	return {
		'reviews': 
		'wordcloud' : wordcloud_generator.generate_wordcloud(key_phrases)
	}