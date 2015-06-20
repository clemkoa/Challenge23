# -*- coding: utf-8 -*-
import csv
import string
import matplotlib.pyplot as plt
import re
import math

def plotPoints(authorList, trainingList):
	x = []
	y = []
	i = 0
	for author in authorList.keys():
		if i > 0 and i < 3:
			for element in trainingList:
				if element[1] == author:
					x.append(len(element[0]))
	#				x.append(getAverageWordLengthInSentence(element[0]))
	#				x.append(getPunctuationNumber(element[0]))
					y.append(getUppercaseNumber(element[0]))
			plt.plot(x,y,'o')
			x = []
			y = []
		i += 1
	plt.show()		
	return

def plotpoints2(authorList, testList, wordMatrix, numberedWords, weightedWords):
	x = []
	y = []
	y1 = []
	y2 = []
	y3 = []
	i = 0
	first = True
	for author in authorList:
		if i < 3 and i >0:
			print author
			print i
			for element in testList:
				if element[1] == author:
					sentence = element[0]
					sentence = removePunctuation(sentence)
					y.append(len(element[0]))
					x.append(calculerProbaTousAuteurs(sentence, authorList, wordMatrix, weightedWords))
					y1.append(getAverageWordLengthInSentence(element[0]))
					y2.append(getPunctuationNumber(element[0]))
					y3.append(getUppercaseNumber(element[0]))
			if first:
				plt.subplot(421)
				plt.plot(x, y, 'o')
				plt.subplot(422)
				plt.plot(x, y1, 'o')
				plt.subplot(425)
				plt.plot(x, y2, 'o')
				plt.subplot(426)
				plt.plot(x, y3, 'o')
				first = False
			else:
				plt.subplot(423)
				plt.plot(x, y, 'o')
				plt.subplot(424)
				plt.plot(x, y1, 'o')
				plt.subplot(427)
				plt.plot(x, y2, 'o')
				plt.subplot(428)
				plt.plot(x, y3, 'o')
			x = []
			y = []
			y1 = []
			y2 = []
			y3 = []
		i += 1
	plt.show()
	return

def calculerProbaAuteur(sentence, i, listeMatrices, tfidfWeightedWords):
	res = 0.0
	words = getWordsFromSentence(sentence)
	for j in range(0, len(words)-1):
		lowercasedI = words[j].lower()
		lowercasedNextI = words[j+1].lower()
		if lowercasedI in numberedWords[i].keys() and lowercasedNextI in listeMatrices[i][numberedWords[i][lowercasedI]].keys() and lowercasedI in tfidfWeightedWords[i].keys():
			res += listeMatrices[i][numberedWords[i][lowercasedI]][lowercasedNextI]*tfidfWeightedWords[i][lowercasedI]
	return res

def calculerProbaTousAuteurs(sentence, authorList, reverseAuthorList, wordMatrix, tfidfWeightedWords):
	res = {}
	for i in range(0, len(authorList.keys())):
		res[i] = calculerProbaAuteur(sentence, i, wordMatrix, tfidfWeightedWords)
	max = 0.0
	maxIndex = 0
	for key in res.keys():
		if res[key] > max:
			maxIndex = key
			max = res[key]
	return reverseAuthorList[maxIndex]

def getAlgorithmScore(authorList, wordMatrix, tfidfWeightedWords, reverseAuthorList):
	csvfile = open('test_sample.csv', 'rb')
	reader = csv.reader(csvfile, delimiter=';')
	trainingList = list(reader)

	w = open('result.csv', mode='w')
	w.write('Id;Author\n')

	for element in trainingList:
		number = element[0]
		sentence = element[1]
		sentence = removePunctuation(sentence)
		res = calculerProbaTousAuteurs(sentence, authorList, reverseAuthorList, wordMatrix, tfidfWeightedWords)
		w.write(str(number) + ';' + res + '\n')
#		print number
	print 'done'
	return

def getWordList(authorList, trainingList):
	wordList = [{} for i in range(0, len(authorList))]
	
	for element in trainingList:
		sentence = element[0]
		author = element[1]
		if author != 'Author':
			words = getWordsFromSentence(sentence)
			for word in words:
				if word not in wordList[authorList[author]].keys():
					wordList[authorList[author]][word] = 1
				else:
					wordList[authorList[author]][word] += 1
	return wordList

def removeIsolatedWords(i, wordList):
	for dico in wordList:
		for key in dico.keys():
			if dico[key] < i:
				del dico[key]
	return wordList

