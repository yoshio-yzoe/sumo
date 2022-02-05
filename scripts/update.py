#データをアップデートするために、現役力士のIDを全部取得する

import pandas as pd
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import re
import player_list

class update:
    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.url = "http://sumodb.sumogames.de/Banzuke.aspx?l=j"

    def active_list(self): #現役力士のID一覧出力
        try:
            html = urlopen(self.url)
            bsObj = BeautifulSoup(html, "html.parser")
            link = bsObj.find_all('a')
            list = []
            for li in link:
                if 'Rikishi.aspx?r=' in str(li):
                    list.append(int(re.split('[=&]', str(li.get("href")))[1]))
        except:
            pass
        return np.array(list)

    def update(self):
        activelist = self.active_list()
        for id in activelist:
            rikishi = player_list.player_list(id)
            rikishi.main()
            print(id)

if __name__ == '__main__':
    update = update()
    update.update()