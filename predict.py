# encoding = utf-8
from dim_items import *
from dim_fashion_matchsets import *
from my_const import *
from clac_similarity import *


class Predict:
    def __init__(self, test_filename, dim_items, cat_similarities, word_similarities):
        self.test_filename = test_filename
        self.dim_items = dim_items
        self.cat_similarities = cat_similarities
        self.word_similarities = word_similarities

    def predict(self):
        logging.debug('predict start')
        f = open(FilePath.fm_submissions, 'w+')
        for line in open(self.test_filename):
            item = line.strip()
            similarities = self.get_similarity(item)

            to_write = item + ' '
            for i in range(0, 199):
                item = similarities[i][0]
                to_write += item + ','
            f.write(to_write[:-1] + '\n')
        logging.debug('finish predicting')

    def get_similarity(self, item):
        similarities = {}
        for another_item in self.dim_items.keys():
            if another_item == item:
                continue
            item_sim = self.get_item_similarity(item, another_item)
            similarities[another_item] = item_sim
        similarities = sorted(similarities.iteritems(), key=lambda temp: temp[1], reverse=True)
        return similarities

    def get_item_similarity(self, item, another_item):
        cat = self.dim_items[item].cat
        another_cat = self.dim_items[another_item].cat
        try:
            cat_sim = self.cat_similarities[cat][another_cat]
        except:
            cat_sim = 0
        terms = self.dim_items[item].terms
        another_terms = self.dim_items[another_item].terms
        term_sim = 0
        for word in terms:
            word_sim = 0
            for another_word in another_terms:
                try:
                    temp = self.word_similarities[word][another_word]
                except:
                    temp = 0
                if word_sim < temp:
                    word_sim = temp
            term_sim += word_sim
        return cat_sim + term_sim

if __name__ == '__main__':
    di = DimItems(FilePath.dim_items)
    dims = di.read_in()
    ms = MatchSets(FilePath.dim_fashion_matchsets)
    match_pairs = ms.get_match_pairs()
    cs = CalcSimilarity()
    csw = cs.WordSim(dims, match_pairs, FilePath.word_similarities)
    word_sim = csw.calc()
    css = cs.CatSim(dims, match_pairs, FilePath.cat_similarities)
    cat_sim = css.calc()
    p = Predict(FilePath.test_items, dims, cat_sim, word_sim)
    p.predict()