def getAverageWordLengthInSentence(sentence):
	words = getWordsFromSentence(sentence)
	sum = 0
	total = 0
	for word in words:
		total += 1
		sum += len(word)
	if total != 0:
		return sum*1.0/total
	return

def getAverageLengthWordByAuthor(authorList, wordList):
	lengthList = {}
	
	for i in range(0, len(authorList)):
		sum = 0
		total = 0
		for key in wordList[i].keys():
			sum += len(key)*wordList[i][key]
			total += wordList[i][key]
		if total != 0:
			lengthList[i] = sum*1.0/total
	return lengthList

def getLengthSentenceByAuthor(authorList, trainingList):
	lengthList = [[] for i in range(0, len(authorList))]
	for element in trainingList:
		sentence = element[0]
		author = element[1]
		if author != 'Author':
			length = len(sentence)
			lengthList[authorList[author]].append(length)
	return lengthList

def getAverageLengthByAuthor(sentenceLengthList, authorList):
	lengthList = {}

	for i in range(0, len(sentenceLengthList)):
		total = 0
		sum = 0
		for length in sentenceLengthList[i]:
			sum += length
			total += 1
		if total != 0:
			lengthList[i] = sum*1.0/total
	return lengthList


def buildAuthorList(trainingList):
	authorList = {}
	authorNumber = 0
	for element in trainingList:
		if element[1] not in authorList and element[1] != 'Author': #histoire d'enlever l'auteur Author
			authorList[element[1]] = authorNumber
			authorNumber += 1
	return authorList

def buildReversedAuthorList(authorList):
	reverseAuthorList = {}
	for key in authorList.keys():
		reverseAuthorList[authorList[key]] = key
	return reverseAuthorList
	
def removePunctuation(sentence):
	sentence = string.replace(sentence, ',','')
	sentence = string.replace(sentence, ';','')
	sentence = string.replace(sentence, '?','')
	sentence = string.replace(sentence, '!','')
	sentence = string.replace(sentence, '.','')
	sentence = string.replace(sentence, '[','')
	sentence = string.replace(sentence, ']','')
	sentence = string.replace(sentence, '*','')
	sentence = string.replace(sentence, '\'',' ')
	sentence = string.replace(sentence, '"','')
	sentence = string.replace(sentence, '-',' ')
	return sentence

def getWordsFromSentence(sentence):
	s = ''
	addedSpace = True
	for l in sentence.lower():
		if l.isalnum():
			s += l
			addedSpace = False
		elif not addedSpace:
			s += ' '
			addedSpace = True

	if addedSpace and s != '':
		s = s[:-1]
	return s.split(' ')

def scoreOccurenceSentence(sentence, wordList, authorList):
	words = getWordsFromSentence(sentence)
	res = []
	for i in range(0, len(authorList)):
		score = 0
		for word in words:
			if word in wordList[i].keys():
				score += wordList[i][word]
		res.append(score)
	return getIndixMax(res)

def getIndixMax(liste):
	index = 0
	maxx = 0
	for i in range(0, len(liste)):
		if liste[i] > maxx:
			maxx = liste[i]
			index = i
	return index

def buildNumberedWords(authorList, allWords):
	res = [{} for i in range(len(authorList))]
	for i in range(0, len(allWords)):
		for j in range(0, len(allWords[i])):
			res[i][allWords[i][j]] = j
	return res


def buildWordMatrix(authorList, trainingList, wordList, numberedWords):
	#####################################
	# construction des matrices automates, une pour chaque auteur
	# chaque matrice est en fait une liste de dico, avec pour l'indice de la liste le i, la cle du dico le j et la valeur le poids en (i,j) de la matrice
	# pour chaque mot i on note a(i,j) la probabilité, pour un auteur fixé, que le mot j succède au mot i dans la phrase
	# [[{2,3},{4,67},{1,4}],[{2,1},{1,3}]]

	listeMatrices = [[] for i in range(0, len(authorList))]
	for i in range(0, len(authorList)):
		for j in range (0, len(numberedWords[i].keys())):
			listeMatrices[i].append({})
	#print listeMatrices

	for element in trainingList:
		sentence = element[0]
		words = getWordsFromSentence(sentence)

		for i in range(0, len(words)-1):
			lowercasedI = words[i].lower()
			lowercasedNextI = words[i+1].lower()
			#incrémenter a(i,j) dans la matrice
			# deja on est dans la liste numéro authorList[element[1]], celle qui correspond à l'auteur de la phrase en cours
			# on utilise word[i] et word[i+1]
			if lowercasedNextI in listeMatrices[authorList[element[1]]][numberedWords[authorList[element[1]]][lowercasedI]].keys():
				listeMatrices[authorList[element[1]]][numberedWords[authorList[element[1]]][lowercasedI]][lowercasedNextI] += 1
			else:
				listeMatrices[authorList[element[1]]][numberedWords[authorList[element[1]]][lowercasedI]][lowercasedNextI] = 1

	return listeMatrices

