import os
import requests
from dotenv import load_dotenv


def get_vacancies_from_sj(language):
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
    vacancies_list = []
    page = 0
    pages_number = 1
    while page < pages_number:
        response = requests.get(url, params=url_params, headers=auth_token)
        response.raise_for_status()
        vacancies_list.append(response.json())
        total = response.json()['total']
        if total <= url_params['count']:
            page += 1
        else:
            total -= url_params['count']
            pages_number += 1
            page += 1
    return vacancies_list


def extract_vacancies_from_sj(vacancies_list):
    vacancies = {'objects': []}
    for scope_vacancies in vacancies_list:
        vacancies['objects'].extend(scope_vacancies['objects'])
        vacancies['total'] = scope_vacancies['total']
    for vacancy in vacancies['objects']:
        vacancy['from'] = vacancy['payment_from']
        vacancy['to'] = vacancy['payment_to']
    return vacancies
