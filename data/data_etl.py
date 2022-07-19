import pandas as pd
import gzip
import json
import database

def parse(path):
  return [json.loads(l) for l in gzip.open(path, 'rb')]

# load the data from the downloaded zip file of amazon reviews
data = parse('Video_Games_5.json.gz')

# push the data into the database
# for testing, we will only use 100 reviews
database.insert_reviews(data[:100])
