'''
Bolti eladások
Legforgalmasabb nap.
Legtöbb/kevesebb bevétel napra bontva, átlagtól nagyon eltérő napok.
Legtöbbet/kevesebbet vásárolt termék.

Actual traffic data of day
traffic:
[
    { // Az adott nap a héten.
    visitors: 32,
    sales: [
        {
        product_name: "product_1",
        net_price: 1000,
        sold_qty: 2,
        timestamp: "10:30"
        },
        {
        product_name: "product_1",
        net_price: 1000,
        sold_qty: 5,
        timestamp: "11:30"
        },
        {
        product_name: "product_2",
        net_price: 1000,
        sold_qty: 1,
        timestamp: "13:30"
        },
    ]
    },
]
'''

import db
from flask import request, Blueprint, Flask
from flask_expects_json import expects_json
import statistics_ as st
import sample

app = Flask(__name__)

db_api = Blueprint('db', __name__)

schema = {
    'type': 'object',
    'properties': {
        'timestamp': {'type': 'string', 'format': 'date'},
        'product_name': {'type': 'string'},
        'price': {'type': 'number'},
        'qty': {'type': 'number'},
        'inc_visitors': {'type': 'number'}
    },
    'required': ['product_name', 'price', 'qty']
}


@db_api.route('/ping')
def health_check():
    return '1'


@db_api.route('/get-sample-data', methods=['GET'])
def get_sample_data():
    return sample.load_sample_data()


@db_api.route('/save-batch-data', methods=['POST'])
def save_batch_data():
    return db.insert_data(request.get_json())


@db_api.route('/add-sale', methods=['POST'])
@expects_json(schema)
def post_add_sale():
    return db.add_sale_of_day(request.get_json())


@db_api.route('/statistics/visitors')
def get_statistics_visitors():
    return st.get_visitors_statistics()


@db_api.route('/statistics/incomes')
def get_statistics_income():
    r = st.get_incomes_statistics(request.args)
    return r


def createTestClient():
    return app.test_client()


app.register_blueprint(db_api)
