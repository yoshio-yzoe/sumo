#力士IDとしこ名の紐づけ

import pandas as pd
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np

class rikishi_data:
    def __init__(self, id):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.id = str(id)
        self.url = "http://sumodb.sumogames.de/Rikishi.aspx?r=" + self.id + "&l=j"
    def main(self):
        try:
            html = urlopen(self.url)
            bsObj = BeautifulSoup(html, "html.parser")
            title = bsObj.find("title").get_text()
            shikona = str(title).split()[0]
            table = bsObj.findAll("table", {"class": "rikishidata"})[0]
        except IndexError:
            return
        rows = table.findAll("tr")[1:]
        alllist = [['id', int(self.id)], ['四股名',shikona]]
        for row in rows:
            mocklist = [(cell.get_text().replace('\u3000', ' ').replace('\xa0', '')).strip() for cell in row.findAll(['td'])]
            if len(mocklist) == 2:
                alllist.append(mocklist)
        print(np.array(alllist))
    def id_to_shikona(self):
        try:
            html = urlopen(self.url)
            bsObj = BeautifulSoup(html, "html.parser")
            title = bsObj.find("title").get_text()
            return str(title).split()[0] #四股名
        except IndexError:
            return



if __name__ == '__main__':

    """
    shikonalist = []
    N = 12659 #最新力士
    #11898～11909はなぜかなし
    for num in range(1, N):
        rikishi = rikishi_data(num)

        shikona = rikishi.id_to_shikona()
        shikonalist.append(shikona)
        #print(num, shikona)
    df = pd.DataFrame(data={'id': range(1, N), '四股名': shikonalist})
    df.to_csv("../id/id.csv")
    """

    df = pd.read_csv("../id/id.csv")
    print(df.head())

