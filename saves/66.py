# -*- coding: utf-8 -*-
import csv
import re
import time
import math
import random
from sklearn import linear_model
from sklearn import svm
from sklearn import ensemble
from sklearn.naive_bayes import GaussianNB

def parseLine(line):
    if line[0] == ',':
        line = line[1:]

    l = []
    start = 0
    inQuotes = False
    hasQuotes = False
    for i in range(len(line)):
        if line[i] == '"':
            inQuotes = not inQuotes
            hasQuotes = True
        elif line[i] == ',' and not inQuotes:
            if hasQuotes:
                v = line[start+1:i-1]
                l.append(v.replace('""', '"'))
            else:
                l.append(line[start:i])
            start = i+1
            hasQuotes = False
            inQuotes = False

    if hasQuotes:
        v = line[start+1:-2] # Because of \n
        l.append(v.replace('""', '"'))
    else:
        l.append(line[start:-1]) # Because of \n

    return l

def writeAnswer(tfidf14, tfidf15):
	r = open('../../challenge_23_data/test_sample.csv', 'r', newline='', encoding='utf-8')
	w = open('results.csv', 'w')

	i = 0
	somme = 0
	start = time.clock()
	w.write('id;video_category_id\n')
	for line in r.readlines():
	    if i == 0:
	        i += 1
	        continue

	    #print(i)
	    line = line.replace('\\"', '""')
	    row = parseLine(line)

	    cat = getBetterCatForTopic(row, tfidf14, tfidf15)

	 #    liste1 = getScoreList2(row, tfidf14)
	 #    liste2 = getScoreList2(row, tfidf15)
		# cat1 = getMaxIndex(liste1)
	 #    cat2 = getMaxIndex(liste2)

	 #    if cat1 == cat2:
	 #    	somme += 1

	    w.write(str(row[0]) + ';' + str(IDsToCats[cat]) + '\n')
	print('somme = ' + str(somme))
	print('done')
	return

def useSVM(tfidf15, trainingList):
	X = []
	Y = []
	#j = 0
	#tot = 0
	# j = 0
	for element in trainingList:
		# if (j%2) != 0:
		# tot += 1
		# print(str(j))
		topicList1 = parseRelevantTopicId(element[15])
		topicList2 = parseRelevantTopicId(element[14])
		res = []
		for i in range(numCat):
			value = 0
			for topic in topicList1:
				if topic in tfidf15[i].keys():
					value += tfidf15[i][topic]
			for topic in topicList2:
				if topic in tfidf15[i].keys():
					value += tfidf15[i][topic]
			res.append(value)
			
		res.append(readDuration(element[9]))
		if element[5] == 'NA' or element[6] == 'NA':
			res.append(0)
			res.append(0)
		# elif (float(element[5])+float(element[6])) == 0:
		# 	res.append(0)
		# else:
		# 	res.append(float(element[6])/(float(element[5])+float(element[6])))			
		else:
			res.append(int(element[5]))
			res.append(int(element[6]))		
		X.append(res)
		Y.append(int(element[0]))
		# j += 1

	# print(tot)
	# La c'est bon on a build X et Y
	# maintenant on passe au test
	print('setting model')
	#clf = linear_model.SGDClassifier(shuffle=True)
	# clf = GaussianNB()
	# clf = ensemble.BaggingClassifier(n_estimators=20)
	clf = ensemble.RandomForestClassifier(n_estimators=20, warm_start=True, criterion="entropy")

	print('beginning fitting')	
	clf.fit(X, Y) 
	print('fit done')

	r = open('../../challenge_23_data/test_sample.csv', 'r', newline='', encoding='utf-8')
	w = open('results.csv', 'w')

	w.write('id;video_category_id\n')

	m = 0
	for line in r.readlines():
		if m == 0:
		    m += 1
		    continue
		line = line.replace('\\"', '""')
		row = parseLine(line)

		res = [[]]
		topicList1 = parseRelevantTopicId(row[15])
		topicList2 = parseRelevantTopicId(row[14])
		
		for i in range(numCat):
			value = 0
			for topic in topicList1:
				if topic in tfidf15[i].keys():
					value += tfidf15[i][topic]
			for topic in topicList2:
				if topic in tfidf15[i].keys():
					value += tfidf15[i][topic]
			if value == 0.0:
				res[0].append(0)
			else:
				res[0].append(value)
		res[0].append(readDuration(row[9]))
		if row[5] == 'NA' or row[6] == 'NA':
			res[0].append(0)
			res[0].append(0)
		else:
			res[0].append(int(row[5]))
			res[0].append(int(row[6]))
		

		#dec = clf.decision_function(res)
		# print(clf.predict(res))
		# print(res)
		# print(dec)
		w.write(str(row[0]) + ';' + str(clf.predict(res)[0]) + '\n')
	return ""



