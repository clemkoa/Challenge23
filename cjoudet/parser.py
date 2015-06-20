# -*- coding: utf-8 -*-
import csv

print 'Beginning parsing'
with open('../challenge_23_data/train_sample.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	trainingList = list(reader)

trainingList.pop(0)

# Donc la on a les donnees comme il faut (on enleve la premiere ligne avec le nom des colonnes)

print trainingList