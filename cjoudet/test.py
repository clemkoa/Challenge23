# -*- coding: utf-8 -*-
import csv
import string


def calculerProbaAuteur(sentence, i):
	res = 0.0
	sentence = removePunctuation(sentence)
	words = sentence.split()
	for j in range(0, len(words)-1):
		lowercasedI = words[j].lower()
		lowercasedNextI = words[j+1].lower()
		if lowercasedI in numberedWords[i].keys() and lowercasedNextI in listeMatrices[i][numberedWords[i][lowercasedI]].keys():
			res += listeMatrices[i][numberedWords[i][lowercasedI]][lowercasedNextI]*allWords[lowercasedI]
	return res

def calculerProbaTousAuteurs(sentence, authorList, reverseAuthorList):
	res = {}
	for i in range(0, len(authorList.keys())):
		res[i] = calculerProbaAuteur(sentence, i)
	max = 0.0
	maxIndex = 0
	for key in res.keys():
		if res[key] > max:
			maxIndex = key
			max = res[key]
	return reverseAuthorList[maxIndex]

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

def buildWeightedWordsMatrix(wordList):
	res = {}
	for i in range(0, len(wordList)):
		for word in wordList[i]:
			if word not in res.keys():
				res[word] = 1
			else:
				res[word] += 1
	return res

def writeAnswer(authorList, reverseAuthorList):
	csvfile = open('test_sample.csv', 'rb')
	reader = csv.reader(csvfile, delimiter=';')
	trainingList = list(reader)

	w = open('result.csv', mode='w')
	w.write('Id;Author\n')

	for element in trainingList:
		number = element[0]
		sentence = element[1]
		sentence = removePunctuation(sentence)
		res = calculerProbaTousAuteurs(sentence, authorList, reverseAuthorList)
		w.write(str(number) + ';' + res + '\n')
#		print number
	print 'done'
	return


def crossLearning():
	pass

def crossTesting():
	csvfile = open('train_sample.csv', 'rb')
	reader = csv.reader(csvfile, delimiter=';')
	trainingList = list(reader)

	w = open('result_cross_testing.csv', mode='w')
	w.write('Id;Author\n')

	i = 0
	for element in trainingList:
		if (i % 10) == 0 and i != 0:
			number = i
			sentence = element[0]
			sentence = removePunctuation(sentence)
			res = calculerProbaTousAuteurs(sentence, authorList, reverseAuthorList)
			w.write(str(number) + ';' + res + '\n')
			# print number
		i += 1
	print 'done writing'

	csvfile.close()
	w.close()

	return

def getGrade():
	print 'beginning grading'
	# authorRank = {'twain': 2581,
	# 'doyle': 2872,
	# 'shakespeare': 3868,
	# 'austen': 7269,
	# 'wilde': 9098,
	# 'doyle': 11003,
	# 'poe': 11029,
	# 'twain': 14530,
	# 'doyle': 16859,
	# 'poe': 16928,
	# 'austen': 23454,
	# 'poe': 23591,
	# 'shakespeare': 24041,
	# 'doyle': 25050,
	# 'wilde': 27991,
	# 'shakespeare': 28724}

	goodAnwsers = 0
	total = 0

	r = open('result_cross_testing.csv', 'rb')
	resultReader = csv.reader(r, delimiter=';')
	resultList = list(resultReader)

	csvfile = open('train_sample.csv', 'rb')
	trainReader = csv.reader(csvfile, delimiter=';')
	trainingList = list(trainReader)

	i = 0
	for element in trainingList:
		if (i % 10) == 0 and i !=0:
			author = element[1]
			for result in resultList:
				if result[0] == i:
					total += 1
					if result[1] == author:
						goodAnwsers += 1
		i += 1
	print goodAnwsers
	print total
	return #(goodAnwsers)*1.0/total



#########################################################################

with open('train_sample.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    trainingList = list(reader)

# dico associant un auteur a un numero
authorList = {}
reverseAuthorList = {}
authorNumber = 0
for element in trainingList:
	if element[1] not in authorList and element[1] != 'Author': #histoire d'enlever l'auteur Author
		authorList[element[1]] = authorNumber
		authorNumber += 1

for key in authorList.keys():
	reverseAuthorList[authorList[key]] = key

print authorList

print reverseAuthorList

# on s'occuper de la liste des mots pour chaque auteur
wordList = []
for i in range(0, len(authorList)):
	wordList.append([])

print wordList

i = 0
for element in trainingList:
	if (i % 10) != 0:
		sentence = element[0]
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

		words = sentence.split()

		for word in words:
			if element[1] != 'Author' and word.lower() not in wordList[authorList[element[1]]]:
				wordList[authorList[element[1]]].append(word.lower())
	i += 1


#print wordList


##### Liste des mots tous mélangés par auteur
allWords = buildWeightedWordsMatrix(wordList)
for word in allWords.keys():
	if allWords[word] != 1:
		allWords[word] = 1.0/allWords[word]
	else:
		allWords[word] = 2.0

print allWords

numberedWords = []
for author in authorList:
	numberedWords.append({})

#print numberedWords


#On construit les dicos pour associer un mot a un int
for i in range(0, len(wordList)):
	for j in range(0, len(wordList[i])):
		numberedWords[i][wordList[i][j]] = j
#print numberedWords

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

integ = 0
for element in trainingList:
	if (integ % 10) !=0:
		sentence = element[0]
		sentence = removePunctuation(sentence)

		print sentence

		words = sentence.split()

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
	integ += 1

print 'Matrice finie, on attaque la normalisation'
#on normalise la matrice
for liste in listeMatrices:
	for dico in liste:
		sum = 0
		for value in dico.values():
			sum += value

		for key in dico.keys():
			dico[key] = (dico[key] + 0.0) / sum

#print listeMatrices[5]
print 'Matrice normalisée'
# maintenant qu'on a la matrice pour chaque auteur, quand on prend une phrase on peut avoir le score de chaque auteur

print calculerProbaTousAuteurs("What's onkores, Bilgewater?", authorList, reverseAuthorList)
print calculerProbaTousAuteurs("The promised letter of thanks from Mr. Collins arrived on Tuesday, addressed to their father, and written with all the solemnity of gratitude which a twelvemonth's abode in the family might have prompted.", authorList, reverseAuthorList)


print 'beginning cross testing sample'
#crossTesting()
print getGrade()

#print 'beginning computing on test sample'
#writeAnswer(authorList, reverseAuthorList)

# idées: mettre un systeme de poids pour chaque mot, en fonction du nombre de fois cité en tout
