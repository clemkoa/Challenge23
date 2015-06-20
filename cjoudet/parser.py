# -*- coding: utf-8 -*-
import csv

print('Beginning parsing')
with open('../challenge_23_data/train_sample.csv', 'rt', encoding='utf-8') as csvfile:
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