# Python program to generate WordCloud
 
# importing all necessary modules
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
 
def generate_wordcloud(words, img_name):
	words = " ".join(words)
	stopwords = set(STOPWORDS)
	wordcloud = WordCloud(width = 800, height = 800,
					background_color ='white',
					stopwords = stopwords,
					min_font_size = 10).generate(words)
	
	# plot the WordCloud image                      
	plt.figure(figsize = (8, 8), facecolor = None)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.tight_layout(pad = 0)
	plt.savefig('static/' + img_name)


# generate_wordcloud(['hi', 'hi', 'hi', 'there', 'bye', 'asd', 'zxc', 'hi'], 'test.png')