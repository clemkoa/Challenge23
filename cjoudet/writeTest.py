# -*- coding: utf-8 -*-
import csv

def writeAnswer():
	csvfile = open('../../challenge_23_data/test_sample.csv', 'rt')
	reader = csv.reader(csvfile, delimiter=',')
	trainingList = list(reader)

	trainingList.pop(0)

	w = open('result.csv', mode='w')
	w.write('Id;Category\n')

	for element in trainingList:
		number = element[0]
		w.write(str(number) + ';1\n')
	print('done')
	return

writeAnswer()
