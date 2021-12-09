import threading
import queue
import db
import numpy as np

q = queue.Queue()


def run_statistics_job():
    q.put((get_most_sold_product_of_day, []))


def execute_background_process():
    while True:
        f, args = q.get()
        f(*args)


def get_most_sold_product_of_day():
    collection = db.client[db.DB_NAME][db.COLLECTION]
    days = collection.find()
    for day in days:
        arr = np.array(list(map(lambda s: s['qty'], day["sales"])))
        max_sold = arr.max().item()
        filtered = list(filter(lambda s: s['qty'] == max_sold, day["sales"]))
        collection.update_one(
            {"_id": day["_id"]},
            {
                "$set": {
                    "most_sold_products": filtered
                }
            }
        )


threading.Thread(target=execute_background_process, daemon=True).start()
