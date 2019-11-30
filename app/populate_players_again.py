from multiprocessing import Queue, cpu_count
from threading import Thread
from time import sleep
from app import db
from flask import current_app
from app.util import player_urls, selenium_task, selenium_queue_listener
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def populate_database(db):
    print("HERE")
    selenium_data = player_urls()
    selenium_data.append('STOP')

    selenium_data_queue = Queue()
    worker_queue = Queue()

    worker_ids = list(range(cpu_count()-1))
    chromeOptions = Options()
    chromeOptions.add_argument('--headless')
    selenium_workers = {
        i: webdriver.Chrome(options=chromeOptions) for i in worker_ids
    }
    for worker_id in worker_ids:
        worker_queue.put(worker_id)

    selenium_processes = [Thread(
            target=selenium_queue_listener, args=(selenium_workers, selenium_data_queue,
            worker_queue, db, current_app._get_current_object()))
            for _ in worker_ids]
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

    db.session.commit()
