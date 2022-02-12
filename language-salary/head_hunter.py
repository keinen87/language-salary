import requests


def get_vacancies_from_hh(language):
    url = 'https://api.hh.ru/vacancies'
    url_params = {
        'text': f'Программист {language}',
        'area': '1',
        'period': '30'
        }
    vacancies = []
    page = 0
    pages_number = 100
    while page < pages_number:
        url_params['page'] = page
        response = requests.get(url, url_params)
        response.raise_for_status()
        vacancies.append(response.json())
        page += 1
        pages_number = response.json()['pages']
    return vacancies


def extract_vacancies_from_hh(pages):
    vacancies = {'objects': []}
    for scope_vacancies in pages:
        vacancies['objects'].extend(scope_vacancies['items'])
        vacancies['total'] = scope_vacancies['found']
    for vacancy in vacancies['objects']:
        vacancy['currency'] = None
        vacancy['from'] = None
        vacancy['to'] = None
        if vacancy['salary']:
            vacancy['currency'] = vacancy['salary']['currency']
            if vacancy['salary']['from'] and \
                    vacancy['salary']['from'] < 1000:
                vacancy['from'] = vacancy['salary']['from'] * 1000
            else:
                vacancy['from'] = vacancy['salary']['from']
            if vacancy['salary']['to'] and \
                    vacancy['salary']['to'] < 1000:
                vacancy['to'] = vacancy['salary']['to'] * 1000
            else:
                vacancy['to'] = vacancy['salary']['to']
    return vacancies
