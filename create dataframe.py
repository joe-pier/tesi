import os
import pandas as pd
import re

folders = []
names = os.listdir()
for i in names:
    if i.startswith('TXT'):
        folders.append(i)

def get_file_names(folder):
  return os.listdir(folder)

def get_cik_date(file):
  cik = re.findall(r"CIK__([0-9]*)", file)[0].zfill(10)
  date = re.findall(r"date__(([0-9]*)-([0-9]*)-([0-9]*))", file)[0][0]
  serial = re.findall(r"serial__([0-9]*)", file)[0]
  return (cik, date, serial)

def get_text(file):
  get_text.counter +=1
  print(get_text.counter, end = "\r")
  with open(file) as f:
    lines = f.readlines()
  return lines
get_text.counter = 0

print("getting file names")
file_names = list(map(get_file_names,folders))
print(sum([len(t) for t in file_names]))

folder_names = list(zip(folders,file_names))

print("get cik date serial")
cik_date_folder = [[get_cik_date(i) for i in j] for k,j in folder_names]

print("get text")
texts = [[get_text(f"{k}/{i}") for i in j] for k,j in folder_names]

print("DONE")
print(len(cik_date_folder))
print(len(texts))
print(sum([len(t) for t in texts]))

print("create dictionary")
test = [dict(zip(cik_date_folder[i], texts[i])) for i,n in enumerate(folders)]

sum([len(t) for t in test])

print("create dataframe")
df = pd.DataFrame(test)
print("quack")

df = df.ffill().bfill().head(1).T


print("making transformations")
df_reset = df.reset_index()

print("renaming columns")
df_reset = df_reset.rename({"index": "cik_date", 0:"text"}, axis = 1)
print("reset index")
df_reset[['cik','dates', 'serial']] = pd.DataFrame(df_reset['cik_date'].tolist(),index=df_reset.index)

df_complete = df_reset.drop("cik_date", axis = 1)

print("concat text")
def concat_list(text_as_list):
    return " ".join(text_as_list)

df_complete["text"] = df_complete["text"].apply(concat_list)

