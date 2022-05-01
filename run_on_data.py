# Run metrics on data
import csv
import readabilitymetrics
from math import ceil

def expand_word_count(text):
	text = text.lower()
	count = len(text.split())
	return (text + " ") * (ceil(100/count))

with open("r3_results_parsed.csv", "r") as csvfile:
	reader = csv.reader(csvfile)
	refL = list(reader)
print(refL[0])

captionsOnly = []
for row in refL:
    captionsOnly.append(row[1])
# print(captionsOnly)

common_med_wordsL, med_words_freq = readabilitymetrics.common_med_words(captionsOnly)
# print(common_med_wordsL)

metricsCSV = []

for row in refL:
    caption = row[1]
    expanded_caption = expand_word_count(caption)
    box_dale_chall = readabilitymetrics.box_readability_metrics(expanded_caption).score
    improved_dale_chall = readabilitymetrics.improved_metrics(common_med_wordsL, expanded_caption)
    newRow = row
    newRow.append(box_dale_chall)
    newRow.append(improved_dale_chall)
    metricsCSV.append(newRow)
    print(row[0])

print(len(metricsCSV))
print(metricsCSV)
print(type(metricsCSV))
with open("r3_metrics_captions.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(metricsCSV)

# #print(refL)
# refL10 = refL[:1]
# for ref in refL10:
# 	print("---------")
# 	caption = ref
# 	caption = expand_word_count(caption)
# 	print("Ref caption: ", caption)
# 	readabilitymetrics.box_readability_metrics(caption)
# 	readabilitymetrics.matched_box(caption)
# 	readabilitymetrics.improved_metrics(common_med_wordsL, caption)
	
