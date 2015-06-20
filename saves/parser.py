# -*- coding: utf-8 -*-
import csv
import re
import time
import math


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

def writeAnswer():
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

	    liste = getScoreList(row, tfidf14, tfidf15)

	    cat = getMaxIndex(liste)

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
	m = re.split(';', relevantTopicId)
	if m:
		for i in range(len(m)):
			m[i] = m[i]
		return m
	else:
		if relevantTopicId == "":
			return []
		else:
			return [].append(relevantTopicId)


print('Beginning parsing')
with open('../../challenge_23_data/train_sample.csv', 'rt', encoding='utf-8') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	trainingList = list(reader)

# with open('../challenge_23_data/test_sample.csv', 'rt', encoding='utf-8') as csvfile:
# 	reader = csv.reader(csvfile, delimiter=',')
# 	trainingList = list(reader)

trainingList.pop(0)

# Donc la on a les donnees comme il faut (on enleve la premiere ligne avec le nom des colonnes)

#print(trainingList)

categories = []
# extracting the data:
for element in trainingList:
	if element[0] == "": 
		#parce qu'on avait deux listes avec des numéros empty au début (c'est du à une virgule qui traîne dans le fond de celled d'avant)
		element.pop(0)
	if element[0] not in categories:
		categories.append(element[0])

print(categories)


# ETAPE NUMERO 1

numCat = 15
catsToIDs = {1: 0, 2: 1, 10: 2, 15: 3, 17: 4, 19: 5, 20: 6, 22: 7, 23: 8, 24: 9, 25: 10, 26: 11, 27: 12, 28: 13, 29: 14}
IDsToCats = {0: 1, 1: 2, 2: 10, 3: 15, 4: 17, 5: 19, 6: 20, 7: 22, 8: 23, 9: 24, 10: 25, 11: 26, 12: 27, 13: 28, 14: 29}


def computeTFIDF(id):
	apparitions = [{} for i in range(numCat)]
	print(apparitions)

	for i in range(numCat):
		for video in trainingList:
			if int(video[0]) == IDsToCats[i]:
				for topic in parseRelevantTopicId(video[id]):
					if topic not in apparitions[i].keys():
						apparitions[i][topic] = 1
					else:
						apparitions[i][topic] += 1

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
		idf[topic] = numCat*1.0/numCatForTopicId[topic]

	print('etape 3 done')

	# ETAPE 4

	tf =[{} for i in range (numCat)]
	for i in range(numCat):
		somme =0
		for topic in apparitions[i].keys():
			somme += apparitions[i][topic]

		for topic in apparitions[i].keys():
			tf[i][topic] = apparitions[i][topic]*1.0/somme

	print('etape 4 done')

	# ETAPE NUMERO 5
	tfidf = [{} for i in range(numCat)]

	for i in range(numCat):
		for topic in tf[i].keys():
			tfidf[i][topic] = tf[i][topic]*math.pow(idf[topic],3)

	print('etape 5 done')
	return tfidf

tfidf15 = computeTFIDF(15)
tfidf14 = computeTFIDF(14)

writeAnswer()

 
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

