import json
import re

from fake_useragent import UserAgent

from main.models.objects import MetricsModel
from main.models.states import MetricsNameModel
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from main.models import Task, TaskResult


def start_parse(task_id, items):
    task = Task.objects.get(id=task_id)
    task.status_id = 2
    task.save()

    rating_model = MetricsNameModel.objects.get(id=1)

    for link in items:

        # try:
            ua = UserAgent()
            user_agent = ua.random
            print(user_agent)

            chrome_options = Options()
            chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})

            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument(f'user-agent={user_agent}')
            chrome_options.add_argument("--start-maximized")
            # driver = webdriver.Chrome(options=chrome_options)
            driver = webdriver.Chrome(executable_path='C://Users//1//PycharmProjects//Okko//src//main//modules//chromedriver.exe')

            driver.get(link)
            driver.implicitly_wait(10)
            rating = driver.find_element(by=By.XPATH, value=("//*[contains(text(),'Рейтинг')]")).text

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

    result = MetricsModel.objects.filter(task_id=task_id)
    print(result)
    if result.exists():
        result_list = []
        for res in result:
            d = {}
            d['task_id'] = task_id
            d['link'] = res.link
            d['metrics_id'] = res.metrics_name.pk
            d['value'] = res.value

            print(d)
            result_list.append(d)

        with open(f"files/task__{task_id}.json", "w", encoding='utf-8') as write_file:
            json.dump(result_list, write_file)

        TaskResult.objects.create(task_id=task_id, link=f"task__{task_id}.json", comment=None)

    else:
        TaskResult.objects.create(task_id=task_id, link=None, comment='Не удалось собрать метрики')

    task.status_id = 3
    task.save()

    print('end')