# encoding = utf-8
from dim_items import *
from dim_fashion_matchsets import *
from clac_similarity import *


class Predict:
    def __init__(self, test_filename, dim_items, cat_similarities, word_similarities):
        self.test_filename = test_filename
        self.dim_items = dim_items
        self.cat_similarities = cat_similarities
        self.word_similarities = word_similarities

    def predict(self):
        f = open(' fm_submissions', 'wa')
        for line in open(self.test_filename):
            item = line.strip()
            similarities = self.get_similarity(item)

            to_write = item + ' '
            num = 200
            for item in similarities.keys():
                if(num == 0):
                    break
                num -= 1
                to_write += item + ','
            f.write(to_write[:-1])

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
    filename = "c:\Users\SunderLab\Documents\myfile\cloth_matching_challenge\data\dim_items.txt"
    di = DimItems(filename)
    dims = di.read_in()
    filename = "c:\Users\SunderLab\Documents\myfile\cloth_matching_challenge\data\dim_fashion_matchsets.txt"
    ms = MatchSets(filename)
    match_pairs = ms.get_match_pairs()
    cs = CalcSimilarity()
    csw = cs.WordSim(dims, match_pairs)
    word_sim = csw.calc()
    css = cs.CatSim(dims, match_pairs)
    cat_sim = css.calc()
    p = Predict(dims, cat_sim, word_sim)
    p.predict()