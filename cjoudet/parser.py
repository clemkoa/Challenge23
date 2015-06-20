# -*- coding: utf-8 -*-
import csv
import re
import isodate

def parseDuration(word):
	sum = 0
	m = re.findall('M([0-9]*)S', word)
	if m:
		sum += int(m[0])
	else:
		print(word + "	nope	")
		# m = re.findall('PT([0-9]*)S', word)
		# return m[0]
	m = re.findall('([0-9]*)M', word)
	print('test')
	return sum


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
					print(parseDuration(element[j]), end="")
				print(element[j] + "	", end="")
		print()
	i += 1

