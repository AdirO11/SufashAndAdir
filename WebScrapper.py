# -*- coding: utf-8 -*-


import urllib3
import getpass
import time 
from time import sleep
import datetime
from bs4 import BeautifulSoup 
from selenium import webdriver
from enum import Enum, unique

chrom_driver = r"C:/Users/{user}/Downloads/chromedriver_win32/chromedriver.exe".format(user = getpass.getuser())
MAX_DAYS_AHEAD = 3

@unique
class e_game_id(Enum):
    """
    enum of game id sites
    """ 
    bwin    =  "bwin"
    winner  =  "winner"
    bet365  =  "bet365"
    circus  =  "circus"


class Game(object):
    def __init__(self, one, x, two, time, game_date_str, game_id):
        
        # one, x, two are dicts of the form {b'name' : odds}
        self.one = one
        self.x = x
        self.two = two
        self.game_time = time
        self.game_date =  game_date_str
        self.game_id = game_id
        
    def __str__(self):
        ss = '\n \
        {game_id} {date} {time} - {one_name}: {one_odd}, {x_name}: {x_odd}, {two_name}: {two_odd} '.\
                            format(game_id = self.game_id,
                                   date = self.game_date, 
                                   time = self.game_time,
                                   one_name = next(iter(self.one.keys())),
                                   one_odd = next(iter(self.one.values())),
                                   x_name = next(iter(self.x.keys())),
                                   x_odd = next(iter(self.x.values())),
                                   two_name = next(iter(self.two.keys())),
                                   two_odd = next(iter(self.two.values()))
                                   )
        return ss
        
class WebScrapper(object):
    '''
    classdocs:
        tools to scrap from.  
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.web_dict = dict()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.bwin_games = set({})
        
    @staticmethod
    def get_bwin_url_by_dates(bwin_str_date):
        bwin_url = 'https://sports.bwin.com/en/sports#dateFilter={}&sportId=4'.format(bwin_str_date)
        return bwin_url
    
    def ScrapBet365(self):
        bet_365 = 'https://www.bet365.com/#/AC/B1/C1/D13/E40/F140/S1/'
        
        
        
        
        
    def ScrapBwin(self):
        now = datetime.datetime.now()
        driver = webdriver.Chrome(chrom_driver)
        games = []
        
        for day_offset in range(0, MAX_DAYS_AHEAD + 1):
            date = now + datetime.timedelta(day_offset)
            bwin_date = '{Y}-{M}-{D}'.format(Y = str(date.year),\
                                                 M = str(date.month).zfill(2),\
                                                 D = str(date.day).zfill(2))
            url = self.get_bwin_url_by_dates(bwin_str_date = bwin_date)            
            driver.get(url)
            sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            games = soup.findAll("div", {"class": "marketboard-event-group__item--event"})
            
            for game in games:
                t = game.find("div", {'class': 'marketboard-event-without-header__market-time'})
                if 'AM' in t.text:
                    time = t.text.split()[0]
                else:
                    time = t.text.split()[0]
                    time = '{H}:{M}'.format(H = (int(time.split(':')[0]) + 12),\
                                            M = time.split(':')[-1])
                names = game.findAll('div', {'class':'mb-option-button__option-name mb-option-button__option-name--odds-4'})
                odds = game.findAll('div', {'class': 'mb-option-button__option-odds'})
                if len(names) != 3 or len(odds) != 3:
                    continue
                one = dict( { names[0].text.encode("utf-8").decode("utf-8")  : odds[0].text} )
                x =   dict( { names[1].text.encode("utf-8").decode("utf-8")  : odds[1].text} )
                two = dict( { names[2].text.encode("utf-8").decode("utf-8")  : odds[2].text} )                
                game_id = e_game_id.bwin.value

                self.bwin_games = self.bwin_games.union((Game(one, x, two, time, bwin_date ,game_id), ))
                
        for game in self.bwin_games:
            print(game)
        
if __name__ == '__main__':
    ws = WebScrapper()
    ws.ScrapBwin()
