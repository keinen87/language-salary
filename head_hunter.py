import requests
from settings import PROGRAMMING_LANGUAGES, TEMPLATE


def predict_rub_salary_hh(vacancy):
    salary = vacancy['salary']
    if salary:
        if salary['currency'] == 'RUR':
            if salary['from'] and salary['to']:
                if salary['from'] < 1000:
                    salary['from'] *= 1000
                if salary['to'] < 1000:
                    salary['to'] *= 1000
                return (salary['from'] + salary['to']) / 2
            elif salary['from']:
                if salary['from'] < 1000:
                    salary['from'] *= 1000
                return salary['from'] * 1.2
            elif salary['to']:
                if salary['to'] < 1000:
                    salary['to'] *= 1000
                return salary['to'] * 0.8


def get_vacancies_from_hh(language):
    key_word = 'Программист'
    url = 'https://api.hh.ru/vacancies'
    url_params = {
        'text': '',
        'area': '1',
        'period': '30'
        }
    url_params['text'] = '{} {}'.format(key_word, language)
    vacancies = {'items': []}
    page = 0
    pages_number = 100
    while page < pages_number:
        url_params['page'] = page
        response = requests.get(url, url_params)
        if response.ok:
            vacancies['found'] = response.json()['found']
            vacancies['items'].extend(response.json()['items'])
            page += 1
            pages_number = response.json()['pages']
    return vacancies


def get_json_info_from_vacancies_hh():
    result = TEMPLATE
    for language in PROGRAMMING_LANGUAGES:
        vacancies = get_vacancies_from_hh(language)
        result[language]['vacancies_processed'] = 0
        result[language]['average_salary'] = 0
        result[language]['vacancies_found'] = vacancies['found']
        for vacancy in vacancies['items']:
            if predict_rub_salary_hh(vacancy):
                result[language]['average_salary'] += predict_rub_salary_hh(vacancy)
                result[language]['vacancies_processed'] += 1
        try:
            result[language]['average_salary'] = \
                int(result[language]['average_salary']/result[language]['vacancies_processed'])
        except ZeroDivisionError:
            result[language]['average_salary'] = 0
    return result
