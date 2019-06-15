import os
import requests
from dotenv import load_dotenv
from terminaltables import SingleTable

PROGRAMMING_LANGUAGES = [
    'JavaScript',
    'Java',
    'Python',
    'Ruby',
    'PHP',
    'C++',
    'C#',
    'C',
    'Go',
    'Objective-C',
    'Scala',
    'Swift',
    'Typescript'
]


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


def predict_rub_salary_sj(payment_from, payment_to):
    if payment_from and payment_to:
        return int((payment_from + payment_to) / 2)
    elif payment_from:
        return int(payment_from * 1.2)
    elif payment_to:
        return int(payment_to * 0.8)


def get_info_from_hh(template):
    key_word = 'Программист'
    url = 'https://api.hh.ru/vacancies'
    url_params = {
        'text': '',
        'area': '1',
        'period': '30'
        }
    result = template
    for language in PROGRAMMING_LANGUAGES:
        url_params['text'] = '{} {}'.format(key_word, language)
        page = 0
        pages_number = 100
        vacancies = []
        while page < pages_number:
            url_params['page'] = page
            response = requests.get(url, url_params)
            if response.ok:
                vacancies.extend(response.json()['items'])
                page += 1
                pages_number = response.json()['pages']
        result[language]['vacancies_found'] = response.json()['found']
        for vacancy in vacancies:
            if predict_rub_salary_hh(vacancy):
                result[language]['average_salary'] += predict_rub_salary_hh(vacancy)
                result[language]['vacancies_processed'] += 1
        result[language]['average_salary'] = \
        int(result[language]['average_salary']/result[language]['vacancies_processed'])
    return result


def get_info_from_sj(template):
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
        'period': 30,
        'count': 100
        }
    result = template
    for language in PROGRAMMING_LANGUAGES:
        url_params['keyword'] = language
        page = 0
        pages_number = 500
        vacancies = []
        while page < pages_number:
            response = requests.get(url, params=url_params, headers=auth_token)
            if response.ok:
                for item in response.json()['objects']:
                        vacancies.append(item)
                page += url_params['count']
        result[language]['vacancies_found'] = response.json()['total']
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


def print_vacancy_info(title, vacancy_info):
    table_data = [
    [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата'
    ]
    ]
    for language in vacancy_info:
        table_data.append([
            language,
            vacancy_info[language]['vacancies_found'],
            vacancy_info[language]['vacancies_processed'],
            vacancy_info[language]['average_salary']
            ])
    table_instance = SingleTable(table_data, title)
    print(table_instance.table)
    print()

if __name__ == '__main__':

    template = {language: {
        'vacancies_found': 0,
        'vacancies_processed': 0,
        'average_salary': 0
    } for language in PROGRAMMING_LANGUAGES}

    print_vacancy_info('HeadHunter Moscow', get_info_from_hh(template))
    print_vacancy_info('SuperJob Moscow', get_info_from_sj(template))
