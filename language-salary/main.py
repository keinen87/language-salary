from head_hunter import extract_vacancies_from_hh
from settings import PROGRAMMING_LANGUAGES, TEMPLATE
from superjob import extract_vacancies_from_sj
from terminaltables import SingleTable


def predict_rub_salary(pay_from, pay_to):
    if pay_from and pay_to:
        return (pay_from + pay_to) / 2
    elif pay_from:
        return pay_from * 1.2
    elif pay_to:
        return pay_to * 0.8


def get_json_info_from_vacancies(language, vacancies):
    result = TEMPLATE
    result[language]['vacancies_found'] = vacancies['total']
    result[language]['vacancies_processed'] = 0
    result[language]['average_salary'] = 0
    for vacancy in vacancies['objects']:
        if vacancy['currency'] and \
               vacancy['currency'] == 'RUR' or 'rub':
            salary = predict_rub_salary(vacancy['from'], vacancy['to'])
            if salary:
                result[language]['average_salary'] += salary
                result[language]['vacancies_processed'] += 1
    try:
        result[language]['average_salary'] = \
            int(result[language]['average_salary']/result[language]['vacancies_processed'])
    except ZeroDivisionError:
        result[language]['average_salary'] = 0
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
    result_from_hh = result_from_sj = TEMPLATE
    for language in PROGRAMMING_LANGUAGES:
        vacancies_from_hh = extract_vacancies_from_hh(language)
        vacancies_from_sj = extract_vacancies_from_sj(language)
        result_from_hh.update(get_json_info_from_vacancies(language, vacancies_from_hh))
        result_from_sj.update(get_json_info_from_vacancies(language, vacancies_from_sj))
    print_vacancy_info('HeadHunter Moscow', result_from_hh)
    print_vacancy_info('SuperJob Moscow', result_from_sj)
