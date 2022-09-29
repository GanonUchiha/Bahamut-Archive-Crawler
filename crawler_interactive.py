from crawler import web_scraping_bot, save_to_csv, save_to_txt

# 存檔檔名模板
CSV_FILE = "{}.csv"
TXT_FILE = "{}.txt"

def invalidURL(url):
    URL = "https://forum.gamer.com.tw/G1.php?bsn="
    return url.startswith(URL)

if __name__ == "__main__":
    url = input("輸入精華區根目錄完整網址：")
    print(url)
    while not invalidURL(url):
        url = input("網址格式錯誤，請重新輸入：")
    archive, forum_name = web_scraping_bot(url)
    csv_file = CSV_FILE.format(forum_name)
    save_to_csv(archive, csv_file)
    txt_file = TXT_FILE.format(forum_name)
    save_to_txt(archive, txt_file)
    input("Press Enter to continue...")
