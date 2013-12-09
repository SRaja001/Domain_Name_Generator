import requests
import re
from flask import Flask, request, render_template, flash
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		keywords = [request.form["key1"], 
					request.form["key2"], 
					request.form["key3"]
					]
		clean_keywords = clean(keywords)
		return render_template("index.html")
	return render_template("index.html")

def clean(words):
	"""Clean the keywords.  Remove empty strings, and remove numbers 
	and special characters from individual keywords"""
	clean_words = []
	p = re.compile("\W") #regex for any non alpha-numeric value
	a = re.compile("\d") #regex for for any digit
	for word in words:
		if word != "":
			b = p.sub("", word)
			c = a.sub("", b)
			clean_words.append(c)
	print "input", words
	print "output", clean_words
	return clean_words

def synonym_lookup(words):
	""" Look up synonyms for words
	Input: List of words
	Output:  

	"""

def domain_lookup(domain):
	"""" Use domai.nr api for domain lookup """"
	URL = "https://domai.nr/api/json/search?q="

	



if __name__ == "__main__":
	app.debug = True
	app.run()