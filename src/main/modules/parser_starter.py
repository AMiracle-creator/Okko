from datetime import datetime

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from main.models.objects import ContentModel, MetricsModel


def parser():
    contents = ContentModel.objects.all()

    for content in contents:

        try:
            ua = UserAgent()
            print(ua.chrome)
            header = {'User-Agent': str(ua.chrome)}
            response = requests.get(content.url, headers=header).text

            soup = BeautifulSoup(response, 'lxml')

            try:
                rating = soup.find('span', class_='DWNLG').text
                print(rating)

            except Exception:
                rating = None
                print('no rating')

            if rating is not None:
                metrics = MetricsModel(material=content.id_content, id_metrics_name=1, value=rating)
                metrics.save()

        except Exception:
            print('wrong link')

    print('end')