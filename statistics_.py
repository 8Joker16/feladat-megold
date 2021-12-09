from flask.helpers import send_file
import db
import re
import pandas as pd
import uuid
import os


def get_visitors_statistics():
    filename = generate_filename()
    v = db.get_all_visitors_data()
    f = format_visitors_data_to_monthly(v)
    df = pd.DataFrame({'keys': ['Jan', 'Feb', 'Mar', 'Apr'],
                       'visitors': f.values()})
    ax = df.plot.bar(x='keys', y='visitors', rot=0, figsize=(15, 10))
    ax.set_xlabel('Months')
    ax.set_ylabel('Visitors')
    ax.set_title('Visitors per month')
    ax.figure.savefig(filename)

    # @after_this_request
    # def remove_file(request):
    #     os.remove(filename)
    #     return request
    return send_file(filename, 'image/png')


def format_visitors_data_to_monthly(d: dict) -> dict:
    data = dict()
    months = get_keys_monthly(d)
    for m in months:
        visitors = [d[key] for key in d.keys() if re.match(m, key)]
        data[m] = sum(visitors)
    return data


def get_keys_monthly(d: dict) -> list:
    months = list()
    for m in d:
        months.append(m[:-3])
    return list(dict.fromkeys(months))


def get_incomes_statistics(args: dict):
    filename = generate_filename()
    r = db.get_all_sales_dy_day()
    s = dict()
    for i in r:
        s[i] = dict()
        s[i]['sum'] = sum(item['price']*item['qty'] for item in r[i])
        s[i]['min'] = min(item['price']*item['qty'] for item in r[i])
        s[i]['max'] = max(item['price']*item['qty'] for item in r[i])
    # return s

    def v(data, key): return list(data[i][key] for i in data)
    df = pd.DataFrame({
        'sum': v(s, 'sum'),
        'min': v(s, 'min'),
        'max': v(s, 'max')
    }, index=s.keys())

    ax = df.plot.line(figsize=(15, 10))
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title('Incomes')
    ax.figure.savefig(filename)

    # @after_this_request
    # def remove_file(request):
    #     os.remove(filename)
    #     return request

    return send_file(filename)


def remove_file(filename):
    os.remove(filename)


def generate_filename() -> str:
    return uuid.uuid4().hex.upper()[0:6]+'.png'
