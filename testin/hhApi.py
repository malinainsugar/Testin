from statistics import mean
import requests

class Vacancy:
    """Класс для представления вакансии

    Attributes:
        name (str): Название вакансии
        description (str): Описание вакансии
        key_skills (list): Список необходимых навыков
        employer_name (str): Компания, опубликовавшая вакансию
        salary (int): Оклад
        currency (str): Валюта
        area_name (str): Город (страна)
        published_at (str): дата публикации вакансии
    """

    def __init__(self, vacancy, salary):
        """Инициализирует объект Vacancy
        
        Args:
            vacancy (dict): Словарь со всей полученной информацией о вакансии
            salary (int): Оклад
        """

        self.name = vacancy["name"]
        self.description = vacancy["description"]
        self.key_skills = [skill['name'] for skill in vacancy["key_skills"]]
        self.employer_name = vacancy["employer"]["name"]
        self.salary = str(salary)[:-3] + ' ' + str(salary)[-3:]
        self.currency = 'руб.' if vacancy['salary']["currency"] == 'RUR' else vacancy['salary']["currency"]
        self.area_name = vacancy["area"]["name"]
        self.published_at = f'{vacancy["published_at"][8:10]}.{vacancy["published_at"][5:7]}.{vacancy["published_at"][:4]}'


class hhApi:
    """Класс для работы с ApiHH.ru"""

    def loadingVacancies(day, month, year, maxLen = 10):
        """Загружает вакансии за необходимый день
        
        Args:
            day (int): День публикации вакансии
            month (int): Месяц публикации вакансии
            year (int): Год публикации вакансии
            maxLen (int): Максимальное число вакансий (по умолчанию = 10)

        Returns:
            vacanciesList (list): Список полученных вакансий в виде объектов Vacancy
        """
        url = 'https://api.hh.ru/vacancies'
        vacanciesList = []
        nameProfession = ['тест', 'qa', 'test', 'quality', 'assurance']

        for hour in range(8, 23):
            response = requests.get(url, headers={}, params={
                'specialization': 1,
                "date_from": f"{year}-{month}-{day}T{str(hour).zfill(2)}:00:00+0300",
                "date_to": f"{year}-{month}-{day}T{str(hour + 1).zfill(2)}:59:00+0300"})

            for page in range((response.json()['found'] // 100) + 1):
                data = requests.get(url, headers={}, params={
                    'specialization': 1,
                    'only_with_salary': True,
                    'text': 'NAME: test OR qa OR quality OR Тестировщик',
                    'found': 1,
                    'per_page': 100,
                    'page': page,
                    "date_from": f"{year}-{month}-{day}T{str(hour).zfill(2)}:00:00+0300",
                    "date_to": f"{year}-{month}-{day}T{str(hour + 1).zfill(2)}:59:00+0300"}).json()

                for vacancy in data['items']:
                    vacancy = requests.get(url=f'https://api.hh.ru/vacancies/{vacancy["id"]}').json()

                    for name in nameProfession:
                        if name in vacancy["name"].lower():

                            if vacancy['salary']['from'] and vacancy['salary']['to']:
                                salary = mean([vacancy['salary']['from'], vacancy['salary']['to']])
                            else:
                                salary = vacancy['salary']['from'] if vacancy['salary']['from'] else vacancy['salary']['to']
                                
                            vacanciesList.append(Vacancy(vacancy, salary))

                            if len(vacanciesList) == maxLen:
                                return vacanciesList
                        break
                    
        return vacanciesList
