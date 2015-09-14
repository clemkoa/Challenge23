#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

def getWordsFromSentence(sentence):
    s = ''
    addedSpace = True
    for l in sentence.lower():
        if l.isalnum():
            s += l
            addedSpace = False
        elif not addedSpace:
            s += ' '
            addedSpace = True

    if addedSpace and s != '':
        s = s[:-1]

    return s.split(' ')

# Markov = [words, counts]
def getAuthorFromSentence(authorNames, markovs, sentence):
    words = getWordsFromSentence(sentence)
    maxAuthor = ''
    maxScore = 0.0

    scores = []
    for i in range(len(authorNames)):
        occ = 0
        order = 0.0
        currentOrderNum = 0
        orderNum = 0
        for k in range(len(words)):
            w = words[k]
            nextW = ''
            if k+1 != len(words):
                nextW = words[k+1]
            prevW = ''
            if k-1 != -1:
                prevW = words[k-1]

            add = False
            if w in markovs[i][0].keys():
                occ += markovs[i][0][w][0]
                if nextW in markovs[i][0][w][1].keys():
                    order += float(markovs[i][0][w][1][nextW])/float(markovs[i][0][w][0])
                    currentOrderNum += 1
                    add = True
                if prevW in markovs[i][0][w][2].keys():
                    order += float(markovs[i][0][w][2][prevW])/float(markovs[i][0][w][0])
                    currentOrderNum += 1
                    add = True

            if not add or nextW == '':
                orderNum += currentOrderNum#pow(currentOrderNum, 2)
                currentOrderNum = 0

        scoreW = (float(occ) / float(markovs[i][1]))# / float(len(words))
        scoreO = 0.0
        if orderNum != 0:
            scoreO += float(orderNum) / float(len(words))#order / orderNum
            score = scoreW + scoreO
        else:
            score = scoreW
        scores.append([score, scoreW, scoreO, ])

        #print('Score is {} + {}'.format(score-beta*order, beta*order))
        if score > maxScore:
            maxScore = score
            maxAuthor = authorNames[i]

    return maxAuthor, scores


print(u'Création des chaines de Markov')
r = csv.reader(open('challenge_21_data/train_sample.csv', mode='r', encoding='utf-8'), delimiter=';', quotechar='"')

authorNames = {0:'twain', 1:'doyle', 2:'shakespeare', 3:'austen', 4:'wilde', 5:'poe'}
authorIds = {'twain':0, 'doyle':1, 'shakespeare':2, 'austen':3, 'wilde':4, 'poe':5}

words = [{} for i in range(len(authorIds))]
counts = [0 for i in range(len(authorIds))]

SAMPLING = True
MAX_SAMPLE = 10
SAMPLE = 0

if SAMPLING:
    print(u'MAX_SAMPLE is {}, SAMPLE is {}'.format(MAX_SAMPLE, SAMPLE))

c = 0
author = ''
for row in r:
    if c == 0:
        c += 1
        continue

    if SAMPLING and c%MAX_SAMPLE == SAMPLE:
        c += 1
        continue

    i = authorIds[row[1]]

    ws = getWordsFromSentence(row[0])
    for k in range(len(ws)):
        w = ws[k]
        nextW = ''
        if k+1 != len(ws):
            nextW = ws[k+1]
        prevW = ''
        if k-1 != -1:
            prevW = ws[k-1]

        if w != '':
            counts[i] += 1

            if w not in words[i].keys():
                words[i][w] = [1, {nextW:1}, {prevW:1}]
            else:
                words[i][w][0] += 1
                if nextW not in words[i][w][1].keys():
                    words[i][w][1][nextW] = 1
                else:
                    words[i][w][1][nextW] += 1
                if prevW not in words[i][w][2].keys():
                    words[i][w][2][prevW] = 1
                else:
                    words[i][w][2][prevW] += 1

    c += 1

markovs = []
for i in range(len(authorIds)):
    markovs.append([words[i], counts[i]])

print(u'Chaines de Markov créées')
print()

alphas = [float(x)/100.0 for x in range(35, 66)]

r = csv.reader(open('challenge_21_data/train_sample.csv', mode='r', encoding='utf-8'), delimiter=';', quotechar='"')

matrix = [[0 for j in range(len(authorIds))] for i in range(len(authorIds))] # Confusion matrix : [RealAuthor][GuessedAuthor]

c = 0
for row in r:
    if c == 0:
        c += 1
        continue

    if SAMPLING and c%MAX_SAMPLE != SAMPLE:
        c += 1
        continue

    guess, scores = getAuthorFromSentence(authorNames, markovs, row[0])
    matrix[authorIds[row[1]]][authorIds[guess]] += 1
    
    """if row[1] != guess:
        print('wrong : {}'.format(c))
        print('scores :')
        for s in scores:
            print(s)
        #print(row[0].encode('utf-8', errors='ignore'))
        print('Should be {}, not {}'.format(authorIds[row[1]], authorIds[guess]))
        print()"""
    """else:
        print('right : {}'.format(c))
        print('scores :')
        for s in scores:
            print(s)
        #print(row[0].encode('utf-8', errors='ignore'))
        print('Is {}'.format(authorIds[row[1]]))
        print()"""

    c += 1

ok = 0
total = 0
for i in range(len(authorIds)):
    ok += matrix[i][i]
    for j in range(len(authorIds)):
        total += matrix[i][j]

accuracy = 100.0*float(ok)/float(total)

print(u'Accuracy : {}% ({} good out of {})'.format(accuracy, ok, total))
print(u'Confusion matrix : {}'.format(matrix))

"""r = csv.reader(open('challenge_21_data/test_sample.csv', mode='r', encoding='utf-8'), delimiter=';', quotechar='"')
w = open('challenge_21_data/answer.csv', mode='w', encoding='utf-8')
w.write('Id;Author\n')
c = 0
for row in r:
    if c == 0:
        c += 1
        continue
    guess = getAuthorFromSentence(authorNames, markovs, row[1])[0]
    w.write(row[0] + ';' + guess + '\n')
    c += 1
"""