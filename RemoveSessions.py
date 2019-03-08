import pandas as pd
import numpy as np
import datetime
import re

def get_suffix(inputstring):
    splitted = re.split('[\W_]+',str(inputstring))
    return_list = []
    for i in range(len(splitted)):
        return_list.append(' '.join(splitted[i:len(splitted)]))
    return return_list

print("Reading input")
df = pd.read_csv("data/combined_query.csv", delimiter="\t",header=None)
print(df.columns)

print("Converting Nones")
df.loc[df[5]=="None", 5] = "nan"
print("Converting timedeltas")
df[5] = pd.to_timedelta(df[5])
print("Converting datetime")
df[2] = pd.to_datetime(df[2])

resultaat = df[(df[2] >= "2006-05-29") & (df[2] <= "2006-06-11") & ~(df[5] <= datetime.timedelta(minutes=30))][1]
df = []
print("Removed session queries")
resultaat.to_csv("data/removed_session_testing.csv", index=False)

print("Done")

print("Splitting")
filename = "data/session_seperated_testing.txt"
file = open(filename,"w")

for query in resultaat:
    splitted = get_suffix(query)
    for suffix in splitted:
        if suffix == "":
            continue
        file.write(suffix + "\n")
file.close()
