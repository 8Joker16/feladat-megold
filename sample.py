import random
from random import randrange
import datetime
import db


def random_date(start) -> datetime:
    return start - datetime.timedelta(minutes=randrange(60*8))


def make_date_from_index(index: int) -> str:
    y = datetime.datetime.today().year
    date = datetime.date(y, 1, 1)
    delta = datetime.timedelta(index - 1)
    newdate = date + delta
    return newdate.strftime("%Y-%m-%d")
    # return random_date(startDate).strftime("%Y-%m-%d")


def generate_sale() -> dict:
    sale = dict()

    products = [
        {'name': 'Test product', 'price': 1500},
        {'name': 'Ketchup', 'price': 1499},
        {'name': 'Milk', 'price': 269},
        {'name': 'Ice cream', 'price': 399},
        {'name': 'Pizza', 'price': 1899}
    ]

    p = random.choice(products)
    sale['product_name'] = p['name']
    sale['price'] = p['price']
    sale['qty'] = random.randint(1, 140)
    # sale['timestamp'] = timestamp.strftime("%Y-%m-%d %H:%M")

    return sale


def generate_sales_of_a_day() -> list:
    day_sales = list()
    for i in range(random.randint(1, 5)):
        day_sales.append(generate_sale())
    return day_sales


def load_sample_data() -> dict:
    db.init_database()
    days = dict({"data": list()})
    for i in range(365):
        days['data'].append({
            "_id": make_date_from_index(i+1),
            "visitors": random.randint(10, 3590),
            "sales": generate_sales_of_a_day()
        })

    db.client[db.DB_NAME][db.COLLECTION].insert_many(days['data'])
    return days
