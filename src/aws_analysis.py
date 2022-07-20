import boto3
import database

comprehend = boto3.client('comprehend')

def analyze(asin = None):
	amazon_reviews_needing_sent_analysis = database.get_aws_no_sentiment_analyzed_reviews(asin)
	amazon_reviews_needing_kp_analysis = database.get_aws_no_key_phrase_analyzed_reviews(asin)
	for review in amazon_reviews_needing_sent_analysis:
		# preform the machine learning on the reviews:
		# get the sentiment and key phrases from the text of the review
		sentiment = comprehend.detect_sentiment(Text = review[1][:5000], LanguageCode = 'en')
		# insert the sentiment and key phrases to the database
		database.insert_aws_sentiment(sentiment, review[0])

	for review in amazon_reviews_needing_kp_analysis:
		key_phrases = comprehend.detect_key_phrases(Text = review[1][:5000], LanguageCode = 'en')
		database.insert_aws_key_phrases(key_phrases, review[0])

