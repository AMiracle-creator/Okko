import re
from datetime import datetime

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from main.models.objects import MetricsModel
from main.models.states import MetricsNameModel

from main.models import Task


def start_parse(task_id, items):
    task = Task.objects.get(id=task_id)
    task.status_id = 2
    task.save()

    rating_model = MetricsNameModel.objects.get(id=1)

    for link in items:

        # try:
            ua = UserAgent()
            print(ua.chrome)
            header = {'User-Agent': str(ua.chrome)}
            response = requests.get(link, headers=header).text

            soup = BeautifulSoup(response, 'lxml')

            # try:
            rating = soup.find('span', class_='_38dQl')
            print(rating)

            # # except Exception:
            #     rating = None
            #     print('no rating')

            if rating is not None:
                result = re.search('\d+', rating).group(0)
                print(result)
                metrics = MetricsModel(task=task, link=link, metrics_name=rating_model, value=result)
                metrics.save()

        # except Exception:
        #     print('wrong link')

    task.status_id = 3
    task.save()

    print('end')