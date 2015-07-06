#!/usr/bin/env python
# -*- coding: utf-8 -*-

from commons import *

def useTFIDF(typeTF, tf, idf, sampling=False, numSampling=2, testSample=0):
    print('TypeTF : {}'.format(typeTF))

    if sampling:
        r = open('../../challenge_23_data/train_sample.csv', 'r', newline='', encoding='utf-8')

        ok = 0
        notOk = 0
    else:
        r = open('../../challenge_23_data/test_sample.csv', 'r', newline='', encoding='utf-8')

    i = -1
    results = []
    decisions = []
    for line in r.readlines():
        if i == -1:
            i += 1
            continue

        if sampling and (i%numSampling != testSample):
            i += 1
            continue

        if not sampling:
            line = line.replace('\\"', '""')
            row = parseLine(line)
            testID = int(row[0])
        else:
            row = parseLine(line)
            catID = catsToIDs[int(row[0])]

        if typeTF == 0:
            topics = parseTopicIDS(row[14]) + parseTopicIDS(row[15])
        else:
            words = getWordsFromSentence(row[1]) + getWordsFromSentence(row[2])

        tfidf = [0.0 for k in range(numCat)]
        
        ### Topics
        if typeTF == 0:
            for t in topics:
                for k in range(numCat):
                    if t in tf[k]:
                        tfidf[k] += tf[k][t] * idf[t]

        ### Words
        if typeTF == 1:
            for w in words:
                for k in range(numCat):
                    if w in tf[k]:
                        tfidf[k] += tf[k][w] * idf[w]

        ### Links
        if typeTF == 2:
            for i in range(len(words)):
                w = words[i]
                nextW = ''
                if i+1 != len(words):
                    nextW = words[i+1]
                prevW = ''
                if i-1 != -1:
                    prevW = words[i-1]

                for k in range(numCat):
                    if w in tf[k].keys() and nextW in tf[k][w].keys():
                        tfidf[k] += idf[w][nextW]# tf[k][w][nextW] * idf[w][nextW]
                    if prevW in tf[k].keys() and w in tf[k][prevW].keys():
                        tfidf[k] += idf[prevW][w]# tf[k][prevW][w] * idf[prevW][w]

        scores = [tfidf[i] for i in range(numCat)]
        results.append(scores)

        maxScore = scores[0]
        maxID = 0

        for k in range(1, numCat):
            if scores[k] > maxScore:
                maxScore = scores[k]
                maxID = k

        decisions.append(maxID)

        if sampling:
            if maxID == catID:
                ok += 1
            else:
                notOk += 1

        i += 1
    r.close()

    if sampling:
        accuracy = 100.0 * float(ok) / float(ok+notOk)
        print('Accuracy : {}'.format(accuracy))
        
        return results, decisions, accuracy
    else:
        return results, decisions

def computeAggregated(decisionTopics, accuracyTopics, decisionWords, accuracyWords, decisionWordLinks, accuracyWordLinks):
    aggregatedDecisions = []

    accuracies = [accuracyTopics, accuracyWords, accuracyWordLinks]
    print('Accuracies : {}'.format(accuracies))

    accuracies = [x/100.0 for x in accuracies]
    weights = [log(accuracies[i]/(1.0-accuracies[i])) + log(numCat-1) for i in range(len(accuracies))]
    print('Weights : {}'.format(weights))

    for i in range(len(decisionTopics)):
        scores = [0.0 for k in range(numCat)]

        scores[decisionTopics[i]] += weights[0]
        scores[decisionWords[i]] += weights[1]
        scores[decisionWordLinks[i]] += weights[2]

        maxScore = scores[0]
        maxID = 0

        for k in range(1, numCat):
            if scores[k] > maxScore:
                maxScore = scores[k]
                maxID = k

        aggregatedDecisions.append(maxID)

    return aggregatedDecisions   

def convertAggregatedDecisions(aggregatedDecisions):
    a = []
    for catID in aggregatedDecisions:
        a.append(IDsToCats[catID])
    return a