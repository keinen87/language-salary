from head_hunter import get_vacancies_from_hh
from settings import PROGRAMMING_LANGUAGES, TEMPLATE
from superjob import get_vacancies_from_sj
from terminaltables import SingleTable


def predict_rub_salary(pay_from, pay_to):
    if pay_from and pay_to:
        if pay_from < 1000:
            pay_from *= 1000
        if pay_to < 1000:
            pay_to *= 1000
        return (pay_from + pay_to) / 2
    elif pay_from:
        if pay_from < 1000:
            pay_from *= 1000
        return pay_from * 1.2
    elif pay_to:
        if pay_to < 1000:
            pay_to *= 1000
        return pay_to * 0.8


def get_json_info_from_vacancies(job_service):
    result = TEMPLATE
    for language in PROGRAMMING_LANGUAGES:
        if job_service == 'hh':
            vacancies = get_vacancies_from_hh(language)
        elif job_service == 'sj':
            vacancies = get_vacancies_from_sj(language)
        result[language]['vacancies_found'] = vacancies['total']
        result[language]['vacancies_processed'] = 0
        result[language]['average_salary'] = 0
        for vacancy in vacancies['objects']:
            if job_service == 'hh':
                salary = vacancy['salary']
                if salary:
                    if salary['currency'] == 'RUR':
                        salary = predict_rub_salary(salary['from'], salary['to'])
                    else:
                        continue
            elif job_service == 'sj':
                salary = predict_rub_salary(vacancy['payment_from'], vacancy['payment_to'])
            if salary:
                result[language]['average_salary'] += salary
                result[language]['vacancies_processed'] += 1
        try:
            result[language]['average_salary'] = \
                int(result[language]['average_salary']/result[language]['vacancies_processed'])
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

    print_vacancy_info('HeadHunter Moscow', get_json_info_from_vacancies('hh'))
    print_vacancy_info('SuperJob Moscow', get_json_info_from_vacancies('sj'))
