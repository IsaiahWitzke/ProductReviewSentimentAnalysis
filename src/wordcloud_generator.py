# Python program to generate WordCloud
 
# importing all necessary modules
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
 
def generate_wordcloud(words, img_name):
	if len(words) == 0:
		words = ['placeholder']
	word_cloud_dict=Counter([w.strip().lower() for w in words])
	stopwords = set(STOPWORDS)
	wordcloud = WordCloud(width = 800, height = 800,
					background_color ='white',
					stopwords = stopwords,
					min_font_size = 10,
					normalize_plurals=False).generate_from_frequencies(word_cloud_dict)
	
	# plot the WordCloud image                      
	plt.figure(figsize = (8, 8), facecolor = None)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.tight_layout(pad = 0)
	plt.savefig('static/' + img_name)
	return img_name


# generate_wordcloud(['hi', 'hi', 'hi', 'there', 'bye', 'asd', 'zxc', 'hi'], 'test.png')