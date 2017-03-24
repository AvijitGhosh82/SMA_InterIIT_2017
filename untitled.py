import csv
f = open('IBM_out.csv', 'r')
df = csv.reader(f, delimiter=',')
data = []
for a in df:
    data.append(a)

headers = data[0]
data = data[1:]
dict_ = {}
dict_["IBM"] = {}
dict_["IBM"]["title"] = {}
dict_["IBM"]["events"] = []


subdict = {}
subdict["media"] = {}
subdict["media"]["url"] = ""
subdict["media"]["caption"] = ""
subdict["media"]["credit"] = ""
subdict["text"] = {}
subdict["text"]["headline"] = "stock"
subdict["text"]["text"] = "ticker"
dict_["IBM"]["title"] = subdict

def get_img(a ,b):
    return ""

for a in data:
    subdict = {}
    subdict["media"] = {}
    subdict["media"]["url"] = get_img(a[39], a[len(a) - 1])
    subdict["media"]["caption"] = "Score Analyse"
    subdict["media"]["credit"] = a[5]
    subdict["text"] = {}
    subdict["text"]["headline"] = a[7]
    subdict["text"]["text"] = "<p>" +  a[3] +"</p>"
    dict_["IBM"]["events"].append(subdict)

import json
fp = open('test_out.json' , 'w')
json.dump(dict_["IBM"], fp)