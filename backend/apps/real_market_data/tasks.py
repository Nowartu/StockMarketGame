from celery import shared_task
from .models import Company, Stock
from datetime import datetime, timedelta
from django.conf import settings
import requests
import xlrd
import os

@shared_task()
def download_data():
    #days = get_days()
    #for day in days:
    #    get_file(day)

    files = [f'files/downloaded/{x}' for x in os.listdir('files/downloaded') if x.endswith(".xls")]
    for file in files:
        add_file_to_database(file)

def get_days():
    days = []
    now = datetime.now()
    last_in_database = Stock.objects.last()
    if last_in_database is None:
        last = datetime.now()
    else:
        last = datetime.combine(last_in_database.date, datetime.min.time())
    while last < now:
        if last.weekday() < 5:
            days.append(last.strftime('%Y-%m-%d'))
        last += timedelta(days=1)
    return days



def get_file(day):
    for name, url in settings.REAL_MARKET_DATA_URLS:
        response = requests.get(url + day, stream=True)
        if response.status_code == 200:
            with open(f'files/downloaded/{name}{day}.xls', 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)


def add_file_to_database(path):
    companies = {x.name: x for x in Company.objects.all()}
    book = xlrd.open_workbook(path)
    sh = book.sheet_by_index(0)
    added = []
    for rx in range(sh.nrows):
        if sh.cell_value(rx, 0) == 'Data':
            continue
        if f'{sh.cell_value(rx, 0)}_{sh.cell_value(rx, 1)}' in added:
            continue
        if sh.cell_value(rx, 1) not in companies.keys():
            company = Company(
                type="AkcjePL",
                name=sh.cell_value(rx, 1),
                full_name='N/D',
                isin=sh.cell_value(rx, 2),
                market='ETF' if 'etf' in path else 'AKCJE',
                submarket='N/D',
                sector='{N/D}',
                stock_no=0,
                market_value=0,
                value=0
            )
            company.save()
            companies = {x.name: x for x in Company.objects.all()}
        stock = Stock(
            company=companies[sh.cell_value(rx, 1)],
            date=sh.cell_value(rx, 0),
            open_price=sh.cell_value(rx, 4),
            close_price=sh.cell_value(rx, 7),
            max_price=sh.cell_value(rx, 5),
            min_price=sh.cell_value(rx, 6),
            volume=sh.cell_value(rx, 9),
            transactions_no=sh.cell_value(rx, 10),
            turnover=sh.cell_value(rx, 11) * 1000
        )
        stock.save()