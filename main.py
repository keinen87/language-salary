from head_hunter import predict_rub_salary_hh, get_info_from_hh
from settings import PROGRAMMING_LANGUAGES
from superjob import predict_rub_salary_sj, get_info_from_sj
from terminaltables import SingleTable


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

    print_vacancy_info('HeadHunter Moscow', get_info_from_hh())
    print_vacancy_info('SuperJob Moscow', get_info_from_sj())
