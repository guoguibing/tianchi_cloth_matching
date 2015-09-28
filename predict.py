# encoding = utf-8
from dim_items import *
from dim_fashion_matchsets import *
from my_const import *
from clac_similarity import *


class Predict:
    def __init__(self, test_filename, dim_items, cat_similarities, word_similarities, item_cat_sim_filename,
                 item_term_sim_filename):
        self.test_filename = test_filename
        self.dim_items = dim_items
        self.cat_similarities = cat_similarities
        self.word_similarities = word_similarities
        self.item_term_sim_file = open(item_term_sim_filename, 'w')
        self.item_cat_sim_file = open(item_cat_sim_filename, 'w')

    def predict(self):
        logging.debug('predict start')
        f = open(FilePath.fm_submissions_filename, 'w+')
        num = 0
        for line in open(self.test_filename):
            item = line.strip()
            similarities = self.get_similarity(item)

            to_write = item + ' '
            max = 199
            if max > len(similarities):
                max = len(similarities)
            for i in range(0, max):
                item = similarities[i][0]
                to_write += item + ','
            f.write(to_write[:-1] + '\n')

            num += 1
            if num % 100 == 0:
                print str(num) + '/5484'
        f.close()
        self.item_cat_sim_file.close()
        self.item_cat_sim_file.close()
        logging.debug('finish predicting')

    def get_similarity(self, item):
        similarities = {}
        for another_item in self.dim_items.keys():
            # if another_item == item:
            #     continue
            try:
                if self.cat_similarities[self.dim_items[item].cat][self.dim_items[another_item].cat] > 0.01:
                    item_sim = self.get_item_similarity(item, another_item)
                    similarities[another_item] = item_sim
            except KeyError:
                continue
        similarities = sorted(similarities.iteritems(), key=lambda temp: temp[1], reverse=True)
        return similarities

    def get_item_similarity(self, item, another_item):
        cat = self.dim_items[item].cat
        another_cat = self.dim_items[another_item].cat
        try:
            cat_sim = self.cat_similarities[cat][another_cat]
        except:
            cat_sim = 0
        return cat_sim + term_sim

if __name__ == '__main__':
    di = DimItems(FilePath.dim_items_filename)
    dims = di.read_in()
    ms = MatchSets(FilePath.dim_fashion_matchsets_filename)
    match_pairs = ms.get_match_pairs()
    cs = CalcSimilarity()
    csw = cs.WordSim(dims, match_pairs, FilePath.word_similarities_filename)
    word_sim = csw.calc()
    css = cs.CatSim(dims, match_pairs, FilePath.cat_similarities_filename)
    cat_sim = css.calc()
    p = Predict(FilePath.test_items_filename,
                dims,
                cat_sim,
                word_sim,
                FilePath.item_cat_sim_filename,
                FilePath.item_term_sim_filename)
    p.predict()
