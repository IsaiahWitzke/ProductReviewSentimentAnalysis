from pydoc import cli
import database
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("azure_language_key")
endpoint = os.getenv("azure_endpoint")

# Authenticate the client using your key and endpoint 
def authenticate_client():
	ta_credential = AzureKeyCredential(key)
	text_analytics_client = TextAnalyticsClient(
			endpoint=endpoint, 
			credential=ta_credential)
	return text_analytics_client

client = authenticate_client()

def sentiment_analysis_with_opinion_mining(client, review_text):

	documents = [ review_text ]
	result = client.analyze_sentiment(documents, show_opinion_mining=True)
	doc_result = [doc for doc in result if not doc.is_error][0]

	res_sentiment = {
		'sentiment': doc_result.sentiment,
		'sentimentScorePositive': doc_result.confidence_scores.positive,
		'sentimentScoreNegative': doc_result.confidence_scores.negative,
		'sentimentScoreNeutral': doc_result.confidence_scores.neutral
	}

	mined_opinions = []
	for s in doc_result.sentences:
		for mined_opinion in s.mined_opinions:
			mined_opinions.append(mined_opinion)

	res_mined_opinions = [{
		'text': op.target.text,
		'sentiment': op.target.sentiment,
		'sentimentScorePositive': op.target.confidence_scores.positive,
		'sentimentScoreNegative': op.target.confidence_scores.negative,
		'sentimentScoreNeutral': op.target.confidence_scores.neutral
	} for op in mined_opinions]

	return res_sentiment, res_mined_opinions
		  
def key_phrase_extraction(client, review_text):

	documents = [review_text]
	response = client.extract_key_phrases(documents = documents)[0]
	result = [{
		"text": p
	} for p in response.key_phrases]

	return result

def analyze(asin = None):
	amazon_reviews_needing_sent_analysis = database.get_azure_no_sentiment_analyzed_reviews(asin)
	amazon_reviews_needing_kp_analysis = database.get_azure_no_key_phrase_analyzed_reviews(asin)
	for review in amazon_reviews_needing_sent_analysis:
		# preform the machine learning on the reviews:
		# get the sentiment and key phrases from the text of the review
		sentiment, opinions_mined = sentiment_analysis_with_opinion_mining(client, review[1][:5000])
		# insert the sentiment and key phrases to the database
		database.insert_azure_sentiment(sentiment, review[0])
		for op in opinions_mined:
			database.insert_azure_mined_opinion(op, review[0])

	for review in amazon_reviews_needing_kp_analysis:
		key_phrases = key_phrase_extraction(client, review[1])
		for kp in key_phrases:
			database.insert_azure_key_phrase(kp, review[0])
