# encoding = utf-8

from clac_similarity import *


class Predict:
    def __init__(self, test_filename, dim_items_filename, cat_similarities_filename, term_similarities_filename, rate):
        self.test_filename = test_filename
        self.dim_item_filename = dim_items_filename
        self.term_similarities_filename = term_similarities_filename
        self.rate = rate
        # get dim_items
        di = DimItems(FilePath.dim_items_filename)
        self.dim_items = di.read_in()
        # get cat similarities
        logging.debug('get cat similarities')
        cat_similarities = {}
        for line in open(cat_similarities_filename, 'r'):
            line = line.strip()
            item, another_item, sim = line.split(',')
            cat_similarities[item + ',' + another_item] = float(sim)
            cat_similarities[another_item + ',' + item] = float(sim)
        self.cat_similarities = cat_similarities

    def predict(self):
        logging.debug('predict start')
        f = open(FilePath.fm_submissions_filename, 'w+')
        num = 0
        for line in open(self.test_filename):
            item = line.strip()
            similarities = self.get_similarity(item)

            to_write = item + ' '
            max_num = 199
            if max_num > len(similarities):
                max_num = len(similarities)
            for i in range(0, max_num):
                item = similarities[i][0]
                to_write += item + ','
            f.write(to_write[:-1] + '\n')

            num += 1
            if num % 20 == 0:
                print str(num) + '/5484'
        f.close()
        logging.debug('finish predicting')

    def get_similarity(self, item):
        term_similarity = {}
        for line in open(self.term_similarities_filename + item):
            line = line.strip()
            another_item, sim = line.split(',')
            term_similarity[another_item] = float(sim)

        similarities = {}
        for another_item in self.dim_items.keys():
            # if another_item == item:
            #     continue
            try:
                if self.cat_similarities[self.dim_items[item].cat + ',' + self.dim_items[another_item].cat] > 0.01:
                    item_sim = self.get_item_similarity(item, another_item, term_similarity)
                    similarities[another_item] = item_sim
            except KeyError:
                continue
        similarities = sorted(similarities.iteritems(), key=lambda temp: temp[1], reverse=True)
        return similarities

    def get_item_similarity(self, item, another_item, term_similarity):
        cat = self.dim_items[item].cat
        another_cat = self.dim_items[another_item].cat
        key = cat + ',' + another_cat
        try:
            cat_sim = self.cat_similarities[key]
        except KeyError:
            cat_sim = 0

        try:
            term_sim = term_similarity[another_item]
        except KeyError:
            term_sim = 0
        return self.rate*cat_sim + (1-self.rate)*term_sim

if __name__ == '__main__':
    rate = 0
    p = Predict(FilePath.test_items_filename,
                FilePath.dim_items_filename,
                FilePath.cat_similarities_filename,
                FilePath.term_similarities_filename,
                rate)
    p.predict()
