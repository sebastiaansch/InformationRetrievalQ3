from pytrie import SortedStringTrie as Trie
import dawg
import csv
ngram_dict = []
with open('../data/ngram_dict.csv', mode='r') as infile:
    reader = csv.reader(infile)
