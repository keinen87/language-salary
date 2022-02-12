from head_hunter import get_vacancies_from_hh, extract_vacancies_from_hh
from superjob import get_vacancies_from_sj, extract_vacancies_from_sj
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


def predict_rub_salary(pay_from, pay_to):
    if pay_from and pay_to:
        return (pay_from + pay_to) / 2
    elif pay_from:
        return pay_from * 1.2
    elif pay_to:
        return pay_to * 0.8


def get_statistic(vacancies):
    result = {}
    result['vacancies_found'] = vacancies['total']
    result['vacancies_processed'] = 0
    result['average_salary'] = 0
    for vacancy in vacancies['objects']:
        if vacancy['currency'] and \
               vacancy['currency'] in ['RUR', 'rub']:
            salary = predict_rub_salary(vacancy['from'], vacancy['to'])
            if salary:
                result['average_salary'] += salary
                result['vacancies_processed'] += 1
    try:
        result['average_salary'] = \
            int(result['average_salary']/result['vacancies_processed'])
    except ZeroDivisionError:
        result['average_salary'] = 0
    return result


def print_vacancy_info(title, vacancies):
    table_data = [
    [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата'
    ]
    ]
    for language in vacancies:
        table_data.append([
            language,
            vacancies[language]['vacancies_found'],
            vacancies[language]['vacancies_processed'],
            vacancies[language]['average_salary']
            ])
    table_instance = SingleTable(table_data, title)
    print(table_instance.table)
    print()

if __name__ == '__main__':
    result_from_hh = {}
    result_from_sj = {}
    for language in PROGRAMMING_LANGUAGES:
        vacancies_list_from_hh = get_vacancies_from_hh(language)
        vacancies_from_hh = extract_vacancies_from_hh(vacancies_list_from_hh)
        vacancies_list_from_sj = get_vacancies_from_sj(language)
        vacancies_from_sj = extract_vacancies_from_sj(vacancies_list_from_sj)
        result_from_hh[language] = get_statistic(vacancies_from_hh)
        result_from_sj[language] = get_statistic(vacancies_from_sj)

    print_vacancy_info('HeadHunter Moscow', result_from_hh)
    print_vacancy_info('SuperJob Moscow', result_from_sj)
