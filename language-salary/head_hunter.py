import requests


def get_vacancies_from_hh(language):
    key_word = 'Программист'
    url = 'https://api.hh.ru/vacancies'
    url_params = {
        'text': '',
        'area': '1',
        'period': '30'
        }
    url_params['text'] = '{} {}'.format(key_word, language)
    vacancies_list = []
    page = 0
    pages_number = 100
    while page < pages_number:
        url_params['page'] = page
        response = requests.get(url, url_params)
        response.raise_for_status()
        vacancies_list.append(response.json())
        page += 1
        pages_number = response.json()['pages']
    return vacancies_list


def extract_vacancies_from_hh(vacancies_list):
    vacancies = {'objects': []}
    for scope_vacancies in vacancies_list:
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
