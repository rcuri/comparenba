from multiprocessing import Queue, cpu_count
from threading import Thread
from time import sleep
from app import db
from flask import current_app
from app.util import player_urls, selenium_task, selenium_queue_listener
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def populate_database(db):
    """
    Use multithreading to search through multiple player websites concurrently
    and commit NBA players to Players table.

    Using ChromeDriver for Chrome version 78.
    """
    # Retrieve all players' URLs to parse and append 'STOP' to end of list
    # to ensure queue is threadsafe.
    selenium_data = player_urls()
    selenium_data.append('STOP')

    selenium_data_queue = Queue()
    worker_queue = Queue()

    # Create multiple instances of webdrivers and assign to them a worker_id
    num_threads = cpu_count()-1
    worker_ids = list(range(num_threads))
    chromeOptions = Options()
    chromeOptions.add_argument('--headless')
    selenium_workers = {
        i: webdriver.Chrome(options=chromeOptions) for i in worker_ids
    }
    for worker_id in worker_ids:
        worker_queue.put(worker_id)

    # Instantiate threads with selenium_queue_listener target function and
    # start the threads
    selenium_threads = [Thread(
            target=selenium_queue_listener, args=(selenium_workers,
            selenium_data_queue,worker_queue, db,
            current_app._get_current_object())) for _ in worker_ids]
    for p in selenium_threads:
        p.daemon = True
        p.start()

    # Place all the URLs of pages to parse in shared data queue so all
    # threads have access
    for d in selenium_data:
        selenium_data_queue.put(d)

    # Wait for queue listener threads to complete
    for p in selenium_threads:
        p.join()

    # Tear down web workers
    for b in selenium_workers.values():
        b.quit()

    db.session.commit()
