#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import glob
import os
import re
import time
import datetime
import gc


# In[2]:


def get_suffix(inputstring):
    splitted = re.split('[\W_]+',str(inputstring))
    return_list = []
    for i in range(len(splitted)):
        return_list.append(' '.join(splitted[i:len(splitted)]))
    return return_list


# In[3]:


data_path = "data/aol-data/"
dir_list = sorted(os.listdir(data_path))
dir_list


# In[4]:
for current_file in range(10):
    print("Starting with reading file " + dir_list[current_file])

    df = pd.read_csv(data_path + "" +dir_list[current_file], delimiter="\t")
    df.columns
    print("Done with reading")

    start_time = time.time()
    print("Starting with processing")

    df['QueryTime'] = pd.to_datetime(df['QueryTime'])
    df['Diff'] = None
    previousQuery = ""
    previousQuery = ""

    matrixding = df.values
    df = []
    del df
    gc.collect()

    for i in range(1,len(matrixding)):
        if matrixding[i,1] == matrixding[i-1,1]:
            matrixding[i, 5] = matrixding[i,2]-matrixding[i-1,2]

    elapsed_time = time.time() - start_time
    print(elapsed_time)


    # In[ ]:

    print("Starting with writing")

    np.savetxt("data/resulting" + str(current_file) + ".csv", matrixding, delimiter="\t", fmt="%s")


    print("Done with writing")
# In[ ]:
# In[ ]:
