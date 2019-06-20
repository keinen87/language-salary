import requests


def extract_vacancies_from_hh(language):
    key_word = 'Программист'
    url = 'https://api.hh.ru/vacancies'
    url_params = {
        'text': '',
        'area': '1',
        'period': '30'
        }
    url_params['text'] = '{} {}'.format(key_word, language)
    vacancies = {'objects': []}
    page = 0
    pages_number = 100
    while page < pages_number:
        url_params['page'] = page
        response = requests.get(url, url_params)
        if response.ok:
            vacancies['total'] = response.json()['found']
            vacancies['objects'].extend(response.json()['items'])
            for vacancy in vacancies['objects']:
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
                else:
                    vacancy['currency'] = None
                    vacancy['from'] = None
                    vacancy['to'] = None
            page += 1
            pages_number = response.json()['pages']
    return vacancies
