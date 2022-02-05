import ssl
from urllib.request import urlopen
import requests
from pathlib import Path
import img2pdf
import urllib.error
import pandas as pd
from bs4 import BeautifulSoup
import os


class mangadl:
    def __init__(self, url):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.url = url
    def main(self):
        urllist = self.url_list()
        volume = 13
        for link in urllist:
            self.gatherimg(link, volume)
            volume -= 1
    def gatherimg(self, link, volume):
        try:
            html = urlopen(link)
            bsObj = BeautifulSoup(html, "html.parser")
            table = bsObj.findAll("img", {"class": "attachment-large size-large"})
            tablex = [image['src'] for image in table]

            count = 0
            for img in tablex:
                save_path = "D:/ScanSnap/library/漫画/賭博破戒録カイジ/" + str(volume) + "/"
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                file_name = str(count).zfill(3) + '.jpg'
                response = requests.get(img)
                open(save_path + file_name, 'wb').write(response.content)
                count += 1
        except IndexError:
            return
        print(save_path)
    def gotopdf(self):
        base_path = "D:/ScanSnap/library/漫画/賭博破戒録カイジ/"
        glob = Path(base_path).glob("*")
        imagefolderlist = list([item for item in list(glob) if item.is_dir()])
        outputpathlist = list([item.with_name(item.name + ".pdf") for item in imagefolderlist])
        for outputpath, imagepath in zip(outputpathlist, imagefolderlist):
            try:
                lists = list(imagepath.glob("**/*"))  # 単フォルダ内を検索
                # pdfを作成
                with open(outputpath, "wb") as f:
                    f.write(img2pdf.convert([str(i) for i in lists if i.match("*.jpg") or i.match("*.png")]))
                print(outputpath.name + " :Done")
            except:
                pass

    def url_list(self):
        try:
            html = urlopen(self.url)
            bsObj = BeautifulSoup(html, "html.parser")
            link = bsObj.find_all('a')
            list = []
            for li in link:
                if '第' in str(li):
                    list.append(li.get('href'))

            return list
        except:
            pass
if __name__ == '__main__':

    url = "https://mangabank.org/dp/%E8%B3%AD%E5%8D%9A%E7%A0%B4%E6%88%92%E9%8C%B2%E3%82%AB%E3%82%A4%E3%82%B8/"
    mangadl = mangadl(url)
    #mangadl.main()
    mangadl.gotopdf()
    #mangadl.gatherimg("https://mangabank.org/1281331/", 7)
    print('finish')

