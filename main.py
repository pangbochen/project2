import sys

from frequent_pattern_mining import *
from phrase_quality_mining import *
from phrase_construction import *

if __name__ == "__main__":

    #min
    max_phrase_length = 4
    threshold = 5
    division_of_phrase_quality = 0.4

    rawTextName = 'data/abstract_1000_2015.txt'
    frequentOutputFileName = 'result/abstract_1000_2015_frequent_pattern.csv'
    qualityOutputFileName = 'result/abstract_1000_2015_phrase_quality.csv'
    segmentedFileName = 'result/abstract_1000_2015_segmented.txt'

    rawFile = open(rawTextName, 'r',encoding='utf-8')
    corpus = []

    # stop points

    StopPoint = "?,.!;:\'\"[]"

    # create corpus line by line, char by char
    for line in rawFile:
        insideCnt = 0
        tmpChars = []

        for c in line:
            # handle the () like case
            if c == '(':
                insideCnt += 1
            elif c == ')':
                insideCnt -= 1
            # no ()
            elif insideCnt == 0:
                if c.isalpha():
                    # only keep the lower part
                    tmpChars.append(c.lower())
                elif c == '\'':
                    tmpChars.append(c)
                else:
                    if len(tmpChars) > 0:
                        corpus.append(''.join(tmpChars))
                    tmpChars.clear()
            #if c in StopPoint:
                #corpus.append('@')

        if len(tmpChars) > 0:
            corpus.append(''.join(tmpChars))
            tmpChars.clear()
    rawFile.close()
    # end of create corpus of the
    print("create corpus from file " + rawTextName)
    print("the corpus size is " + str(len(corpus)))
    #get frequent patterns imformation

    frequentPatterns  = frequentPatternMining(corpus, frequentOutputFileName, threshold, max_phrase_length)


    print("the threshold is " + str(threshold))
    print("create frequent patterns file : " + frequentOutputFileName)
    print("size of frequent patterns is " + str(len(frequentPatterns)))

    #end of frequent patterns

    # TODO phrase quality

    (phraseQuality, phraseQualityThreshold) = phraseQualityMining(len(corpus), frequentPatterns, division_of_phrase_quality, qualityOutputFileName)
    print("create phrase quality file : " + qualityOutputFileName)
    print("size of phrase quality file is " + str(len(phraseQuality)))

    print("threshold of phrase quality is "+str(phraseQualityThreshold))

    # # TODO the connection of quality and construction
    rawFile = open(rawTextName, 'r', encoding='utf-8')
    segmentedFile = open(segmentedFileName, 'w', encoding='utf-8')

    for line in rawFile:

        line_corpus = line.split()
        constructor = phraseConstructor(phraseQuality, line_corpus, phraseQualityThreshold)
        constructor.construct_phrases()

        segmented_line = constructor.getText()


        segmentedFile.write(segmented_line+'\n')
    segmentedFile.close()


    # Finised input of LDA
    #store phrases as input of LDA model

