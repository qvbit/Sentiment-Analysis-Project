#!/usr/bin/env python

"""Clean comment text for easier parsing."""

from __future__ import print_function

import sys
import re
import string
import argparse
import json

__author__ = ""
__email__ = ""

# Some useful data.
_CONTRACTIONS = {
	"tis": "'tis",
	"aint": "ain't",
	"amnt": "amn't",
	"arent": "aren't",
	"cant": "can't",
	"couldve": "could've",
	"couldnt": "couldn't",
	"didnt": "didn't",
	"doesnt": "doesn't",
	"dont": "don't",
	"hadnt": "hadn't",
	"hasnt": "hasn't",
	"havent": "haven't",
	"hed": "he'd",
	"hell": "he'll",
	"hes": "he's",
	"howd": "how'd",
	"howll": "how'll",
	"hows": "how's",
	"id": "i'd",
	"ill": "i'll",
	"im": "i'm",
	"ive": "i've",
	"isnt": "isn't",
	"itd": "it'd",
	"itll": "it'll",
	"its": "it's",
	"mightnt": "mightn't",
	"mightve": "might've",
	"mustnt": "mustn't",
	"mustve": "must've",
	"neednt": "needn't",
	"oclock": "o'clock",
	"ol": "'ol",
	"oughtnt": "oughtn't",
	"shant": "shan't",
	"shed": "she'd",
	"shell": "she'll",
	"shes": "she's",
	"shouldve": "should've",
	"shouldnt": "shouldn't",
	"somebodys": "somebody's",
	"someones": "someone's",
	"somethings": "something's",
	"thatll": "that'll",
	"thats": "that's",
	"thatd": "that'd",
	"thered": "there'd",
	"therere": "there're",
	"theres": "there's",
	"theyd": "they'd",
	"theyll": "they'll",
	"theyre": "they're",
	"theyve": "they've",
	"wasnt": "wasn't",
	"wed": "we'd",
	"wedve": "wed've",
    	"well": "we'll",
    	"were": "we're",
    	"weve": "we've",
    	"werent": "weren't",
    	"whatd": "what'd",
    	"whatll": "what'll",
    	"whatre": "what're",
    	"whats": "what's",
    	"whatve": "what've",
    	"whens": "when's",
    	"whered": "where'd",
    	"wheres": "where's",
    	"whereve": "where've",
    	"whod": "who'd",
    	"whodve": "whod've",
    	"wholl": "who'll",
    	"whore": "who're",
    	"whos": "who's",
    	"whove": "who've",
    	"whyd": "why'd",
    	"whyre": "why're",
    	"whys": "why's",
    	"wont": "won't",
    	"wouldve": "would've",
    	"wouldnt": "wouldn't",
    	"yall": "y'all",
    	"youd": "you'd",
    	"youll": "you'll",
    	"youre": "you're",
    	"youve": "you've"
}

# You may need to write regular expressions.

