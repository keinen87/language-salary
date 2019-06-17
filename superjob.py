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


def get_info_from_sj():
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
    result = TEMPLATE

    for language in PROGRAMMING_LANGUAGES:
        result[language]['vacancies_processed'] = 0
        result[language]['average_salary'] = 0
        url_params['keyword'] = language
        page = 0
        pages_number = 1
        vacancies = []
        while page < pages_number:
            response = requests.get(url, params=url_params, headers=auth_token)
            if response.ok:
                result[language]['vacancies_found'] = response.json()['total']
                total_vacancies = result[language]['vacancies_found']
                for item in response.json()['objects']:
                        vacancies.append(item)
                if total_vacancies <= url_params['count']:
                    page += 1
                else:
                    total_vacancies -= url_params['count']
                    pages_number += 1
                    page += 1
        for vacancy in vacancies:
            salary = predict_rub_salary_sj(vacancy['payment_from'], vacancy['payment_to'])
            if salary:
                result[language]['average_salary'] += salary
                result[language]['vacancies_processed'] += 1
        try:
            result[language]['average_salary'] = int(result[language]['average_salary']/result[language]['vacancies_processed'])
        except ZeroDivisionError:
            result[language]['average_salary'] = 0
    return result
