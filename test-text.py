# Run readability scores of ref captions

import csv
import readabilitymetrics
from math import ceil

def expand_word_count(text):
	text = text.lower()
	count = len(text.split())
	return (text + " ") * (ceil(100/count))

with open("ref-captions.csv", "r") as csvfile:
	reader = csv.reader(csvfile)
	refL = list(reader)

refL =  [j for i in refL for j in i]

common_med_wordsL, med_words_freq = readabilitymetrics.common_med_words(refL)
print(type(common_med_wordsL))
#print(refL)
refL10 = refL[:1]
for ref in refL10:
	print("---------")
	caption = ref
	caption = expand_word_count(caption)
	print("Ref caption: ", caption)
	readabilitymetrics.box_readability_metrics(caption)
	readabilitymetrics.matched_box(caption)
	readabilitymetrics.improved_metrics(common_med_wordsL, caption)
	