# def buildNumberedWords(authorList, trainingList, wordList):
# 	#On construit les dicos pour associer un mot a un int
# 	numberedWords = [{} for author in authorList]
# 	for i in range(0, len(wordList)):
# 		for j in range(0, len(wordList[i])):
# 			numberedWords[i][wordList[i][j]] = j
# 	return numberedWords

def getPunctuationNumber(sentence):
	result = re.findall(';|,|\.|!|\?',sentence)
	return len(result)

def getUppercaseNumber(sentence):
	return sum(1 for c in sentence if c.isupper())

def allWordsByAuthor(trainingList, authorList):
	res = [[] for i in range(len(authorList))]
	for element in trainingList:
		sentence = element[0]
		words = getWordsFromSentence(sentence)
		for word in words:
			if word != 'Author' and word not in res[authorList[element[1]]]:
				res[authorList[element[1]]].append(word)
	return res 

def weightedWords(allWords, authorList):
	res = {}
	for i in range( len(allWords) ):
		for word in allWords[i]:
			if word not in res.keys():
				res[word] = 1
			else:
				res[word] += 1

	for word in res.keys():
		if res[word] != 1:
			res[word] = 1.0/res[word]
		else:
			res[word] = 2.0    # coefficient énorme pour les mots n'apparaissant que chez un auteur
	return res


def tfidfWeightedWords(wordList, authorList):
	res = [{} for author in authorList]
	for author in authorList.keys():
		for word in wordList[authorList[author]].keys():
			res[authorList[author]][word] = getTfidfWeight(word, author, authorList, wordList)
	return res

def getTfidfWeight(word, author, authorList, wordList):
	return getFrequency(word, author, wordList, authorList)*getIdfi(word, wordList, authorList)

def getFrequency(word, author, wordList, authorList):
	total = 0
	f = 0
	for key in wordList[authorList[author]].keys():
		if key == word:
			f = wordList[authorList[author]][key]
		total += wordList[authorList[author]][key]
	return f*1.0/total

def getIdfi(word, wordList, authorList):
	total = 0
	for author in authorList:
		for key in wordList[authorList[author]].keys():
			if key == word:
				total += 1
	if total !=0:
		return math.log(6.0/total)
	return 0

#################################################################
###################        MAIN         #########################
###################						#########################
#################################################################

print 'Beginning...'
with open('train_sample.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=';')
	trainingList = list(reader)

trainingList.pop(0)
testList = []
i = 0
for element in trainingList:
	if (i % 10) == 0:
		testList.append(element)
		trainingList.pop(i)


print 'Building authorLists'
authorList = buildAuthorList(trainingList)
print authorList
reverseAuthorList = buildReversedAuthorList(authorList)

print 'Building wordLists'
wordList = getWordList(authorList, trainingList)
# #wordList = removeIsolatedWords(3, wordList)
# averageWordLength = getAverageLengthWordByAuthor(authorList, wordList)
# print averageWordLength
# # print wordList

print 'Building matrices'
allWords = allWordsByAuthor(trainingList, authorList)
# print 'Building weightedWords'
# weightedWords = weightedWords(allWords, authorList)
print 'Building numberedWords'
numberedWords = buildNumberedWords(authorList, allWords)
print 'Building wordMatrix'
wordMatrix = buildWordMatrix(authorList, trainingList, allWords, numberedWords)
print 'Building tfidfWeightedWords'
tfidfWeightedWords = tfidfWeightedWords(wordList, authorList)
print tfidfWeightedWords


# print 'He had always the look of one who had kept himself unspotted from the world.'
# print calculerProbaTousAuteurs('He had always the look of one who had kept himself unspotted from the world.',authorList, reverseAuthorList, wordMatrix, tfidfWeightedWords)

print 'Beginning algorithm...'
getAlgorithmScore(authorList, wordMatrix, tfidfWeightedWords, reverseAuthorList)

# print 'Plotting'
# plotpoints2(authorList, testList, wordMatrix, numberedWords, weightedWords)

# print 'Building lengthList'
# sentenceLengthList = getLengthSentenceByAuthor(authorList, trainingList)
# averageLengthList = getAverageLengthByAuthor(sentenceLengthList, authorList)
# #print sentenceLengthList
# print averageLengthList

#plotPoints(authorList, trainingList)