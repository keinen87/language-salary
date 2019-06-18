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
    vacancies = {'objects': []}
    page = 0
    pages_number = 100
    while page < pages_number:
        url_params['page'] = page
        response = requests.get(url, url_params)
        if response.ok:
            vacancies['total'] = response.json()['found']
            vacancies['objects'].extend(response.json()['items'])
            page += 1
            pages_number = response.json()['pages']
    return vacancies
