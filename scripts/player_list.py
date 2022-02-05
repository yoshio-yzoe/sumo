#力士個々人の通算成績を出す

import ssl
from urllib.request import urlopen
import urllib.error
import pandas as pd
from bs4 import BeautifulSoup


class player_list:
    def __init__(self, id):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.id = str(id)
        self.url = "http://sumodb.sumogames.de/Rikishi.aspx?r=" + self.id + "&l=j"
    def main(self):
        try:
            html = urlopen(self.url)
            bsObj = BeautifulSoup(html, "html.parser")
            table = bsObj.findAll("table", {"class": "rikishi"})[0]
        except IndexError:
            return
        # テーブルを指定
        rows = table.findAll("tr")[1:]
        year = []
        month = []
        yusho = []
        banduke = []
        shohai = []
        kaisuu = []
        datayeah = []
        number = list(range(1,16))
        for row in rows:
            datarow = []

            for cell in row.findAll(['td']):
                datacolumn = []
                if cell.contents == []:
                    continue
                else:
                    if len(cell.contents) >= 2:
                        for hoshi in cell.contents:
                            chip = str(hoshi)
                            if (chip == '<img border="0" src="img/hoshi_shiro.gif"/>' or chip == '<img border="0" src="img/hoshi_fusensho.gif"/>'):
                                datacolumn.append("win")
                            elif (chip == '<img border="0" src="img/hoshi_kuro.gif"/>' or chip == '<img border="0" src="img/hoshi_fusenpai.gif"/>'):
                                datacolumn.append("lose")
                            elif (chip == '<img border="0" src="img/hoshi_hikiwake.gif"/>'):
                                datacolumn.append("draw")
                            elif (chip == '<img border="0" src="img/hoshi_yasumi.gif"/>'):
                                datacolumn.append("yasumi")
                        if datacolumn != []:
                            datayeah.append(datacolumn)
                    else:
                        con = cell.findAll("a")
                        for cont in con:
                            if "Banzuke.aspx?" in str(cont):
                                year.append(int(str(cont.get("href"))[15:19]))
                                month.append(str(cont.get("href"))[19:21])
                        text = cell.get_text().split()
                        datarow.extend(text)
            if datarow != []:
                if len(datarow) == 2:
                    banduke.append(datarow[1])
                    shohai.append(None)
                    yusho.append(None)
                    kaisuu.append(None)
                else:
                    banduke.append(datarow[1])
                    shohai.append(datarow[2])
                    if len(datarow) >= 6:
                        if (datarow[4] == "優勝"):
                            yusho.append("優勝")
                        elif (datarow[4] == "準優勝"):
                            yusho.append("準優勝")
                        else:
                            yusho.append(None)
                        if "回" in datarow[5]:
                            kaisuu.append(int(datarow[5][1:].split('回')[0]))
                        else:
                            kaisuu.append(None)
                    else:
                        yusho.append(None)
                        kaisuu.append(None)


        df1 = pd.DataFrame(datayeah, columns = number)
        columns = ["year", "month", "banduke", "shohai", "yusho", "kaisu"]
        df2 = pd.DataFrame(data = {"year": year, "month": month, "banduke": banduke, "shohai": shohai, "yusho": yusho, "kaisu": kaisuu}, columns=columns)
        if len(df1) == len(df2):
            df = pd.concat([df2, df1], axis=1)
        else:
            minus = len(df2) - len(df1)
            nondatadf = pd.DataFrame([[None] * 15] * minus, columns=number)
            df3 = pd.concat([nondatadf, df1]).reset_index()
            df = pd.concat([df2, df3], axis=1)
        df.to_csv("../rikishi_data/" + self.id + ".csv" , encoding="utf-8")

if __name__ == '__main__':
    exceptlist = []
    httplist = []
    #11898から
    for num in range(11910, 12659):

        rikishi = player_list(num)
        try:
            rikishi.main()
        except urllib.error.HTTPError as e:
            httplist.append(num)
            #print(e.cide)
            print(httplist)
        except ValueError:
            exceptlist.append(num)
            print(exceptlist)
        print(num)
    print(exceptlist)