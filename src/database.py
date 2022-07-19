import sqlite3


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

def get_aws_sentiments():
	conn = sqlite3.connect("reviews.db")
	cur = conn.execute("SELECT * FROM aws_sentiment")
	rows = cur.fetchall()
	cols = [description[0] for description in cur.description]
	conn.close()
	return cols, rows

def get_aws_key_phrases():
	conn = sqlite3.connect("reviews.db")
	cur = conn.execute("SELECT * FROM aws_key_phrases")
	rows = cur.fetchall()
	cols = [description[0] for description in cur.description]
	conn.close()
	return cols, rows

def get_reviews():
	conn = sqlite3.connect("reviews.db")
	cur = conn.execute("SELECT * FROM user_reviews")
	rows = cur.fetchall()
	cols = [description[0] for description in cur.description]
	conn.close()
	return cols, rows
