from crawler import web_scraping_bot, save_to_csv, save_to_txt
from template import TEMPL_OUTPUT_CSV, TEMPL_OUTPUT_TXT

def is_valid_url(url: str) -> bool:
    '''
    Tests whether the given url is a valid url to the archive root webpage

    Returns:
        A boolean value

    Parameter(s):
        url: The webpage url
    '''
    URL = "https://forum.gamer.com.tw/G1.php?bsn="
    return url.startswith(URL)

def main():
    url = input("輸入精華區根目錄完整網址：")
    print(url)

    # Proceeds only if provided with a valid archive url
    while not is_valid_url(url):
        url = input("網址 \"{}\" 格式錯誤，請重新輸入：".format(url))

    # Retrieve the archive content from the url
    archive, forum_name = web_scraping_bot(url)

    # Save result to file(s)
    csv_file = TEMPL_OUTPUT_CSV.format(forum_name)
    save_to_csv(archive, csv_file)
    txt_file = TEMPL_OUTPUT_TXT.format(forum_name)
    save_to_txt(archive, txt_file)

    input("Press Enter to continue...")

if __name__ == "__main__":

    main()
