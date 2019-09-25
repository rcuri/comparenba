from multiprocessing import Queue, cpu_count
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import requests, string
from bs4 import BeautifulSoup
import shutil
import timeit
import os
from app import db
from app.models import Player
from flask import current_app

def player_urls():
    chromeOptions = Options()
    chromeOptions.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chromeOptions)

    bball_ref_url = "https://www.basketball-reference.com"
    base_url = "https://www.basketball-reference.com/players/"

    letters = 'abcdefghijklmnopqrstuvwyz'
    urls_to_search = []
    for letter in letters:
        url = base_url + letter + "/"
        players = driver.get(url)
        players_soup = BeautifulSoup(driver.page_source, 'html.parser')
        names = players_soup.findAll('th', attrs={'data-stat':'player', 'scope':'row'})
        for name in names:
            player_url = bball_ref_url + name.find('a')['href']
            urls_to_search.append(player_url)

    return urls_to_search

def populate_images(db):
    start = timeit.default_timer()
    selenium_data = player_urls()
    selenium_data.append('STOP')

    selenium_data_queue = Queue()
    worker_queue = Queue()

    worker_ids = list(range(cpu_count()-1))
    chromeOptions = Options()
    chromeOptions.add_argument('--headless')
    selenium_workers = {i: webdriver.Chrome(chrome_options=chromeOptions) for i in worker_ids}
    for worker_id in worker_ids:
        worker_queue.put(worker_id)


    def selenium_task(worker, data, db, app):
        worker.get(data)
        player_page_soup = BeautifulSoup(worker.page_source, 'html.parser')
        player_name = player_page_soup.find('h1', attrs={'itemprop':'name'}).text
        img = player_page_soup.find('img', attrs={'itemscope':'image'})
        if img is not None:
            try:
                with app.app_context():
                    file_name = img['src'].split('/')[-1]
                    player = Player.query.filter(Player.player_name==player_name).first()
                    player.player_image = file_name
                    db.session.commit()
            except Exception as e:
                print(e)




    def selenium_queue_listener(data_queue, worker_queue, db, app):
        print(app)
        while True:
            current_data = data_queue.get()
            if current_data == 'STOP':
                print("STOP encountered, killing worker thread")
                data_queue.put(current_data)
                break
            else:
                print(f"Got the item {current_data} on the data queue")
            worker_id = worker_queue.get()
            worker = selenium_workers[worker_id]
            selenium_task(worker, current_data, db, app)
            worker_queue.put(worker_id)
        return


    selenium_processes = [Thread(target=selenium_queue_listener,
                                 args=(selenium_data_queue, worker_queue, db, current_app._get_current_object())) for _ in worker_ids]
    for p in selenium_processes:
        p.daemon = True
        p.start()

    for d in selenium_data:
        selenium_data_queue.put(d)

    print("Waiting for Queue listener threads to complete")
    for p in selenium_processes:
        p.join()

    print("Tearing down web workers")
    for b in selenium_workers.values():
        b.quit()

    end = timeit.default_timer()
    print(end-start)
    db.session.commit()
