import os
import requests
from dotenv import load_dotenv


def extract_vacancies_from_sj(language):
    load_dotenv()
    token = os.environ['TOKEN']
    url = 'https://api.superjob.ru/2.0/vacancies/'
    auth_token = {
        'X-Api-App-Id': '{}'.format(token)
    }
    url_params = {
        'town': 4,
        'catalogues': 48,
        'currency': 'rub',
        'page': 0,
        'count': 100
        }
    url_params['keyword'] = language
    vacancies = {'objects': []}
    page = 0
    pages_number = 1
    while page < pages_number:
        response = requests.get(url, params=url_params, headers=auth_token)
        if response.ok:
            vacancies['total'] = response.json()['total']
            for item in response.json()['objects']:
                    vacancies['objects'].append(item)
                    for vacancy in vacancies['objects']:
                        vacancy['from'] = vacancy['payment_from']
                        vacancy['to'] = vacancy['payment_to']    
            if vacancies['total'] <= url_params['count']:
                page += 1
            else:
                vacancies['total'] -= url_params['count']
                pages_number += 1
                page += 1
    return vacancies
