import time
import requests
import csv
import re
from bs4 import BeautifulSoup

# 目標URL網址\存檔檔名模板
URL = "https://forum.gamer.com.tw/G1.php?bsn={}"
CSV_FILE = "output/{}.csv"
TXT_FILE = "output/{}.txt"

# 欲抓取之討論版清單
forums = [29220, 60076, 30861, 31406]
forums = [29220]

def get_resource(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
               "AppleWebKit/537.36 (KHTML, like Gecko)"
               "Chrome/84.0.4147.105 Safari/537.36"}
    return requests.get(url, headers=headers) 

def parse_html(html_str):
    return BeautifulSoup(html_str, "lxml")

def isDir(img_tag):
    return img_tag["class"][0] == "IMG-E14"

def title_rename(title):
    return re.sub(r"[\\\/:\*\?\"><\|]", "", title.strip().replace(" ", "_"))

def get_archive(soup, layer=0, parent_no=""):
    archive = []
    sleep_time = 1
    count = 0

    table = soup.find(class_="FM-stb1")
    title = ""
    if layer == 0:
        title = soup.find("title").text.replace("精華區 - 巴哈姆特", "")
        title = title_rename(title)
        print("開始分析 {} 的精華區目錄".format(title))
        archive.append(["編號", "主題", "網址", "更新日期"])
    for row in table.find_all("tr")[1:]:
        count += 1
        # print(row, end="\n\n")
        cells = row.find_all("td")
        entry_no = str(cells[0].string)
        if layer > 0:
            entry_no = "%s-%s" %(parent_no, entry_no)
        
        content = cells[1]
        entry_type = "Dir" if isDir(content.find("img")) else "File"
        content_str = "%s%s" %("    " * layer, content.find("a").string)
        link = "https://forum.gamer.com.tw/" + content.find("a")["href"]
        date = cells[4].string
        entry = [entry_no, content_str, link, date]
        archive.append(entry)
        if entry_type == "Dir": # Iterate into subdirectories
            # print("Sleeping for %d second(s)..." %sleep_time)
            time.sleep(sleep_time)
            child_archive, _ = web_scraping_bot(link, layer+1, entry_no)
            archive += child_archive
        
    return archive, title

def save_to_csv(archive, csv_file):
    with open(csv_file, "w+", newline="", encoding="utf8") as fp:
        print("儲存至 {}".format(csv_file))
        writer = csv.writer(fp)
        for entry in archive:
            writer.writerow(entry)

def save_to_txt(archive, txt_file):
    with open(txt_file, "w", newline="", encoding="utf-8") as fp:
        print("儲存至 {}".format(txt_file))
        fp.write("編號{} | 主題\n".format(" " * 16))
        for entry in archive[1:]:
            fp.write("{0:<20} | {1}\n".format(entry[0], entry[1]))

def web_scraping_bot(url, layer=0, parent_no=""):
    archive = []
    
    if layer == 0:
        print("抓取: 精華區根目錄資料中...")
    else:
        print("抓取: 第{}-{}層子目錄資料中...".format(parent_no, layer))
    r = get_resource(url)
    if r.status_code == requests.codes.ok:
        soup = parse_html(r.text)
        with open("test.txt", "w", encoding="utf-8") as fp:
            fp.write(r.text)
        archive, title = get_archive(soup, layer, parent_no)
    else:
        print("HTTPS請求錯誤... %s" %url)

    return archive, title

if __name__ == "__main__":
    for forum_bsn in forums:
        url = URL.format(forum_bsn)
        print(url)
        archive, forum_name = web_scraping_bot(url)
        csv_file = CSV_FILE.format(forum_name)
        save_to_csv(archive, csv_file)
        txt_file = TXT_FILE.format(forum_name)
        save_to_txt(archive, txt_file)
