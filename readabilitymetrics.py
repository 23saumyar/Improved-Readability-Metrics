# Readability Scores

# pip install py-readability-metrics
from readability import Readability
from nltk.tokenize import sent_tokenize, TweetTokenizer

import re
import spacy
from textstat.textstat import textstatistics,legacy_round
import textstat
import string 
import nltk
from nltk.stem.porter import PorterStemmer

nltk.download("punkt")


# Splits the text into sentences, using
# Spacy's sentence segmentation which can
# be found at https://spacy.io/usage/spacy-101
def break_sentences(text):
	nlp = spacy.load('en_core_web_sm')
	doc = nlp(text)
	return list(doc.sents)

# Returns Number of Words in the text
def word_count(text):
	sentences = break_sentences(text)
	words = 0
	for sentence in sentences:
		words += len([token for token in sentence])
	# return words
	return textstat.lexicon_count(text, removepunct=True)

# Returns the number of sentences in the text
def sentence_count(text):
	sentences = break_sentences(text)
	return len(sentences)

# Returns average sentence length
def avg_sentence_length(text):
	words = word_count(text)
	sentences = sentence_count(text)
	average_sentence_length = float(words) / float(sentences)
	return average_sentence_length



def count_word_syllables(word):
    """
    Simple syllable counting
    """

    word = word if type(word) is str else str(word)

    word = word.lower()

    if len(word) <= 3:
        return 1

    word = re.sub('(?:[^laeiouy]es|[^laeiouy]e)$', '', word) # removed ed|
    word = re.sub('^y', '', word)
    matches = re.findall('[aeiouy]{1,2}', word)
    return len(matches)


# Textstat is a python package, to calculate statistics from
# text to determine readability,
# complexity and grade level of a particular corpus.
# Package can be found at https://pypi.python.org/pypi/textstat
def syllables_count(text):
	syllables = 0
	tokenizer = TweetTokenizer()
	tokens = tokenizer.tokenize(text)
	
	for t in tokens:
		match = re.match('^[.,\/#!$%\'\^&\*;:{}=\-_`~()]$', t)	
		if not (match is not None):
			word_syllable_count = count_word_syllables(t)
			syllables += word_syllable_count
			#poly_syllable_count += 1 if word_syllable_count >= 3 else 0
	return syllables
	# return textstatistics().syllable_count(word)

# Returns the average number of syllables per
# word in the text
def avg_syllables_per_word(text):
	syllable = syllables_count(text)
	words = word_count(text)
	print("word count", words)
	print("num of syllables", syllable)
	ASPW = float(syllable) / float(words)
	return ASPW

# Return total Difficult Words in a text
def difficult_words(text):

	nlp = spacy.load('en_core_web_sm')
	doc = nlp(text)
	# Find all words in the text
	words = []
	sentences = break_sentences(text)
	for sentence in sentences:
		words += [str(token) for token in sentence]

	# difficult words are those with syllables >= 2
	# easy_word_set is provide by Textstat as
	# a list of common words
	diff_words_set = set()

	for word in words:
		syllable_count = syllables_count(word)
		if word not in nlp.Defaults.stop_words and syllable_count >= 3:
			diff_words_set.add(word)

	return len(diff_words_set)

# A word is polysyllablic if it has more than 3 syllables
# this functions returns the number of all such words
# present in the text
def poly_syllable_count(text):
	count = 0
	words = []
	sentences = break_sentences(text)
	for sentence in sentences:
		words += [token for token in sentence]


	for word in words:
		syllable_count = syllables_count(word)
		if syllable_count >= 3:
			count += 1
	return count


def flesch_reading_ease(text):
	"""
		Implements Flesch Formula:
		Reading Ease score = 206.835 - (1.015 × ASL) - (84.6 × ASW)
		Here,
		ASL = average sentence length (number of words
				divided by number of sentences)
		ASW = average word length in syllables (number of syllables
				divided by number of words)
	"""
	print(avg_sentence_length(text))
	print(avg_syllables_per_word(text))
	FRE = 206.835 - float(1.015 * avg_sentence_length(text)) -\
		float(84.6 * avg_syllables_per_word(text))
	return FRE 


def improved_flesch_reading_ease(commonMedL, text):
	# adjust text here
	# calculate new score
	print("in improved flesch")
	print(text)
	print(commonMedL)	
	cleaned_text = ""
	for word in text.split(" "):
		if word not in commonMedL and word[:-1] not in commonMedL:
			cleaned_text += word + " "
		elif "." in word:
			cleaned_text += ". "
	print("cleaned text") 
	print(cleaned_text)	
	return flesch_reading_ease(cleaned_text)


def gunning_fog(text):
	per_diff_words = (difficult_words(text) / word_count(text) * 100)
	grade = 0.4 * (avg_sentence_length(text) + per_diff_words)
	return grade


