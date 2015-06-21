# -*- coding: utf-8 -*-
import csv

def buildText():
	print('Beginning parsing')
	with open('../../challenge_23_data/train_sample.csv', 'rt', encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		trainingList = list(reader)

	trainingList.pop(0)
	for element in trainingList:
		if element[0] == '':
			element.pop(0)

	wordCount = [{}]
	for element in trainingList:



	return
