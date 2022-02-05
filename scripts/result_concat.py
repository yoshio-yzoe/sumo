
import pandas as pd
import codecs
import csv
basedir = "../data/"
higashi_hoshi = []
higashi_id = []
nishi_hoshi = []
nishi_id = []
columns = ["higashi_hoshi", "higashi_id", "nishi_hoshi", "nishi_id"]

def main1():
    for year in range(1958, 2022):
        for month in ["01", "03", "05", "07", "09", "11"]:
            for day in range(1, 16):
                filename = basedir + str(year) + "/" + str(month) + "/幕内/" + str(day) + ".csv"
                try:
                    with codecs.open(filename, "r", "Shift-JIS", "ignore") as file:
                        df = pd.read_csv(file, usecols=columns)
                        higashi_hoshi.extend(df["higashi_hoshi"])
                        higashi_id.extend(df["higashi_id"])
                        nishi_hoshi.extend(df["nishi_hoshi"])
                        nishi_id.extend(df["nishi_id"])
                except FileNotFoundError:
                    continue
        print(str(year) + "done")
    df2 = pd.DataFrame(data = {"higashi_hoshi": higashi_hoshi, "higashi_id": higashi_id, "nishi_hoshi": nishi_hoshi, "nishi_id":nishi_id}, columns=columns)
    df2.to_csv(basedir+"summary/summary.csv", encoding="utf-8")

def main2():

    from collections import defaultdict
    from functools import partial
    import numpy as np
    file = "../data/summary/summary.csv"
    #counter = defaultdict(int)
    counter = defaultdict(partial(np.array, [0, 0]))
    with open(file) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if int(row[2]) < int(row[4]):
                key = tuple([row[2], row[4]])
                if row[1] == 'win':
                    counter[key] += np.array([1,0])
                elif row[1] == 'lose':
                    counter[key] += np.array([0,1])
            else:
                key = tuple([row[4], row[2]])
                if row[3] == 'win':
                    counter[key] += np.array([1,0])
                elif row[3] == 'lose':
                    counter[key] += np.array([0,1])
    return counter

def write_csv(file, save_dict):
    save_row = {}
    higashi_id = []
    nishi_id = []
    higashi_wins = []
    higashi_loses = []
    for key, value in save_dict.items():
        higashi_id.append(key[0])
        nishi_id.append(key[1])
        higashi_wins.append(value[0])
        higashi_loses.append(value[1])

    columns = ["higashi_id", "nishi_id", "higashi_wins", "higashi_loses"]
    df = pd.DataFrame(
        data={"higashi_id": higashi_id, "nishi_id": nishi_id, "higashi_wins": higashi_wins, "higashi_loses": higashi_loses},
        columns=columns)

    df.to_csv(file)




if __name__ == '__main__':

    write_csv("../data/summary/history.csv", main2())