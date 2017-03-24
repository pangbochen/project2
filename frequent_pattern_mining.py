# -*- coding: utf-8 -*-
import codecs

def frequentPatternMining(corpus, oputfile, threshold):
    '''
    :param corpus:      the corpus of the text
    :param oputfile:    out file name of the frequent patterns
    :param threshold:   min frequent
    :return:            frequent patterns, frequency dic f of frequent patterns
    '''
    max_length_of_phrase = 6

    frequentPatterns = {}      # 'key' : frequency
    patterns = {}
    len_corpus = len(corpus)

    # for the length 1 words frequncy dict
    for i in range(len_corpus):
        if corpus[i] in patterns:
            patterns[corpus[i]].append(i)
        else:
            patterns[corpus[i]] = [i]

    patternFile = open(oputfile, 'w')

    len_pattern = 1

    while len(patterns) > 0:
        if len_pattern > max_length_of_phrase:
            break
        len_pattern += 1
        new_patterns = {}

        for pattern_phrase, positions in patterns.items():
            cnt_pattern = len(positions)
            posibility_pattern = cnt_pattern / len_corpus
            if cnt_pattern >= threshold:
                # key : [frequency, *quality]
                frequentPatterns[pattern_phrase] = cnt_pattern

                #result frequent pattern

                #TODO delete when finish quality part
                patternFile.write( pattern_phrase + "," + str(cnt_pattern) + "," + str(posibility_pattern) + '\n' )

                # search for new pattern with len_patter in length
                for i in positions:
                    if i+1 < len_corpus:
                        new_pattern_phrase = pattern_phrase + " " + corpus[i+1]

                        if new_pattern_phrase in new_patterns:
                            new_patterns[new_pattern_phrase].append(i+1)
                        else:
                            new_patterns[new_pattern_phrase] = [i+1]

        patterns.clear()
        patterns = new_patterns
    patternFile.close()
    return frequentPatterns

if __name__ == '__main__':
    threshold = 5
    rawTextFileName = 'result/abstract.txt'
    patternOutputFile = 'result/abstract_frequent_pattern.csv'
    ENDPIONTS = ".!?,;:\'\"[]"

    raw = open(rawTextFileName, 'r')
    corpus = []
    for line in raw:
        inside = 0
        chars = []
        for ch in line:
            if ch == '(':
                inside += 1
            elif ch == ')':
                inside -= 1
            elif inside == 0:
                if ch.isalpha():
                    chars.append(ch.lower())
                elif ch == '\'':
                    chars.append(ch)
                else:
                    if len(chars) > 0:
                        corpus.append(''.join(chars))
                    chars = []
            # if ch in ENDPIONTS:
            #     corpus.append('$')
        if len(chars) > 0:
            corpus.append(''.join(chars))
            chars = []
    print("length of the corpus from txt file is ", len(corpus))
    frequentPatterns = frequentPatternMining(corpus, patternOutputFile, threshold)
    print("number of the frequent patterns from corpus is ", len(frequentPatterns))
