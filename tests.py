import unittest
import app
import db
import random
import datetime


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


def make_date_from_index(index: int) -> str:
    y = datetime.datetime.today().year
    date = datetime.date(y, 1, 1)
    delta = datetime.timedelta(index - 1)
    newdate = date + delta
    return newdate.strftime("%Y-%m-%d")
    # return random_date(startDate).strftime("%Y-%m-%d")


def load_sample_data() -> dict:
    days = dict({"data": list()})
    for i in range(120):
        days['data'].append({
            "_id": make_date_from_index(i+1),
            "visitors": random.randint(10, 3590),
            "sales": generate_sales_of_a_day()
        })
    return days


class DBTests(unittest.TestCase):
    '''
    Sets up the test
        self.app: creates a Flask instance with test_client
        self.db: creates a mongodb client
        self.sample_upload_data: generates sample Sys/Dia data structure
    '''

    def setUp(self):
        self.app = app.createTestClient()
        self.db = db.create_db_connection()

    def test_init_db(self):
        db.init_database()

    # test if the API is available

    def test_site_health_check(self):
        response = self.app.get('/ping')
        self.assertEqual(response.data, b'1')

    # seeds up the databas through /upload API endpoint

    def test_upload_correct(self):
        response = self.app.post(
            '/save-batch-data', json=load_sample_data(),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'data saved')

    # tests if db exists
    def test_x_database_exists(self):
        self.assertIn(db.DB_NAME, db.client.list_database_names())

    # this should fail, because it's sending data instead of json
    def test_upload_incorrect(self):
        response = self.app.post(
            '/save-batch-data', data=load_sample_data(),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def add_sales_test_data() -> dict:
        return {
            "product_name": "Teszt termék",
            "price": 110,
            "qty": 4,
            "date": "2021-01-01",
            "inc_visitors": 13000
        }


if __name__ == '__main__':
    unittest.main()
