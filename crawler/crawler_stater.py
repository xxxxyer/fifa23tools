# encoding: utf-8
"""
@author: zhaozilong
@contact: whuzhaozilong@whu.edu.cn
@time: 2023/1/5 20:06
"""
from time import sleep

import bs4.element
import cloudscraper
from bs4 import BeautifulSoup
from retrying import retry
import utils.MysqlTool

if __name__ == '__main__':
    mysqlTool = utils.MysqlTool.MysqlTool()
    scraper = cloudscraper.create_scraper()

    def error_fun(attempts, delay):
        print("{} try error, delay {}".format(attempts, delay))
        if attempts > 10:
            return False
        while delay < 1:
            return True


    @retry(stop_max_attempt_number=3, wait_fixed=5000, stop_func=error_fun)
    def get_data_of_page(page):
        url = "https://www.futbin.com/players?page={}".format(page)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        resp = scraper.get(url, headers=headers).text
        soup = BeautifulSoup(resp, 'lxml')
        tag = soup.find('table', id='repTb')

        data = []
        for child in tag.tbody.children:
            if type(child) is bs4.element.Tag and child.get('class') is not None and\
                    ('player_tr_1' in child.get('class') or 'player_tr_2' in child.get('class')):

                id = int(child.contents[1].div.get('data-igs').replace('player-', ''))
                name = child.contents[3].contents[3].contents[1].contents[1].text
                club = child.contents[3].contents[3].contents[3].contents[1].contents[1].get('data-original-title')
                nation = child.contents[3].contents[3].contents[3].contents[1].contents[3].get('data-original-title')
                league = child.contents[3].contents[3].contents[3].contents[1].contents[5].get('data-original-title')
                first_positon = child.contents[7].contents[1].text

                data.append((id, name, club, nation, league, first_positon))
                print(id, name, club, nation, league, first_positon)

        mysqlTool.insert_datas(data)
        return


    for i in range(1, 611):
        print("page {}".format(i))
        get_data_of_page(i)
        sleep(1)