def smog_index(text):
	"""
		Implements SMOG Formula / Grading
		SMOG grading = 3 + ?polysyllable count.
		Here,
		polysyllable count = number of words of more
		than two syllables in a sample of 30 sentences.
	"""

	if sentence_count(text) >= 3:
		poly_syllab = poly_syllable_count(text)
		SMOG = (1.043 * (30*(poly_syllab / sentence_count(text)))**0.5) \
				+ 3.1291
		return legacy_round(SMOG, 1)
	else:
		return 0


def load_dale_chall():
    dale_chall_path = 'dale_chall_porterstem.txt'
    with open(dale_chall_path) as f:
        return set(line.strip() for line in f)

def dale_chall_complex_words(text, medWords):
	porter_stemmer = PorterStemmer()
	dale_chall_set = load_dale_chall()
	dale_chall_set.update(medWords)
	# print(dale_chall_set)
	count = 0
	cleaned_text = text.translate(str.maketrans('', '', string.punctuation))
	# print(cleaned_text.split(" "))
	for word in cleaned_text.split(" "):
		stem = porter_stemmer.stem(word.lower())
		if stem not in dale_chall_set and len(stem)>0:
			count += 1
	# print(count)
	return count




def dale_chall_readability_score(text, medWords):
	words_per_sent =  avg_sentence_length(text)
	num_dale_chall_complex = dale_chall_complex_words(text, medWords)
	percent_difficult_words = num_dale_chall_complex / word_count(text) *100
	raw_score = 0.1579 * percent_difficult_words + 0.0496 * words_per_sent
	adjusted_score = raw_score + 3.6365 \
		if percent_difficult_words > 5 \
        else raw_score
	return adjusted_score


def improved_dale_chall_readability_score(text, commonMedL):
	cleanedMedSet = set()
	for k in commonMedL:
		cleanedMedSet.add(k)
	return dale_chall_readability_score(text, cleanedMedSet)


def old_dale_chall_readability_score(text):
	"""
		Implements Dale Challe Formula:
		Raw score = 0.1579*(PDW) + 0.0496*(ASL) + 3.6365
		Here,
			PDW = Percentage of difficult words.
			ASL = Average sentence length
	"""
	words = word_count(text)
	# Number of words not termed as difficult words
	count = words - difficult_words(text)
	if words > 0:

		# Percentage of words not on difficult word list

		per = float(count) / float(words) * 100

	# diff_words stores percentage of difficult words
	diff_words = 100 - per

	raw_score = (0.1579 * diff_words) + \
				(0.0496 * avg_sentence_length(text))

	# If Percentage of Difficult Words is greater than 5 %, then;
	# Adjusted Score = Raw Score + 3.6365,
	# otherwise Adjusted Score = Raw Score

	if diff_words > 5:

		raw_score += 3.6365

	return raw_score 

def improved_flesch_reading_ease(commonMedL, text):
	# adjust text here
	# calculate new score
	print("in improved flesch")
	print(text)
	print(commonMedL)	
	cleaned_text = ""
	for word in text.split(" "):
		if word not in commonMedL and word[:-1] not in commonMedL:
			cleaned_text += word + " "
		elif "." in word:
			cleaned_text += ". "
	print("cleaned text") 
	print(cleaned_text)	
	return flesch_reading_ease(cleaned_text)



def common_med_words(allTextL):
	allText = " ".join(allTextL)
	allText = allText.replace(".","")
	allText = allText.replace(",","")

	nlp = spacy.load('en_core_web_sm')
	wordDict = dict()
	for word in allText.split():
		if word not in nlp.Defaults.stop_words:
			wordDict.setdefault(word,0)
			wordDict[word] += 1

	
	freqItems = wordDict.items()
	sortedFreq = sorted(freqItems, key=lambda item: item[1], reverse = True)
	
	return wordDict.keys(), sortedFreq



def box_readability_metrics(text):
	r = Readability(text)
	# print(r.statistics())
	# print(r._statistics.num_dale_chall_complex)
	# print("-------")
	# print("Box readability metrics ")
	# print("Flesch Kincaid ", r.flesch_kincaid())
	# print("Flesch ", r.flesch())
	# print("Gunning Fog ", r.gunning_fog())
	# print("Coleman Liau ", r.coleman_liau())
	# print("Ari ",r.ari())
	# print("Linsear Write ", r.linsear_write())
	# print("smog ", r.smog())
	# print("spache ", r.spache())
	# print("Dale Chall ", r.dale_chall())
	return r.dale_chall()

def matched_box(text):
	print("__________")
	print("Matched box metrics:")
	# print("Flesh ", flesch_reading_ease(text))
	# print("gunning fog ", gunning_fog(text))
	# print("smog index ",smog_index(text))
	print("dale chall ",dale_chall_readability_score(text, set()))




def improved_metrics(common_med_wordsL, text):
	# print("------ improved")
	# print(improved_flesch_reading_ease(common_med_wordsL, text))
	# print(improved_dale_chall_readability_score(text, common_med_wordsL))
	return improved_dale_chall_readability_score(text, common_med_wordsL)
