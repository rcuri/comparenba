from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from string import ascii_lowercase
from bs4 import BeautifulSoup
from app import db
from app.models import Player

def player_urls():
    """
    Retrieve all the NBA players' page URLs and return list.

    Using Selenium webdriver to make requests to website and scrape pages
    using javascript to load content.

    Using ChromeDriver for Chrome version 78.
    """
    chromeOptions = Options()
    chromeOptions.add_argument('--headless')
    driver = webdriver.Chrome(options=chromeOptions)

    bball_ref_url = "https://www.basketball-reference.com"
    base_url = "https://www.basketball-reference.com/players/"

    letters = ascii_lowercase
    urls_to_search = []
    for letter in letters:
        url = base_url + letter + "/"
        players = driver.get(url)
        players_soup = BeautifulSoup(driver.page_source, 'html.parser')
        names = players_soup.findAll(
            'th', attrs={'data-stat':'player', 'scope':'row'})
        for name in names:
            player_url = bball_ref_url + name.find('a')['href']
            urls_to_search.append(player_url)

    return urls_to_search


def selenium_task(worker, data):
    """
    Using selenium webdriver (worker), make a request to URL (data) and
    parse player information. Return Player object created from this
    information.
    """
    try:
        worker.get(data)

        player_page_soup = BeautifulSoup(
            worker.page_source, 'html.parser')
        player_name = player_page_soup.find(
            'h1', attrs={'itemprop':'name'}).text
        try:
            debut = float(
                player_page_soup.find(
                string="NBA Debut: ").find_parent('p').text[-5:][:4])
        except:
            debut = None

        try:
            career_stats = player_page_soup.findAll(
                'table', attrs={'id':'per_game'})[0].find('tfoot')
        except:
            career_stats = None

        try:
            fg_made = float(
                career_stats.find(attrs={'data-stat':'fg_per_g'}).text)
        except:
            fg_made = None

        try:
            fg_attempt = float(
                career_stats.find(attrs={'data-stat':'fga_per_g'}).text)
        except:
            fg_attempt = None

        try:
            fg_pct = float(
                career_stats.find(attrs={'data-stat':'fg_pct'}).text)
        except:
            fg_pct = None

        try:
            three_made = float(
                career_stats.find(attrs={'data-stat':'fg3_per_g'}).text)
        except:
            three_made = None

        try:
            three_attempt = float(
                career_stats.find(attrs={'data-stat':'fg3a_per_g'}).text)
        except:
            three_attempt = None

        try:
            three_pct = float(
                career_stats.find(attrs={'data-stat':'fg3_pct'}).text)
        except:
            three_pct = None

        try:
            ft_made = float(
                career_stats.find(attrs={'data-stat':'ft_per_g'}).text)
        except:
            ft_made = None

        try:
            ft_attempt = float(
                career_stats.find(attrs={'data-stat':'fta_per_g'}).text)
        except:
            ft_attempt = None

        try:
            ft_pct = float(
                career_stats.find(attrs={'data-stat':'ft_pct'}).text)
        except:
            ft_pct = None

        try:
            tot_pts = float(
                career_stats.find(attrs={'data-stat':'pts_per_g'}).text)
        except:
            tot_pts = None

        try:
            o_reb = float(
                career_stats.find(attrs={'data-stat':'orb_per_g'}).text)
        except:
            o_reb = None

        try:
            d_reb = float(
                career_stats.find(attrs={'data-stat':'drb_per_g'}).text)
        except:
            d_reb = None

        try:
            tot_reb = float(
                career_stats.find(attrs={'data-stat':'trb_per_g'}).text)
        except:
            tot_reb = None

        try:
            ass = float(
                career_stats.find(attrs={'data-stat':'ast_per_g'}).text)
        except:
            ass = None

        try:
            stls = float(
                career_stats.find(attrs={'data-stat':'stl_per_g'}).text)
        except:
            stls = None

        try:
            blks = float(
                career_stats.find(attrs={'data-stat':'blk_per_g'}).text)
        except:
            blks = None

        try:
            tov = float(
                career_stats.find(attrs={'data-stat':'tov_per_g'}).text)
        except:
            tov = None

        try:
            ts_pct = float(
                player_page_soup.findAll(
                'table', attrs={'id':'advanced'})[0].find('tfoot').find(
                attrs={'data-stat':'ts_pct'}).text)
        except:
            ts_pct = None

        try:
            img = player_page_soup.find(
                'img', attrs={'itemscope':'image'})
            file_name = img['src'].split('/')[-1]
        except:
            file_name = None

        pos_set = set()
        position_list = player_page_soup.findAll(
            'table', attrs={'id':'per_game'})[0].find(
            'tbody').findAll(attrs={'data-stat':'pos'})
        for pos in position_list:
            if pos is not None:
                pos_set.add(pos.text)

        positions = ', '.join(pos_set)

        player = Player(
            player_name=player_name, player_image=file_name,
            position=positions, first_nba_season=debut,
            field_goal_made=fg_made, field_goal_attempted=fg_attempt,
            field_goal_pct=fg_pct, three_pt_made=three_made,
            three_pt_attempted=three_attempt, three_pt_pct=three_pct,
            free_throw_made=ft_made, free_throw_attempted=ft_attempt,
            free_throw_pct=ft_pct, true_stg_pct=ts_pct, points=tot_pts,
            off_reb=o_reb, def_reb=d_reb, tot_reb=tot_reb, assists=ass,
            steals=stls, blocks=blks, turnovers=tov)
        return player
    except Exception as e:
        # If page failed to load, return URL in order to add back to URL queue
        # and reattempt to load page
        return e, data


def selenium_queue_listener(
        selenium_workers, data_queue, worker_queue, db, app):
    """
    Run selenium threads until you have added all NBA players to database.
    """
    with app.app_context():
        while True:
            # Get URL in front of the queue
            current_data = data_queue.get()
            if current_data == 'STOP':
                # if STOP encountered, kill worker thread
                data_queue.put(current_data)
                break
            # Line below for testing purposes
            #    else: print(f"Got the item {current_data} on the data queue")

            # Get a webdriver instance from queue using associated worker_id.
            # Use worker to visit URL and create Player object using
            # selenium_task. Return worker to queue when finished.
            worker_id = worker_queue.get()
            worker = selenium_workers[worker_id]
            player = selenium_task(worker, current_data)
            worker_queue.put(worker_id)

            # If Player returned from selenium_task, add player to session.
            # Otherwise, add URL back to queue since the page failed to load.
            if type(player) is Player:
                db.session.add(player)
            else:
                data_queue.put(current_data)
        db.session.commit()
    return
