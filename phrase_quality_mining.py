from math import log2
from helper import findKthLargest
def phrasePKLMining(len_corpus, frequentPatterns):
    '''
    :param corpus:              corpus of text
    :param frequentPatterns:    frequency
    :return:
    '''
    # quality only for phrase, for single word, the quality is zero

    #len_corpus = len(corpus)

    # PKL

    PKL = {}

    tmp_pkl = 0.0
    min_pml = float("inf")
    for pattern, frequency in frequentPatterns.items():
        units = pattern.split()
        if len(units) >= 2:
            tmp_pkl = 0.0
            min_pml = float("inf")
            for i in range(1, len(units)):
                f_v  = frequentPatterns[pattern]
                f_ul = frequentPatterns[ ' '.join(units[: i]) ]
                f_ur = frequentPatterns[ ' '.join(units[i: ]) ]

                #min_pml = min(min_pml, log2(len_corpus*f_v/(f_ul*f_ur)))
                min_pml = min(min_pml, log2(len_corpus * f_v / (f_ul * f_ur)))
            #update pkl for phrase

            #tmp_pkl = min_pml * frequency / len_corpus

            tmp_pkl = min_pml * frequency

            PKL[pattern] = tmp_pkl

    return PKL


def wordIDFMining(frequentPatterns):

    # frequent phrases
    frequentPhrases = {}
    # word that in frequent Phrase
    frequentWords = {}

    #generate frequentPhrases
    for pattern, frequency in frequentPatterns.items():
        if len(pattern.split()) > 1:
            frequentPhrases[pattern] = frequency

    #generate grequentWords
    for phrase, frequency in frequentPatterns.items():
        words = phrase.split()
        for word in words:
            if word in frequentWords:
                frequentWords[word] += 1
            else:
                frequentWords[word] = 1

    len_words = len(frequentWords)
    len_phrases = len(frequentPhrases)

    # IDF of the frequent word
    '''
    IDF of a phrase:    phrase -- file
    IDF of a word:      word   -- phrases
    '''

    IDF_words = {}

    # update the words
    word_cnt = 0
    for word in frequentWords.keys():

        IDF_words[word] = log2(len_phrases / frequentWords[word])


    return IDF_words

def phraseQualityMining(corpus_length, frequentPatterns, quality_division = 0.1, outputName=''):
    '''
    :param corpus:              corpus of text
    :param frequentPatterns:    frequency
    :return:                    phrase qulity quality and threshold
    '''
    # quality only for phrase, for single word, the quality is zero

    quality_phrases = {}
    quality_threshold = 0.0
    quality_percent = quality_division

    #
    len_corpus = corpus_length


    # IDF of the frequent word
    # two subdicts of frequent patterns

    # frequent phrases
    frequentPhrases = {}
    # word that in frequent Phrase
    frequentWords = {}

    # generate frequentPhrases
    for pattern, frequency in frequentPatterns.items():
        if len(pattern.split()) > 1:
            frequentPhrases[pattern] = frequency

    # generate grequentWords
    for phrase, frequency in frequentPatterns.items():
        words = phrase.split()
        for word in words:
            if word in frequentWords:
                frequentWords[word] += 1
            else:
                frequentWords[word] = 1

    len_words = len(frequentWords)
    len_phrases = len(frequentPhrases)

    # IDF of the frequent word
    '''
    IDF of a phrase:    phrase -- file
    IDF of a word:      word   -- phrases
    '''

    IDF_words = wordIDFMining(frequentPatterns)


    # PKL of the frequent phrase

    PKL = phrasePKLMining(len_corpus, frequentPatterns)



    # end of PKL of the phrase
    # IDF of the phrase

    # compute the quality of the frequent phrase
    for phrase in frequentPhrases:
        phrase_quality = 0.0
        phrase_PKL = PKL[phrase]
        average_word_IDF = 0.0
        words = phrase.split()
        for word in words:
            average_word_IDF += IDF_words[word]
        average_word_IDF /= len(words)
        #
        phrase_quality = phrase_PKL / average_word_IDF

        quality_phrases[phrase] = phrase_quality

    # get the quality threshold
    quality_threshold = findKthLargest(quality_phrases.values(), int(quality_percent*len_phrases))

    #

    #write qualityfile
    if True:
        if len(outputName)>0:
            qualityFile = open(outputName, 'w', encoding='utf-8')
            for (key, value) in quality_phrases.items():
                qualityFile.write(key + "," + str(value) + '\n')

            qualityFile.close()

    return (quality_phrases, quality_threshold)

#def main function sd
if __name__ == '__main__':
    quality_division = 0.2
    len_corpus = 321032
    frequentPatternFileName = 'result/abstract_1000_2015_frequent_pattern.csv'
    patternFile = open(frequentPatternFileName, 'r')
    f = {}
    for line in patternFile:
        units = line.split(',')
        f[units[0]] = int(units[1])
    len_frequent_patterns = len(f)
    PKL = phrasePKLMining(len_corpus, f)
    IDF = wordIDFMining(f)
    (QUALITY, quality_threshold) = phraseQualityMining(len_corpus,f,quality_division)
    print(QUALITY)
    print(quality_threshold)