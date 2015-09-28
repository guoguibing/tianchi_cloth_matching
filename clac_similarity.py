# coding = utf-8

from my_const import *
from dim_items import *
from dim_fashion_matchsets import *
from my_const import *
import os
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    filename='cloth_matching.log',
                    filemode='w')


class CalcSimilarity:
    def write_to_file(self, similarity, filename):
        logging.debug("saving file: " + filename)
        f = open(filename, 'w')
        for obj_1 in similarity.keys():
            for obj_2 in similarity[obj_1]:
                value = similarity[obj_1][obj_2]
                f.write(obj_1 + ',' + obj_2 + ',' + str(value) + '\n')
        f.close()
        logging.debug("finish saving")

    class CatSim:
        def __init__(self, dim_items, match_pairs, out_filename):
            self.dim_items = dim_items
            self.match_pairs = match_pairs
            self.out_filename = out_filename

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
                cat_1_dic[cat_2] = value_1 + self.match_pairs[match_pair]
                cat_pairs[cat_1] = cat_1_dic

                try:
                    cat_2_dic = cat_pairs[cat_2]
                except:
                    cat_2_dic = {}
                try:
                    value_2 = cat_2_dic[cat_1]
                except:
                    value_2 = 0
                cat_2_dic[cat_1] = value_2 + self.match_pairs[match_pair]
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
            CalcSimilarity.write_to_file(CalcSimilarity(), cat_similarities, self.out_filename)
            return cat_similarities

    class WordSim:
        def __init__(self, dim_items, match_pairs, out_filename):
            self.dim_items = dim_items
            self.match_pairs = match_pairs
            self.out_filename = out_filename

        def get_word_pair(self):
            logging.debug('get word pairs')
            word_pairs = {}
            for match_pair in self.match_pairs.keys():
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
            CalcSimilarity.write_to_file(CalcSimilarity(), word_similarities, self.out_filename)
            return word_similarities

    class TermSim:
        def __init__(self, dim_items, word_similarities, test_filename, out_filename):
            self.dim_items = dim_items
            self.word_similarities = word_similarities
            self.test_filename = test_filename
            self.out_filename = out_filename
            os.makedirs(out_filename)

        def calc(self):
            logging.debug('calc term similarity')
            items = []
            for line in open(self.test_filename, 'r'):
                item = line.strip()
                items.append(item)
            for i in range(0, len(items)):
                out_file = open(self.out_filename + items[i], 'a')
                for j in range(0, len(items)):
                    item = items[i]
                    another_item = items[j]

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
                    out_file.write( another_item + ',' + str(term_sim) + '\n')
                out_file.close()
            logging.debug('finish calc term similarity')

if __name__ == '__main__':
    di = DimItems(FilePath.dim_items_filename)
    dims = di.read_in()
    ms = MatchSets(FilePath.dim_fashion_matchsets_filename)
    match_pairs = ms.get_match_pairs()

    cs = CalcSimilarity()
    css = cs.CatSim(dims, match_pairs, FilePath.cat_similarities_filename)
    cat_sim = css.calc()

    csw = cs.WordSim(dims, match_pairs, FilePath.word_similarities_filename)
    word_sim = csw.calc()

    cst = cs.TermSim(dims, word_sim, FilePath.test_items_filename, FilePath.term_similarities_filename)
    cst.calc()
