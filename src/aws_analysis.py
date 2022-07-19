from ssl import ALERT_DESCRIPTION_UNRECOGNIZED_NAME
import boto3
import database

comprehend = boto3.client('comprehend')

columns, amazon_reviews = database.get_reviews()

text_idx = columns.index('reviewText')
id_idx = columns.index('id')

sentiment_cols, prev_sentiments = database.get_aws_sentiments()
key_phrases_cols, prev_key_phrases = database.get_aws_key_phrases()

sentiment_review_id_idx = sentiment_cols.index('userReview')
key_phrases_review_id_idx = sentiment_cols.index('userReview')

for review in amazon_reviews:
	if review[id_idx] in [r[sentiment_review_id_idx] for r in prev_sentiments]:
		print("skipping review {}".format(review[id_idx]))
		continue
	if review[id_idx] in [r[key_phrases_review_id_idx] for r in prev_key_phrases]:
		print("skipping review {}".format(review[id_idx]))
		continue
	# preform the machine learning on the reviews:
	# get the sentiment and key phrases from the text of the review
	sentiment = comprehend.detect_sentiment(Text = review[text_idx][:5000], LanguageCode = 'en')
	key_phrases = comprehend.detect_key_phrases(Text = review[text_idx][:5000], LanguageCode = 'en')
	# insert the sentiment and key phrases to the database
	database.insert_aws_sentiment(sentiment, review[id_idx])
	database.insert_aws_key_phrases(key_phrases, review[id_idx])
