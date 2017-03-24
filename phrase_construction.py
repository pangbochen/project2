class constructNode:
    def __init__(self, _left=0, _right=0,_sig=0):
        '''
        :param _left:  left bendge
        :param _right: right bendge
        :param _sig:  sig
        '''
        self.left = _left
        self.right = _right
        self.sig = _sig
        self.donotsearch = False

    def printNode(self):
        print(self.left, self.right, self.sig)

    def isToDelete(self, cmpNode):
        '''
        :param cmpNode: constructNode
        :return:
        '''
        return (cmpNode.left <= self.left and cmpNode.right >=self.right) or \
            ( cmpNode.left>=self.left and cmpNode.right <= self.right) or \
            ( cmpNode.left<=self.left and self.left<=cmpNode.right<=self.right) or \
            ( cmpNode.right>=self.right and self.left<=cmpNode.left<= self.right)

    def setZero(self):
        self.left,self.right,self.sig = 0,0,0

class phraseConstructor:

    def __init__(self, sig_f, text_corpus, min_thresh):
        '''
        :param sig_f:       sig score dict
        :param text_corpus:  corpus of the document
        :param thresh:  min thresh <=
        '''
        self.f = sig_f
        self.thresh = min_thresh
        self.H = [constructNode(int(i), int(i),int(sig_f[text_corpus[i]] if text_corpus[i] in sig_f else 0)) for i in range(len(text_corpus))]
        self.corpus = text_corpus
        self.createPairSig(sig_f, self.H, text_corpus)

    def createPairSig(self, f, H, corpus):
        self.pair_sig = [ constructNode(i, i+1, f[ ' '.join(corpus[ H[i].left : H[i+1].right+1 ]) ] if ' '.join(corpus[ H[i].left : H[i+1].right+1 ]) in f else 0 ) for i in range(len(H)-1) ]

    def find_max_pair_of_H(self):
        if len(self.H) > 1:
            m = 0
            k = 0
            tmp_sig = 0
            tmp_str = ''
            for i in range(0, len(self.H) - 1):
                tmp_str = ' '.join(self.corpus[self.H[i].left: self.H[i + 1].right + 1])
                tmp_sig = self.f[tmp_str] if tmp_str in self.f else 0
                if tmp_sig > m:
                    k = i
                    m = tmp_sig
            return (k, m)
        else:
            return (-1, -1)

    def find_max_pair_of_H_from_pair_sig(self):
        if len(self.pair_sig) > 0:
            m = 0
            k = 0
            for i in range(len(self.pair_sig)):
                if self.pair_sig[i].sig > m:
                    k = i
                    m = self.pair_sig[i].sig
            return (k, m)
        else:
            return -1

    def PrintH(self):
        for item in self.H:
            print(item.left, item.right, item.sig)

    def construct_phrases(self):
        while len(self.H) > 1:
            # TODO design a list of <index, sig> for H to speed up
            (index_of_max, sig_of_max_pair) = self.find_max_pair_of_H_from_pair_sig()
            # (index_of_max, sig_of_max_pair) = find_max_pair_of_H(H)         #find max pair
            # merge the pair
            # judge is to merge
            if sig_of_max_pair >= self.thresh:
                self.H[index_of_max].right = self.H[index_of_max + 1].right
                self.H[index_of_max].sig = sig_of_max_pair

                # update pair_sig list
                if index_of_max != 0:
                    # update pre node
                    # unchage pair_sig[index_of_max-1].left

                    self.pair_sig[index_of_max - 1].right = self.H[index_of_max].right
                    tmp_str = ' '.join(self.corpus[self.pair_sig[index_of_max - 1].left: self.pair_sig[index_of_max - 1].right + 1])
                    tmp_sig = self.f[tmp_str] if tmp_str in self.f else 0
                    self.pair_sig[index_of_max - 1].sig = self.f[tmp_str] if tmp_str in self.f else 0
                if index_of_max != len(self.pair_sig) - 1:
                    # update post node
                    # unchange pair_sig[index_of_max-1].right
                    self.pair_sig[index_of_max + 1].left = self.H[index_of_max].left
                    tmp_str = ' '.join(self.corpus[self.pair_sig[index_of_max + 1].left: self.pair_sig[index_of_max + 1].right + 1])
                    tmp_sig = self.f[tmp_str] if tmp_str in self.f else 0
                    self.pair_sig[index_of_max + 1].sig = tmp_sig
                # delete node for H and pair_sig
                del self.pair_sig[index_of_max]
                del self.H[index_of_max + 1]
            else:
                break

    def getPhrase(self):
        ret = [("", 0) for _ in range(len(self.H))]
        (tmp_str, tmp_sig) = ("",0)
        for i in range(len(self.H)):
            tmp_str = "-".join(self.corpus[self.H[i].left : self.H[i].right+1])
            tmp_sig = self.f[tmp_str] if tmp_str in self.f else 0
            ret[i] = (tmp_str, tmp_sig)
        return ret


#as

if __name__ == "__main__":
    thresh = 5
    f = {"marko blanket": 5, "feature selection": 6, "support vector": 12, "support vector machines": 8}
    str = "marko blanket feature selection for support vector machines"
    corpus = str.split()

    constructor = phraseConstructor(f, corpus, thresh)
    constructor.construct_phrases()
    constructor.PrintH()

    phrases = constructor.getPhrase()

    print(' '.join( [item[0] for item in phrases] ))