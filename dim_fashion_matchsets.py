# coding:utf-8
import logging
from my_const import *

class MatchSets:

    def __init__(self, filename):
        self.filename = filename

    def read_in(self):
        logging.debug("read in matchsets")
        match_sets = []
        for line in open(self.filename):
            line = line[:-1]
            match_set = []
            number, a_set = line.split(" ")
            parts = a_set.split(";")
            for part in parts:
                match_set.append(part.split(","))
            match_sets.append(match_set)
        logging.debug("finish reading matchsets, match_sets size: %d" % len(match_sets))
        return match_sets

    def get_match_pairs(self):
        match_sets = self.read_in()
        logging.debug("get match pairs")
        match_pairs = {}
        for match_set in match_sets:
            for i in range(0, len(match_set) - 1):
                part = match_set[i]
                for j in range(i + 1, len(match_set) - 1):
                    another_part = match_set[j]
                    for item in part:
                        for another_item in another_part:
                            key = item + "," + another_item
                            try:
                                value = match_pairs[key]
                            except Exception:
                                value = 0
                            match_pairs[key] = value + 1
                            # match_pairs[another_item + "," + item] = value + 1
        logging.debug("finish geting match pairs, match_pairs size: %d" % len(match_pairs))
        return match_pairs

if __name__ == "__main__":
    ms = MatchSets(FilePath.dim_fashion_matchsets)
    ms.get_match_pairs()

