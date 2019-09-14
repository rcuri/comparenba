import requests, string
from app.models import Player
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def populate_database(db):
    chromeOptions = Options()
    chromeOptions.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chromeOptions)

    bball_ref_url = "https://www.basketball-reference.com"
    base_url = "https://www.basketball-reference.com/players/"


    for letter in string.ascii_lowercase:
        url = base_url + letter + "/"
        players = driver.get(url)
        players_soup = BeautifulSoup(driver.page_source, 'html.parser')
        names = players_soup.findAll('th', attrs={'data-stat':'player', 'scope':'row'})
        for name in names:
            player_url = bball_ref_url + name.find('a')['href']
            player_page = driver.get(player_url)
            player_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            player_name = player_page_soup.find('h1', attrs={'itemprop':'name'}).text
            try:
                debut = float(player_page_soup.find(string="NBA Debut: ").find_parent('p').text[-5:][:4])
            except:
                debut = None

            try:
                career_stats = player_page_soup.findAll('table', attrs={'id':'per_game'})[0].find('tfoot')
            except:
                career_stats = None

            try:
                fg_made = float(career_stats.find(attrs={'data-stat':'fg_per_g'}).text)
            except:
                fg_made = None

            try:
                fg_attempt = float(career_stats.find(attrs={'data-stat':'fga_per_g'}).text)
            except:
                fg_attempt = None

            try:
                fg_pct = float(career_stats.find(attrs={'data-stat':'fg_pct'}).text)
            except:
                fg_pct = None

            try:
                three_made = float(career_stats.find(attrs={'data-stat':'fg3_per_g'}).text)
            except:
                three_made = None

            try:
                three_attempt = float(career_stats.find(attrs={'data-stat':'fg3a_per_g'}).text)
            except:
                three_attempt = None

            try:
                three_pct = float(career_stats.find(attrs={'data-stat':'fg3_pct'}).text)
            except:
                three_pct = None

            try:
                ft_made = float(career_stats.find(attrs={'data-stat':'ft_per_g'}).text)
            except:
                ft_made = None

            try:
                ft_attempt = float(career_stats.find(attrs={'data-stat':'fta_per_g'}).text)
            except:
                ft_attempt = None

            try:
                ft_pct = float(career_stats.find(attrs={'data-stat':'ft_pct'}).text)
            except:
                ft_pct = None

            try:
                tot_pts = float(career_stats.find(attrs={'data-stat':'pts_per_g'}).text)
            except:
                tot_pts = None

            try:
                o_reb = float(career_stats.find(attrs={'data-stat':'orb_per_g'}).text)
            except:
                o_reb = None

            try:
                d_reb = float(career_stats.find(attrs={'data-stat':'drb_per_g'}).text)
            except:
                d_reb = None

            try:
                tot_reb = float(career_stats.find(attrs={'data-stat':'trb_per_g'}).text)
            except:
                tot_reb = None

            try:
                ass = float(career_stats.find(attrs={'data-stat':'ast_per_g'}).text)
            except:
                ass = None

            try:
                stls = float(career_stats.find(attrs={'data-stat':'stl_per_g'}).text)
            except:
                stls = None

            try:
                blks = float(career_stats.find(attrs={'data-stat':'blk_per_g'}).text)
            except:
                blks = None

            try:
                tov = float(career_stats.find(attrs={'data-stat':'tov_per_g'}).text)
            except:
                tov = None

            try:
                ts_pct = float(player_page_soup.findAll('table', attrs={'id':'advanced'})[0].find('tfoot').find(attrs={'data-stat':'ts_pct'}).text)
            except:
                ts_pct = None

            pos_set = set()
            for pos in player_page_soup.findAll('table', attrs={'id':'per_game'})[0].find('tbody').findAll(attrs={'data-stat':'pos'}):
                if(pos is not None):
                    pos_set.add(pos.text)



            positions = ''
            for item in pos_set:
                if len(positions) == 0:
                    positions += item
                else:
                    positions += ', ' + item



            player = Player(player_name=player_name, position=positions, first_nba_season=debut, field_goal_made=fg_made, field_goal_attempted=fg_attempt, field_goal_pct=fg_pct, three_pt_made=three_made, three_pt_attempted=three_attempt, three_pt_pct=three_pct, free_throw_made=ft_made, free_throw_attempted=ft_attempt, free_throw_pct=ft_pct, true_stg_pct=ts_pct, points=tot_pts, off_reb=o_reb, def_reb=d_reb, tot_reb=tot_reb, assists=ass, steals=stls, blocks=blks, turnovers=tov)
            print(player.player_name)
            db.session.add(player)
            print(player.player_name)
            db.session.commit()

        break