def sanitize(text):
	"""Do parse the text in variable "text" according to the spec, and return
	a LIST containing FOUR strings 
	1. The parsed text.
	2. The unigrams
	3. The bigrams
	4. The trigrams
	"""
	#remove the punctuation at the beginning

	# YOUR CODE GOES BELOW:
	remove_tabs_newlines = text.replace('\n', ' ').replace('\t', ' ')
	remove_urls = re.sub('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', '', remove_tabs_newlines)

	lowercase = remove_urls.lower()
	text_arr = lowercase.split()

	#make punctuation its own character
	punc_text_arr = []
	end_punc = ['.', ',', '!', '?', ';', ':']
	for i in range(len(text_arr)):
		cur_text_elem = text_arr[i]
		text_elem = cur_text_elem[:]
		temp_text = re.sub("[^\w,.\?!;:]+", "", text_elem)

		b = []
		while(len(temp_text) > 0 and temp_text[-1] in end_punc):
			b.append(temp_text[-1])
			temp_text = temp_text[:-1]
		b.append(temp_text)
		if(len(b) > 1):
			b = b[::-1]
			b[0] = cur_text_elem[:-1 * len(b) + 1]
		if(len(b) == 1):
			b[0] = cur_text_elem
		punc_text_arr = punc_text_arr + b
		#if(len(temp_text) > 0 and temp_text[-1] in end_punc):
		#	cur_text_elem = re.sub("[^\w,.\?!;:\-']+", "", cur_text_elem)
		#elif(cur_text_elem == text_elem):
		#	punc_text_arr.append(cur_text_elem)
		#else:
		#	punc_text_arr.append(cur_text_elem)
	#print(punc_text_arr)
	#punc_text = re.sub("(( (,|.|!|\?|;|:) |[\w]| ))", '', punc_text)
	a = []
    	#remove non alphanumeric characters
    	#should we also remove quotes, ---, and parens?
	for i in range(len(punc_text_arr)):
		punc_elem = punc_text_arr[i]
		if(not(punc_elem in end_punc)):
			punc_elem = re.sub("[^\w,.\?!;:\-']+", "", punc_elem)
			a.append(punc_elem)
		else:
			a.append(punc_elem)
	punc_text_arr = a
	#revert the contractions
	contractions_keys = _CONTRACTIONS.keys()
	for i in range(len(punc_text_arr)):
		punc_elem = punc_text_arr[i]
		if(punc_elem in contractions_keys):
			punc_text_arr[i] = _CONTRACTIONS[punc_elem]
	#print(punc_text_arr
	parsed_text = ' '.join(punc_text_arr)
	#use the punc_text_arr to make unigrams, bigrams, and trigrams
	unigrams = ""
	for i in range(len(punc_text_arr)):
		elem = punc_text_arr[i]
		if(not(elem in end_punc)):
			unigrams = unigrams + elem + " "
	if(len(unigrams) > 0 and unigrams[-1] == " "):
		unigrams = unigrams[:-1]	
	
	bigrams = ""
	bigram_a, bigram_b = "", ""
	for i in range(len(punc_text_arr)):
		elem = punc_text_arr[i]
		if(elem in end_punc):
			bigram_a, bigram_b = "", ""
		elif(len(bigram_a) == 0 and len(bigram_b) == 0):
			bigram_a = elem
		elif(len(bigram_a) == 0):
			bigram_a = elem
			bigram_b = bigram_b + "_" + elem
			bigrams = bigrams + " " + bigram_b
			bigram_b = ""
		elif(len(bigram_b) == 0):
			bigram_b = elem
			bigram_a = bigram_a + "_" + elem
			bigrams = bigrams + " " + bigram_a
			bigram_a = ""	
	#if(len(bigram_b) > 0):
	#	bigrams = bigrams + " " + bigram_b
	if(len(bigrams) > 2):
    		bigrams = bigrams[1:]            

	trigrams = ""
	trigram_a, trigram_b, trigram_c = "", "", ""
	for i in range(len(punc_text_arr)):
		elem = punc_text_arr[i]
		if(elem in end_punc):
                	trigram_a, trigram_b, trigram_c = "", "", ""
		elif(len(trigram_a) == 0 and len(trigram_b) == 0 and len(trigram_c) == 0):
                	trigram_a = elem
		elif(len(trigram_b) == 0 and len(trigram_c) == 0):
			trigram_a = trigram_a + "_" + elem
			trigram_b = elem
		elif(len(trigram_c) == 0):
			trigram_c = elem
			trigram_b = trigram_b + "_" + elem
			trigram_a = trigram_a + "_" + elem
			trigrams = trigrams + " " + trigram_a
			trigram_a = ""
		elif(len(trigram_b) == 0):
			trigram_b = elem
			trigram_a = trigram_a + "_" + elem
			trigram_c = trigram_c + "_" + elem
			trigrams = trigrams + " " + trigram_c
			trigram_c = ""
		elif(len(trigram_a) == 0):
			trigram_a = elem
			trigram_c = trigram_c + "_" + elem
			trigram_b = trigram_b + "_" + elem
			trigrams = trigrams + " " + trigram_b
			trigram_b = ""
	#if(len(trigram_c) > 0):
	#	trigrams = trigrams + " " + trigram_c
	if(len(trigrams) > 2):
        	trigrams = trigrams[1:] 

	return [parsed_text, unigrams, bigrams, trigrams]


if __name__ == "__main__":
	# This is the Python main function.
	# You should be able to run
	# python cleantext.py <filename>
	# and this "main" function will open the file,
	# read it line by line, extract the proper value from the JSON,
	# pass to "sanitize" and print the result as a list.

	# YOUR CODE GOES BELOW.
	#filename = sys.argv[1]
	#how long is the file? if it is long, then we shouldn't be doing the whole thing at once because it will take too long and the buffer will fill up
	#text = ""
	#with open(filename) as f_read:
	#	text = f_read.readline()[:-1]  + " " #this is a fast way of immediately getting rid of the newline character
	#print(str(sanitize(text)))
	data = []
	#text = "I'm afr-ai*d twenty-three... can't explain myself, sir. Because I am not myself, you see?"
	#print(text)
	#print(str(sanitize(text)))
	#print(sanitize(text))
	with open("sample-comments.json") as json_data:
		for line in json_data:
			data.append(json.loads(line)['body']);
	for comments in data:
		print(str(sanitize(comments)))
	#print(str(sanitize(text)))
