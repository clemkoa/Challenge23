import parser
import matplotlib.pyplot as plt

def plotPoints(trainingList, tfidf14, tfidf15):
	x = []
	y = []
	j = 0
	for i in range(2):
		for video in trainingList:
			if (j%10) == 0:
				if int(video[0]) == IDsToCats[i]:
					 x.append(parser.getScoreForCat(video, tfidf14, tfidf15,1))
				#			x.append(getAverageWordLengthInSentence(element[0]))
				#			x.append(getPunctuationNumber(element[0]))
					# if int(video[6]) !=0:
					# 	calc = int(video[5])*1.0/(int(video[6]) + int(video[5]))
					# else:
					# 	calc = 1
					# x.append(calc)
					 y.append(parser.getScoreForCat(video, tfidf14, tfidf15,0))
			j += 1
		plt.plot(x,y,'o')
		x = []
		y = []
	plt.show()		
	return 






######################################################
######################################################
######################################################
######################################################
######################################################

# ETAPE NUMERO 1

numCat = 15
catsToIDs = {1: 0, 2: 1, 10: 2, 15: 3, 17: 4, 19: 5, 20: 6, 22: 7, 23: 8, 24: 9, 25: 10, 26: 11, 27: 12, 28: 13, 29: 14}
IDsToCats = {0: 1, 1: 2, 2: 10, 3: 15, 4: 17, 5: 19, 6: 20, 7: 22, 8: 23, 9: 24, 10: 25, 11: 26, 12: 27, 13: 28, 14: 29}

trainingList = parser.initiateTrainingList()
tfidf15 = parser.computeTFIDF(15, trainingList)
tfidf14 = parser.computeTFIDF(14, trainingList)
plotPoints(trainingList, tfidf14, tfidf15)
