#星取表作成

import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import os
import re

class sumo_to_csv:
    def __init__(self, year, month, day):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.year = str(year)
        self.month = month
        self.day = str(day)
        self.url = "http://sumodb.sumogames.de/Results.aspx?b=" + self.year + self.month + "&d=" + self.day + "&l=j"


    def save_file_at_new_dir(self, new_dir_path, new_filename, new_file_content, mode='w'):
        os.makedirs(new_dir_path, exist_ok=True)
        with open(os.path.join(new_dir_path, new_filename), mode) as f:
            f.write(new_file_content)

    def get_table(self):
        try:
            html = urlopen(self.url)
            bsObj = BeautifulSoup(html, "html.parser")
            table = bsObj.findAll("table", {"class": "tk_table"})[0] #0:幕内、1:十両、2:幕下、3:三段目、4:序二段、5:序の口
        except IndexError:
            return
        # テーブルを指定
        rows = table.findAll("tr")[1:]
        self.title = table.findAll("tr")[0].find('td').get_text()


        higashi_hoshi = []
        higashi_banduke = []
        higashi_shikona = []
        kimarite = []
        nishi_banduke = []
        nishi_shikona = []
        nishi_hoshi = []
        higashi_id = []
        nishi_id = []
        for row in rows:
            datarow = []
            i = 0
            for cell in row.findAll(['td', 'th']):
                chip = str(cell.contents[0])
                if (chip == '<img border="0" src="img/hoshi_shiro.gif"/>' or chip == '<img border="0" src="img/hoshi_fusensho.gif"/>'):
                    datarow.append("win")
                elif (chip == '<img border="0" src="img/hoshi_kuro.gif"/>' or chip == '<img border="0" src="img/hoshi_fusenpai.gif"/>'):
                    datarow.append("lose")
                elif (chip == '<img border="0" src="img/hoshi_hikiwake.gif"/>'):
                    datarow.append("draw")
                else :
                    con = cell.findAll("a")
                    for cont in con:
                        if "Rikishi.aspx?" in str(cont):
                            id = int(str(cont.get("href"))[15:-4])
                            if i == 1:
                                nishi_id.append(id)
                            if i == 0:
                                higashi_id.append(id)
                                i = 1
                    #print(con)
                    #print(str(cell.contents[3])) #0:番付　1;決まりて　2:しこ名(title)
                    #kimarite = str(cell.contents[1]).split()[1]
                    #con = str(cell.contents[2])
                    #print(con)
                    #if con.p is not None:
                        #print("Yes")
                    text = cell.get_text().split()
                    datarow.extend(text)
            datarow[2] = re.split('[0123456789]', datarow[2])[0]
            datarow[-3] = re.split('[0123456789]', datarow[-3])[0]
            datarow[4] = re.split('[0123456789]', datarow[4])[0]
            datarow = [d for d in datarow if "(" not in d]
            higashi_hoshi.append(datarow[0])
            higashi_banduke.append(datarow[1])
            higashi_shikona.append(datarow[2])
            kimarite.append(datarow[3])
            nishi_banduke.append(datarow[4])
            nishi_shikona.append(datarow[5])
            nishi_hoshi.append(datarow[6])

            print(datarow)
            #writer.writerow(csvRow)
        columns = ["higashi_hoshi", "higashi_banduke", "higashi_shikona", "higashi_id", "kimarite", "nishi_banduke", "nishi_shikona", "nishi_id", "nishi_hoshi"]
        df = pd.DataFrame(data = {"higashi_hoshi": higashi_hoshi, "higashi_banduke": higashi_banduke, "higashi_shikona": higashi_shikona, "higashi_id": higashi_id, "kimarite": kimarite, "nishi_banduke": nishi_banduke, "nishi_shikona":nishi_shikona, "nishi_id":nishi_id, "nishi_hoshi": nishi_hoshi}, columns=columns)
        return df

    def csv_maker(self):
        df = self.get_table()
        if df is None:
            return
        else:
            directory = "../data/"+ str(self.year) + "/" + self.month + "/" + self.title
            csv_name = str(self.day) + ".csv"
            if not os.path.exists(directory):
                os.makedirs(directory)
            full_name = os.path.join(directory, csv_name)
            if df is not None:
                df.to_csv(full_name, encoding="utf-8")


if __name__ == '__main__':

    #years = list(range(1958,1978))  # 1909から あとで1979の3月から
    years = [2020, 2021]
    #十両　1979以前
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    #months = ["01", "03", "05", "07", "09", "11"]
    days = list(range(1,16))
    for year in years:
        for month in months:
            for day in days:
                csvname = "../data/"+ str(year) + "/" + month + "/" + "十両/" + str(day) + ".csv"
                if (os.path.exists(csvname) == True):
                    continue
                else:
                    sumo = sumo_to_csv(year, month, day)
                    sumo.csv_maker()
        print(str(year)+"done")
    """

    year = 1997
    month = "11"
    days = list(range(9,16))
    for day in days:
        sumo = sumo_to_csv(year, month, day)
        sumo.csv_maker()
    """