import re

from fake_useragent import UserAgent

from main.models.objects import MetricsModel
from main.models.states import MetricsNameModel
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from main.models import Task


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
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

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

    task.status_id = 3
    task.save()

    print('end')