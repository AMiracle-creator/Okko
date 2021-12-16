from datetime import datetime

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from fake_useragent import UserAgent
from peewee import MySQLDatabase, Model, PrimaryKeyField, IntegerField, CharField
from bs4 import BeautifulSoup

pg_db = MySQLDatabase(database="apiparser", user='iriparser', password='asdflk#$KGf8FD&fasdjkksdf', host='89.223.67.114',
                      port=3306, charset='utf8mb4')


class BaseModel(Model):
    class Meta:
        database = pg_db


class Metrics(BaseModel):
    id = PrimaryKeyField(null=False)
    material_id = IntegerField()
    id_metrics_name = IntegerField()
    value = CharField(max_length=255)
    time = IntegerField(default=0)


class Content(BaseModel):
    id_content = PrimaryKeyField(null=False)
    resource = CharField(max_length=255)
    created_at = IntegerField()
    project_name = CharField(max_length=255)
    id_format_content = IntegerField()
    name_content = CharField(max_length=255)
    url = CharField(max_length=255, unique=True)
    success = IntegerField(default=0)
    success_date_update = IntegerField()
    acc_type = IntegerField()


def parser():
    print('start')
    cur = pg_db.cursor()
    cur.execute('SELECT * from content where resource = "OKKOTV"')
    rows = cur.fetchall()
    cur.close()

    for row in rows:
        link = row[6]
        print(link)

        try:
            ua = UserAgent()
            print(ua.chrome)
            header = {'User-Agent': str(ua.chrome)}
            response = requests.get(link, headers=header).text

            soup = BeautifulSoup(response, 'lxml')

            try:
                rating = soup.find('span', class_='DWNLG').text
                print(rating)

            except Exception:
                rating = None
                print('no rating')

            if rating is not None:
                Metrics.create(material_id=row[0], id_metric_name=36, value=rating)

        except Exception:
            print('wrong link')

    print('end')


scheduler = BlockingScheduler(daemon=True)
date_now = datetime.now().strftime('%H:%M:%S:%f')
print(date_now)
# from now - 3
date_time_str = '00:06:00'

date_time = datetime.strptime(date_time_str, '%H:%M:%S')
print(date_time.strftime('%H:%M:%S:%f'))
scheduler.add_job(parser, trigger=CronTrigger(hour=date_time.hour, minute=date_time.minute),
replace_existing=True)

try:
    scheduler.start()
except KeyboardInterrupt as e:
    print(e)
    scheduler.shutdown()