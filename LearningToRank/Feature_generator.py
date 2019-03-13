import pandas as pd
import csv
import pyltr
import numpy as np
import datetime
import re
import time
import dawg
from nltk import ngrams
from heapq import nlargest
from operator import itemgetter

with open('../data/ngram_dict.csv', mode='r') as infile:
    reader = csv.reader(infile)
#     ngram_dict = {rows[0]:rows[1] for rows in reader}
    ngram_data=[tuple([line[0], int(line[1])]) for line in reader if int(line[1])>2]
ngram_dict = dawg.IntCompletionDAWG(ngram_data)
# prefix_suffix_pairs_background = pd.read_csv("../data/prefix_suffix_pairs.txt")

# Importing all the necessary dictionaries
suffixes = pd.read_csv("../data/Freq_background.csv", index_col='Unnamed: 0')
with open('../data/sorted_popular_queries.csv', mode='r') as infile:
    reader = csv.reader(infile)
    skipheader = next(reader)
    data=[tuple([line[1], int(line[2])]) for line in reader if int(line[2])>2]
sortedpopulardict = dawg.IntCompletionDAWG(data)


data = []
ngram_data = []

## Change this for other top10k, top100k of nothing
top100k = suffixes.iloc[range(100000),:]
suffixes = []
top100ktuple = [tuple(x) for x in top100k.values]
# top100ktuple = [tuple([line["0"], int(line["counts"])])]
top100kdict = dawg.IntCompletionDAWG(top100ktuple)
top100k = []


# In[3]:



def get_single_ngram_features(query_input, ngram_dict):
    ngram_scores = [0,0,0,0,0,0]

    for n in range(1,7):

        sixgrams = ngrams(query_input.split(), n)
        for grams in sixgrams:
            try:
                ngram_scores[n-1] = ngram_scores[n-1] + ngram_dict.get(' '.join(grams),0)
            except:
                pass
    return ngram_scores

def get_ngram_features(inputs, ngram_dict):
    results = [[get_single_ngram_features(x, ngram_dict)] for x in inputs];
    return results


# In[4]:


# Read in training data
removed_session_training = pd.read_csv('/media/root/TINI 2/dataIR/removed_session_validation.csv', header=None, index_col=[0])
removed_session_training[1] = removed_session_training[1].str.replace('[\W_]+', ' ')


# In[52]:


## Process training
training_queries = removed_session_training.reset_index(drop=True)
candidate_prefixes = []
right_query = []

amount_of_suffix_splits = 5
for j in range(len(training_queries)):
    current_query = str(training_queries[1][j])
    split_query = current_query.split(" ")
    suffix = ' '.join(split_query[1:])
    prefix = split_query[0] + " "

    for i in np.unique(np.linspace(0, len(suffix), amount_of_suffix_splits).astype(int)):
        candidate_prefixes.append(prefix + suffix[:i])
        right_query.append(current_query)

print("done")
candidate_prefixes


# In[ ]:


# Run this to clear memory
all_candidates = []
relevant_candidate = []
qids =  []
ngram_features =  []


# In[ ]:


all_candidates = []
relevant_candidate = []
qids =  []
ngram_features =  []

time_taken_top100k = 0
split_time = 0
appendtime = 0
ngramtime = 0
real_query_time = 0
total_time_begin = time.time()
checkpoint_time = time.time()
with open('../data/training_feature_validation.csv','w') as file:
    for candidate_prefix_i in range(len(candidate_prefixes)):
        if candidate_prefix_i % 10000 == 0:
            end_checkpoint = time.time() - checkpoint_time
            print("Time between checkpoints: " + str(end_checkpoint))
            print("Total time elapsed: " + str(time.time() - total_time_begin))
            print(str(candidate_prefix_i) + '/' + str(len(candidate_prefixes)))
            checkpoint_time = time.time()

        candidate_prefix = candidate_prefixes[candidate_prefix_i]
        original_query = right_query[candidate_prefix_i]

    #     Getting the endterm for every prefix
        split_time_start = time.time()
        splitted = re.split('[\W_]+',candidate_prefix)
        if candidate_prefix[len(candidate_prefix)-1] == ' ':
            endterm = splitted[len(splitted)-2] + " "
        else:
            endterm = splitted[len(splitted)-1]
        split_time = split_time + time.time() - split_time_start

        # Creating the synthetic candidates
        start = time.time()
        top10suffix = nlargest(10, top100kdict.items(prefix=candidate_prefix), key=itemgetter(1))
        out = [i[0] for i in top10suffix]
        preprefix = candidate_prefix[:-len(endterm)]
        outcombined1 = [preprefix + s for s in out]
        time_taken_top100k = time_taken_top100k + time.time() - start

        current_candidates = outcombined1

        # Getting the top # real queries
        realquerystart = time.time()
        if not(candidate_prefix == "www " or candidate_prefix == "http "):
            top50queries = nlargest(25, sortedpopulardict.items(prefix=candidate_prefix), key=itemgetter(1))
            keys_pop = [i[0] for i in top50queries]
            current_candidates.extend(keys_pop)
        real_query_time = real_query_time + time.time() - realquerystart

        current_relevant_candidates = [s == original_query for s in current_candidates]

        # Appending
#         append_time_start = time.time()
#         all_candidates.extend(current_candidates)
#         relevant_candidate.extend()
#         qids.extend(np.ones(len(current_candidates)) * candidate_prefix_i)
#         appendtime = appendtime + time.time() - append_time_start

#         # Creating features
#         ngram_time_start = time.time()
#         ngram_features.extend(get_ngram_features(current_candidates, ngram_dict))
#         ngramtime = ngramtime + time.time() - ngram_time_start

        feature_vector = get_ngram_features(current_candidates, ngram_dict)
        for i in range(len(feature_vector)):
            file.write(str(feature_vector[i][0]) + ";" + str(int(current_relevant_candidates[i])) + ";" + str(current_candidates[i]) + ";" + str(candidate_prefix_i))
            file.write('\n')
total_time = time.time() - total_time_begin

print("Total time: " + str(total_time))
print("Top100k suffix time: " + str(time_taken_top100k))
print("Total split time: " + str(split_time))
print("Total append time: " + str(appendtime))
print("Total ngram time: " + str(ngramtime))
print("Total real query time: " + str(real_query_time))
