# coding:utf-8

'''
记录每个商品信息的类
'''


class Dim:
    def __init__(self, item, cat, terms):
        self.item = item
        self.cat = cat
        self.terms = terms

'''
读取并返回每商品的信息
'''
import logging


class DimItems:
    def __init__(self, filename):
        self.filename = filename

    def read_in(self):
        logging.debug("read in dim items")
        dims = {}
        num = 0
        for line in open(self.filename):
            line = line[:-1]
            item, cat, name = line.split(" ")
            terms = name.split(",")
            dims[item] = Dim(item, cat, terms)
            # print item, cat, name, terms
            # print num
            # num += 1
            # if num == 2:
            #     break
        logging.debug("finish reading dim items")
        return dims


if __name__ == "__main__":
    filename = "c:\Users\SunderLab\Documents\myfile\cloth_matching_challenge\data\dim_items.txt"
    di = DimItems(filename)
    dims = di.read_in()
    print dims['41'].cat
