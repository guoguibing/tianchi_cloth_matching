# coding = utf-8

from dim_items import *
from dim_fashion_matchsets import *
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    filename='cloth_matching.log',
                    filemode='w')


class CalcSimilarity:

    class CatSim:
        def __init__(self, dim_items, match_pairs):
            self.dim_items = dim_items
            self.match_pairs = match_pairs

        def get_cat_pair(self):
            logging.debug('geting cat pairs')
            cat_pairs = {}
            for match_pair in self.match_pairs.keys():
                item_1, item_2 = match_pair.split(',')
                cat_1 = self.dim_items[item_1].cat
                cat_2 = self.dim_items[item_2].cat
                try:
                    cat_1_dic = cat_pairs[cat_1]
                except:
                    cat_1_dic = {}
                try:
                    value_1 = cat_1_dic[cat_2]
                except:
                    value_1 = 0
                cat_1_dic[cat_2] = value_1 + match_pairs[match_pair]
                cat_pairs[cat_1] = cat_1_dic

                try:
                    cat_2_dic = cat_pairs[cat_2]
                except:
                    cat_2_dic = {}
                try:
                    value_2 = cat_2_dic[cat_1]
                except:
                    value_2 = 0
                cat_2_dic[cat_1] = value_2 + match_pairs[match_pair]
                cat_pairs[cat_2] = cat_2_dic
            logging.debug('finish getting cat pairs, cat_pairs size: %d' % len(cat_pairs))
            return cat_pairs

        def calc(self):
            cat_pairs = self.get_cat_pair()
            logging.debug('calc cat similarity')
            cat_similarities = {}
            for cat in cat_pairs.keys():
                cat_similarity = {}
                total_count = 0
                for another_cat in cat_pairs[cat].keys():
                    total_count += cat_pairs[cat][another_cat]
                for another_cat in cat_pairs[cat].keys():
                    count = cat_pairs[cat][another_cat]
                    similarity = 1.0*count/total_count
                    cat_similarity[another_cat] = similarity
                cat_similarities[cat] = cat_similarity
            logging.debug('finish calc cat similarity, cat_similarities size: %d' % len(cat_similarities))
            return cat_similarities

    class WordSim:
        def __init__(self, dim_items, match_pairs):
            self.dim_items = dim_items
            self.match_pairs = match_pairs

        def get_word_pair(self):
            logging.debug('get word pairs')
            word_pairs = {}
            for match_pair in match_pairs.keys():
                item_1, item_2 = match_pair.split(',')
                terms_1 = self.dim_items[item_1].terms
                terms_2 = self.dim_items[item_2].terms
                for word_1 in terms_1:
                    for word_2 in terms_2:
                        try:
                            word_1_pair = word_pairs[word_1]
                        except:
                            word_1_pair = {}
                        try:
                            count = word_1_pair[word_2]
                        except:
                            count = 0
                        word_1_pair[word_2] = count + 1
                        word_pairs[word_1] = word_1_pair

                        try:
                            word_2_pair = word_pairs[word_2]
                        except:
                            word_2_pair = {}
                        try:
                            count = word_2_pair[word_1]
                        except:
                            count = 0
                        word_2_pair[word_1] = count + 1
                        word_pairs[word_1] = word_2_pair
            logging.debug('finish getting word pairs, word_pairs size: %d' % len(word_pairs))
            return word_pairs

        def calc(self):
            word_pairs = self.get_word_pair()
            logging.debug('calc word similarity')
            word_similarities = {}
            for word in word_pairs.keys():
                word_similarity = {}
                total_count = 0
                for another_word in word_pairs[word].keys():
                    total_count += word_pairs[word][another_word]
                for another_word in word_pairs[word].keys():
                    count = word_pairs[word][another_word]
                    if count > 10:
                        similarity = 1.0*count/total_count
                        word_similarity[another_word] = similarity
                word_similarities[word] = word_similarity
            logging.debug('finish calc word similarity, word_similarity size: %d' % len(word_similarities))
            return word_similarities


if __name__ == '__main__':
    filename = "c:\Users\SunderLab\Documents\myfile\cloth_matching_challenge\data\dim_items.txt"
    di = DimItems(filename)
    dims = di.read_in()
    filename = "c:\Users\SunderLab\Documents\myfile\cloth_matching_challenge\data\dim_fashion_matchsets.txt"
    ms = MatchSets(filename)
    match_pairs = ms.get_match_pairs()

    cs = CalcSimilarity()
    # css = cs.CatSim(dims, match_pairs)
    # cat_sim = css.calc()
    # print cat_sim['399']

    csw = cs.WordSim(dims, match_pairs)
    word_sim = csw.calc()
