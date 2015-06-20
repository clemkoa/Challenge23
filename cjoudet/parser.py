# -*- coding: utf-8 -*-
import csv
import re
import isodate

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

i = 0
tab = [9,12,15]
for element in trainingList:
	if i < 100:
		for j in range(len(element)):
			if j in tab:
				if j == 9:
					print(str(readDuration(element[j])) + "	", end="")
				elif j == 15:
					for topic in parseRelevantTopicId(element[j]):
						print(topic + " TTT ", end= "")
				else:
					print(element[j] + "	", end="")
		print()
	i += 1

