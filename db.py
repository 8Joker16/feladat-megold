from datetime import date as d_
from flask.wrappers import Response
from pymongo import MongoClient
from bson import json_util
import _queues
DB_NAME = 'webstore'
HOST = 'localhost'
PORT = 27017
COLLECTION = 'data'
A_SRC = 'authSource=admin'


def create_db_connection():
    C_STRING = f'mongodb://{HOST}:{PORT}/{DB_NAME}?{A_SRC}'
    client = MongoClient(C_STRING)
    return client


client = create_db_connection()


def add_sale_of_day(args) -> str:
    date = args['date'] if args.get(
        'date') else d_.today().strftime("%Y-%m-%d")
    q = {"_id": date}
    r = client[DB_NAME][COLLECTION].find_one(q)
    if r is None:
        client[DB_NAME][COLLECTION].insert_one({
            '_id': date,
            'sales': [{
                'product_name': args['product_name'],
                'price': args['price'],
                'qty': args['qty']
            }],
            'visitors': 0})
    else:
        sales = r.get('sales')
        if sales:
            sales.append({
                'product_name': args['product_name'],
                'price': args['price'],
                'qty': args['qty']
            })
        else:
            sales = list()
            sales.append({
                'product_name': args['product_name'],
                'price': args['price'],
                'qty': args['qty']
            })
        visitors = r.get('visitors')
        if visitors:
            v_ = args['inc_visitors'] if args.get('inc_visitors') else 0
            visitors += v_
        u = {'sales': sales, 'visitors': visitors}
        client[DB_NAME][COLLECTION].update_one(
            {'_id': date}, {'$set': u})
    return '1'


def get_all_visitors_data() -> dict:
    r = get_all_data()
    data = dict()
    for i in r:
        data[i['_id']] = i['visitors']
    return data


def get_all_sales_dy_day() -> dict:
    r = get_all_data()
    data = dict()
    for i in r:
        data[i['_id']] = i['sales']
    return data


def get_all_data():
    return client[DB_NAME][COLLECTION].find()


def insert_data(days):
    client[DB_NAME][COLLECTION].insert_many(days['data'])
    _queues.run_statistics_job()
    return 'data saved'


def init_database():
    client = create_db_connection()
    client.drop_database(DB_NAME)