def getBetterCatForTopic(row, tfidf14, tfidf15):
	liste = getScoreList(row, tfidf14, tfidf15)
	return getMaxIndex(liste)

def getScoreForCat(row, tfidf14, tfidf15, i):
	liste = getScoreList(row, tfidf14, tfidf15)
	return liste[i]

def getScoreList(video, tfidf14, tfidf15):
	topicList = parseRelevantTopicId(video[15])
	res = []
	for i in range(numCat):
		value = 0
		for topic in topicList:
			if topic in tfidf15[i].keys():
				value += tfidf15[i][topic]
		res.append(value)
	for i in range(numCat):
		value = 0
		for topic in topicList:
			if topic in tfidf14[i].keys():
				value += tfidf14[i][topic]
		res[i] = value*value
	return res

def getScoreList2(video, tfidf):
	topicList = parseRelevantTopicId(video[15])
	res = []
	for i in range(numCat):
		value = 0
		for topic in topicList:
			if topic in tfidf[i].keys():
				value += tfidf[i][topic]
		res.append(value)
	return res


def getMaxIndex(liste):
	maxVal = 0
	maxId = 0
	for i in range(len(liste)):
		if liste[i] > maxVal:
			maxVal = liste[i]
			maxId = i
	return maxId


def readDuration(s):
    duration = 0

    if s == 'NA' or s == "":
        return 0

    #print(s)
    s = s[1:] # Remove the 'P'

    if s[0] != 'T':
        i = 0
        while s[i] != 'D':
            i += 1

        val = s[0:i]
        
        #print('Days : {}'.format(val))
        duration += val*24*3600

        s = s[i+1:]
    
    s = s[1:] # Remove the 'T'
    #print(s)

    while s != '':
        i = 0
        while s[i] != 'H' and s[i] != 'M' and s[i] != 'S':
            i += 1
        
        val = int(s[0:i])
        
        if s[i] == 'H':
            #print('Hours : {}'.format(val))
            duration += val*3600
        elif s[i] == 'M':
            #print('Minutes : {}'.format(val))
            duration += val*60
        elif s[i] == 'S':
            #print('Seconds : {}'.format(val))
            duration += val

        s = s[i+1:]

    #print('Duration : {}'.format(duration))
    return duration


def parseRelevantTopicId(relevantTopicId):
	if relevantTopicId == "":
		return []
	m = re.split(';', relevantTopicId)
	if m:
		return m
	else:
		return [].append(relevantTopicId)

