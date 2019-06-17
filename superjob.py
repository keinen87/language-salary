import os
import requests
from settings import PROGRAMMING_LANGUAGES, TEMPLATE
from dotenv import load_dotenv


def predict_rub_salary_sj(payment_from, payment_to):
    if payment_from and payment_to:
        return int((payment_from + payment_to) / 2)
    elif payment_from:
        return int(payment_from * 1.2)
    elif payment_to:
        return int(payment_to * 0.8)


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
    vacancies = {'objects': []}
    page = 0
    pages_number = 1
    while page < pages_number:
        response = requests.get(url, params=url_params, headers=auth_token)
        if response.ok:
            vacancies['total'] = response.json()['total']
            for vacancy in response.json()['objects']:
                    vacancies['objects'].append(vacancy)
            if vacancies['total'] <= url_params['count']:
                page += 1
            else:
                vacancies['total'] -= url_params['count']
                pages_number += 1
                page += 1
    return vacancies


def get_json_info_from_vacancies_sj():
    result = TEMPLATE
    for language in PROGRAMMING_LANGUAGES:
        vacancies = get_vacancies_from_sj(language)
        result[language]['vacancies_found'] = vacancies['total']
        result[language]['vacancies_processed'] = 0
        result[language]['average_salary'] = 0
        for vacancy in vacancies['objects']:
            salary = predict_rub_salary_sj(vacancy['payment_from'], vacancy['payment_to'])
            if salary:
                result[language]['average_salary'] += salary
                result[language]['vacancies_processed'] += 1
        try:
            result[language]['average_salary'] = \
                int(result[language]['average_salary']/result[language]['vacancies_processed'])
        except ZeroDivisionError:
            result[language]['average_salary'] = 0
    return result
