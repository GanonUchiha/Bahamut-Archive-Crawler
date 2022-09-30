import time
import requests
import csv
import re
from bs4 import BeautifulSoup, Tag
from typing import List, Tuple

from template import TEMPL_FORUM_URL, TEMPL_OUTPUT_CSV, TEMPL_OUTPUT_TXT

def get_resource(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
               "AppleWebKit/537.36 (KHTML, like Gecko)"
               "Chrome/84.0.4147.105 Safari/537.36"}
    return requests.get(url, headers=headers) 

def parse_html(html_str) -> BeautifulSoup:
    '''
    Parse the webpage into a BeautifulSoup object

    Returns:
        A BeautifulSoup object

    Paramters:
        html_str: a string in html
    '''
    return BeautifulSoup(html_str, "lxml")

def is_dir(img_tag: Tag):
    '''
    Checks whether an archive entry is a directory

    Returns:
        A boolean value

    Paramters:
        img_tag: the archive entry, as a Tag object
    '''
    return img_tag["class"][0] == "IMG-E14"

def title_rename(title):
    title_normalized: str = re.sub(r"[^\w\d☆！：（） ]+", "", title)
    title_cleaned: str = re.sub(" +", " ", title_normalized.strip())
    return title_cleaned

def get_archive(soup: BeautifulSoup, dir_depth=0, parent_id="") -> Tuple[List, str]:
    '''
    Extract archive content and title from the archive webpage

    Returns:
        A tuple of two objects:
            1. The archive content, as a List object
            2. The title of the archive, as a string value

    Parameters:
        soup: the webpage, as a BeautifulSoup object
        dir_depth: depth of the Archive directory (root=0)
        parent_id: The ID of the parent directory
    '''

    archive = []
    sleep_time = 1
    count = 0

    table = soup.find(class_="FM-stb1")
    title = ""
    if dir_depth == 0:
        title = soup.find("title").text.replace("精華區 - 巴哈姆特", "")
        title = title_rename(title)
        print("開始分析 「{}」 的精華區目錄".format(title))
        archive.append(["編號", "主題", "網址", "更新日期"])

    for row in table.find_all("tr")[1:]:
        count += 1
        # print(row, end="\n\n")
        cells: List[BeautifulSoup] = row.find_all("td")
        entry_id = str(cells[0].string)
        if dir_depth > 0:
            entry_id = "%s-%s" %(parent_id, entry_id)
        
        content = cells[1]
        entry_type = "Dir" if is_dir(content.find("img")) else "File"
        content_str = "%s%s" %("    " * dir_depth, content.find("a").string)
        link = "https://forum.gamer.com.tw/" + content.find("a")["href"]
        date = cells[4].string
        entry = (entry_id, content_str, link, date)
        archive.append(entry)

        # Iterate into subdirectories, if possible
        if entry_type == "Dir": 
            # print("Sleeping for %d second(s)..." %sleep_time)
            time.sleep(sleep_time)
            child_archive, _ = web_scraping_bot(link, dir_depth+1, entry_id)
            archive += child_archive
        
    return archive, title

def save_to_csv(archive: List, csv_file: str):
    '''
    Saving result as csv file

    Returns:
        None

    Parameters:
        archive: The archive content, as a List object
        csv_file: The location to save the csv file
    '''
    with open(csv_file, "w+", newline="", encoding="utf8") as fp:
        print("儲存至 \"{}\"".format(csv_file))
        writer = csv.writer(fp)
        for entry in archive:
            writer.writerow(entry)

def save_to_txt(archive, txt_file):
    '''
    Saving result as txt file

    Returns:
        None

    Parameters:
        archive: The archive content, as a List object
        txt_file: The location to save the txt file
    '''
    with open(txt_file, "w", newline="", encoding="utf-8") as fp:
        print("儲存至 \"{}\"".format(txt_file))
        fp.write("編號{} | 主題\n".format(" " * 16))
        for entry in archive[1:]:
            fp.write("{0:<20} | {1}\n".format(entry[0], entry[1]))

def web_scraping_bot(page_url, dir_depth=0, parent_id="") -> Tuple[List, str]:
    '''
    Main scraping function, retriving archive content recursively.

    Parameters:
        page_url: URL to the archive page
        dir_depth: The depth of the archive directory (root=0)
        parent_id: The number of the parent directory
    '''
    
    # Show current progress
    if dir_depth == 0:
        print("[INFO] 抓取精華區根目錄資料中...")
    else:
        print("[INFO] 抓取第{}-{}層子目錄資料中...".format(parent_id, dir_depth))
    
    # Get webpage as a BeautifulSoup object
    r = get_resource(page_url)

    if r.status_code == requests.codes.OK:
        soup = parse_html(r.text)

        # Save webpage for debugging
        # with open("test.txt", "w", encoding="utf-8") as fp:
        #     fp.write(r.text)

        # Extract archive content and title from the webpage
        archive, title = get_archive(soup, dir_depth, parent_id)
        return archive, title
    else:
        print("[Error] HTTPS請求錯誤... %s" %page_url)

def main():
    # Target forum IDs
    list_forums = [29220, 60076, 30861, 31406]

    # Itereate through the target forums
    for forum_number in list_forums:
        url = TEMPL_FORUM_URL.format(forum_number)
        print(url)
        archive, forum_name = web_scraping_bot(url)

        csv_file = TEMPL_OUTPUT_CSV.format(forum_name)
        save_to_csv(archive, csv_file)
        
        txt_file = TEMPL_OUTPUT_TXT.format(forum_name)
        save_to_txt(archive, txt_file)

if __name__ == "__main__":
    main()