def initiateTrainingList():
	print('Beginning parsing')
	with open('../../challenge_23_data/train_sample.csv', 'rt', encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		trainingList = list(reader)

	# with open('../challenge_23_data/test_sample.csv', 'rt', encoding='utf-8') as csvfile:
	# 	reader = csv.reader(csvfile, delimiter=',')
	# 	trainingList = list(reader)

	trainingList.pop(0)
	for element in trainingList:
		if element[0] == '':
			element.pop(0)

	return trainingList
# Donc la on a les donnees comme il faut (on enleve la premiere ligne avec le nom des colonnes)

#print(trainingList)
def initiateCategories(trainingList):
	categories = []
	# extracting the data:
	for element in trainingList:
		if element[0] == "": 
			#parce qu'on avait deux listes avec des numéros empty au début (c'est du à une virgule qui traîne dans le fond de celled d'avant)
			element.pop(0)
		if element[0] not in categories:
			categories.append(element[0])

	# print(categories)
	return categories

def computeTFIDF(id, trainingList):
	apparitions = [{} for i in range(numCat)]
	print(apparitions)

	for i in range(numCat):
		# j = 0
		for video in trainingList:
			# if (j%2) == 0:
			if int(video[0]) == IDsToCats[i]:
				for topic in parseRelevantTopicId(video[15]):
					if topic not in apparitions[i].keys():
						apparitions[i][topic] = 1
					else:
						apparitions[i][topic] += 1
			# j += 1

	for i in range(numCat):
		# j = 0
		for video in trainingList:
			# if (j%2) == 0:
			if int(video[0]) == IDsToCats[i]:
				for topic in parseRelevantTopicId(video[14]):
					if topic not in apparitions[i].keys():
						apparitions[i][topic] = 1
					else:
						apparitions[i][topic] += 1
			# j += 1

	print('etape 1 done')

	# ETAPE NUMERO 2 

	numCatForTopicId = {}
	for i in range(numCat):
		for topic in apparitions[i].keys():
			if topic in numCatForTopicId.keys():
				numCatForTopicId[topic] += 1
			else:
				numCatForTopicId[topic] = 1

	print('etape 2 done')

	# ETAPE NUMERO 3

	idf = {}
	for topic in numCatForTopicId.keys():
		# print(topic)
		idf[topic] = float(numCat)/float(numCatForTopicId[topic])

	# print(idf.keys())
	print('etape 3 done')

	# ETAPE 4

	tf =[{} for i in range (numCat)]
	for i in range(numCat):
		somme = 0
		for topic in apparitions[i].keys():
			somme += apparitions[i][topic]

		for topic in apparitions[i].keys():
			tf[i][topic] = apparitions[i][topic]/somme


	print('etape 4 done')

	# ETAPE NUMERO 5
	tfidf = [{} for i in range(numCat)]
	for i in range(numCat):
		for topic in tf[i].keys():
			tfidf[i][topic] = tf[i][topic]*math.pow(idf[topic],3)

	print('etape 5 done')
	return tfidf


def computeCrossTFIDF(id, trainingList, k, rand):
	print(str(rand))
	apparitions = [{} for i in range(numCat)]
	for i in range(numCat):
		n = 0
		j = 0
		for video in trainingList:
			if ((j+rand) % k) != 0:
				if (n%2) == 0:
					if int(video[0]) == IDsToCats[i]:
						for topic in parseRelevantTopicId(video[15]):
							if topic not in apparitions[i].keys():
								apparitions[i][topic] = 1
							else:
								apparitions[i][topic] += 1
			n += 1
			j += 1

	for i in range(numCat):
		n = 0
		j = 0
		for video in trainingList:
			if ((j+rand)%k) != 0:
				if (n%2) == 0:
					if int(video[0]) == IDsToCats[i]:
						for topic in parseRelevantTopicId(video[14]):
							if topic not in apparitions[i].keys():
								apparitions[i][topic] = 1
							else:
								apparitions[i][topic] += 1
			n += 1
			j += 1

	# ETAPE NUMERO 2 

	numCatForTopicId = {}
	for i in range(numCat):
		for topic in apparitions[i].keys():
			if topic in numCatForTopicId.keys():
				numCatForTopicId[topic] += 1
			else:
				numCatForTopicId[topic] = 1

	# ETAPE NUMERO 3

	idf = {}
	for topic in numCatForTopicId.keys():
		# print(topic)
		idf[topic] = float(numCat)/float(numCatForTopicId[topic])

	# ETAPE 4

	tf =[{} for i in range (numCat)]
	for i in range(numCat):
		somme = 0
		for topic in apparitions[i].keys():
			somme += apparitions[i][topic]

		for topic in apparitions[i].keys():
			tf[i][topic] = apparitions[i][topic]*1.0/somme

	# ETAPE NUMERO 5
	tfidf = [{} for i in range(numCat)]
	for i in range(numCat):
		for topic in tf[i].keys():
			tfidf[i][topic] = tf[i][topic]*math.pow(idf[topic],3)

	#print('etape 5 done')
	return tfidf

def crossSVM(tfidf15, trainingList, k, rando):
	X = []
	Y = []
	print(str(rando))
	#j = 0
	#tot = 0
	j = 0
	n = 0
	for element in trainingList:
		if ((j+rando)%k) != 0:
			if (n%2) != 0:
				# print(str(j))
				topicList1 = parseRelevantTopicId(element[15])
				topicList2 = parseRelevantTopicId(element[14])
				res = []
				for i in range(numCat):
					value = 0
					for topic in topicList1:
						if topic in tfidf15[i].keys():
							value += tfidf15[i][topic]
					for topic in topicList2:
						if topic in tfidf15[i].keys():
							value += tfidf15[i][topic]
					res.append(value)
				res.append(readDuration(element[9]))
				if element[5] == 'NA' or element[6] == 'NA':
					res.append(0)
					res.append(0)
				else:
					res.append(int(element[5]))
					res.append(int(element[6]))
				X.append(res)
				Y.append(int(element[0]))
		n += 1
		j += 1

	# La c'est bon on a build X et Y
	# maintenant on passe au test
	print('Setting classifier')
	# clf = ensemble.GradientBoostingClassifier()
	# clf = ensemble.BaggingClassifier(n_estimators=20)
	# clf = linear_model.SGDClassifier(shuffle=True)
	# clf = GaussianNB()
	clf = ensemble.RandomForestClassifier(n_estimators=25)

	print('beginning fitting')	
	clf.fit(X, Y) 
	print('fit done')

	print('Beggining cross test...')

	confusionMatrix = [[0 for j in range(numCat)] for i in range(numCat)]
	acc = 0
	tot = 0
	j = 0
	l = 0
	for row in trainingList:
		if l == 0:
		    l += 1
		    continue

		if ((j+rando)%k) == 0:
			# print(str(j))
			res = [[]]
			topicList1 = parseRelevantTopicId(row[15])
			topicList2 = parseRelevantTopicId(row[14])
			
			for i in range(numCat):
				value = 0
				for topic in topicList1:
					if topic in tfidf15[i].keys():
						value += tfidf15[i][topic]
				for topic in topicList2:
					if topic in tfidf15[i].keys():
						value += tfidf15[i][topic]
				if value == 0.0:
					res[0].append(0)
				else:
					res[0].append(value)
			res[0].append(readDuration(row[9]))
			if row[5] == 'NA' or row[6] == 'NA':
				res[0].append(0)
				res[0].append(0)
			else:
				res[0].append(int(row[5]))
				res[0].append(int(row[6]))
			temp = clf.predict(res)[0]
			if (int(temp) == int(row[0])):
				acc += 1
			confusionMatrix[catsToIDs[int(row[0])]][catsToIDs[int(temp)]] += 1
			tot += 1
		j += 1
	print()
	print (float(acc)/float(tot))
	print()
	for i in range(numCat):
		for j in range(numCat):
			print(str(confusionMatrix[i][j]) + "	", end="")
		print()

	return ""

def main():
	trainingList = initiateTrainingList()
	tfidf15 = computeTFIDF(15, trainingList)
	# tfidf14 = computeTFIDF(14, trainingList)

	# writeAnswer(tfidf14, tfidf15)
	useSVM(tfidf15, trainingList)
	return



def crossValidation(k):
	rand = int(random.random()*k)
	print(str(rand))
	trainingList = initiateTrainingList()
	tfidf15 = computeCrossTFIDF(15, trainingList, k, rand)

	crossSVM(tfidf15, trainingList, k, rand)
	return


# ETAPE NUMERO 1

numCat = 15
catsToIDs = {1: 0, 2: 1, 10: 2, 15: 3, 17: 4, 19: 5, 20: 6, 22: 7, 23: 8, 24: 9, 25: 10, 26: 11, 27: 12, 28: 13, 29: 14}
IDsToCats = {0: 1, 1: 2, 2: 10, 3: 15, 4: 17, 5: 19, 6: 20, 7: 22, 8: 23, 9: 24, 10: 25, 11: 26, 12: 27, 13: 28, 14: 29}

main()
# crossValidation(20)

# useSVM())

# i = 1000
# tab = [9,12,14,15]
# for element in trainingList:
# 	if i < 1100:
# 		for j in range(len(element)):
# 			if j in tab:
# 				if j == 9:
# 					print(str(readDuration(element[j])) + "	", end="")
# 				elif j == 14:
# 					print(str(parseRelevantTopicId(element[j])) + "	", end="")
# 				elif j == 15:
# 					print(str(parseRelevantTopicId(element[j])) + "	", end="")
# 				else:
# 					print(element[j] + "	", end="")
# 		print()
# 	i += 1
# lin_clf = svm.LinearSVC()
# lin_clf.fit(X, Y) 
# LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True, intercept_scaling=1, loss='squared_hinge', max_iter=1000, multi_class='ovr', penalty='l2', random_state=None, tol=0.0001, verbose=0)
# dec = lin_clf.decision_function([[1]])
# dec.shape[1]
# X = [[1,2], [5,8], [1.5,1.8], [8,8],[1,0.6], [9,11]]
# Y = [0, 1, 2, 1, 2,0 ]
# clf = svm.SVC(kernel='rbf')
# clf.fit(X, Y) 
# # SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.0, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)
# dec = clf.decision_function([1,3])
# print(dec)
# dec.shape[1] # 4 classes: 4*3/2 = 6