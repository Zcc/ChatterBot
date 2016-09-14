# -*- coding: utf-8 -*-
from .base_match import BaseMatchAdapter
import os
import jieba
from gensim import corpora, models
from chatterbot.conversation import Statement
import copy


class ClosestCosineAdapter(BaseMatchAdapter):
    """
    The ClosestMatchAdapter creates a response by
    using fuzzywuzzy's process class to extract the most similar
    response to the input. This adapter selects a response to an
    input statement by selecting the closest known matching
    statement based on the Levenshtein Distance between the text
    of each statement.
    """

    def __init__(self, **kwargs):
        super(ClosestCosineAdapter, self).__init__(**kwargs)

        self.tfidf_model = None
        self.dictionary = None
        self.corpus = None
        self.corpus_vec = None
        self.inverted_index = {}
        # self.index = None

    def getCorpus(self, dic, sentencelist):
        return [dic.doc2bow(t) for t in self.segmentlist(sentencelist)]

    def Stopwords(self):
        data_file = os.path.join(
            os.path.dirname(__file__), 'data', 'stopwords.dic'
        )
        return [w.strip() for w in open(data_file, encoding='utf-8').readlines()]

    def segment(self, sentence):
        # stopwords = self.Stopwords()
        # stopwords = []
        # print len(stopwords),stopwords[:10]
        # return [w for w in jieba.cut(str(sentence)) if w not in stopwords]
        return [w for w in jieba.cut(str(sentence))]

    def segmentlist(self, sentencelist):
        return [self.segment(w) for w in sentencelist]

    def getCos(self, vector1, vector2):
        v1s = sum([v[1] * v[1] for v in vector1]) ** 0.5
        v2s = sum([v[1] * v[1] for v in vector2]) ** 0.5
        v1v2 = 0
        i = 0
        for v1 in vector1:
            if i >= len(vector2): break
            if v1[0] == vector2[i][0]: v1v2 += v1[1] * vector2[i][1]
            if v1[0] < vector2[i][0]: continue
            i += 1
        if v1s * v2s == 0:
            return -1
        return v1v2 / v1s * v2s

    def get(self, input_statement):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        if len(self.statement_list) == 0:
            print("loading data.....")
            self.statement_list = self.context.storage.get_response_statements()
        if not self.statement_list:
            if self.has_storage_context:
                # Use a randomly picked statement
                return 0, self.context.storage.get_random()
            else:
                raise self.EmptyDatasetException()

        confidence = -1
        closest_match = input_statement

        if self.tfidf_model is None:
            print('init tfidf model....')
            seg = [sw["segment_text"] for sw in self.statement_list]

            print('built dictionary....')
            self.dictionary = corpora.Dictionary(seg)
            self.corpus = [self.dictionary.doc2bow(t) for t in seg]

            print('training tfidf model....')
            self.tfidf_model = models.TfidfModel(self.corpus)
            self.corpus_vec = self.tfidf_model[self.corpus]

            print('built Inverted Index....')
            for i, cor in enumerate(self.corpus):
                for w in cor:
                    if self.inverted_index.get(w[0]):
                        self.inverted_index[w[0]].append(i)
                    else:
                        self.inverted_index[w[0]] = []

        query_bow = self.getCorpus(self.dictionary, [str(input_statement.text)])
        wordsinlist = []
        for word in query_bow[0]:
            wordsinlist += self.inverted_index.get(word[0])

        query_vec = self.tfidf_model[query_bow][0]
        for i, vec in ((j, self.corpus_vec[j]) for j in wordsinlist):
            cosine = self.getCos(query_vec, vec)
            if cosine >= confidence:
                closest_match = self.statement_list[i]
                confidence = cosine
        '''
        closest_match, confidence = process.extractOne(
            input_statement.text,
            text_of_all_statements
        )
        '''
        values = copy.deepcopy(closest_match)
        print(values)
        statement_text = values['text']

        del (values['text'])
        # Convert the confidence integer to a percent
        # confidence /= 100.0
        print(str(self.__class__).split('.')[-1][:-2], str(confidence), statement_text)
        return confidence, Statement(statement_text, **values)
