from Table import Table, Vacancy
from Report import Statistics, Report
from MultiprocessingByYear import MultiprocessingByYear
import csv
import os
import sys
import re


class InputConnect:
    """Класс, отвечающий за выбор вывода информации о вакансиях

    Attributes:
        file (DataSet): Объект класса DataSet - инициализирует файл
        table (Table): Объект класса Table - инициализирует таблицу
        statistics (Statistics): Объект класса Statistics - используется для анализа вакансий
        report (Report): Объект класса Report - формирует итоговый отчёт
    """
    def __init__(self):
        """Инициализирует объект InputConnect"""
        #outputSelection = input("Вакансии или Статистика: ")
        outputSelection = 'Статистика'
        self.file = DataSet()

        if outputSelection == "Вакансии":
            self.table = Table()
            if self.table.checkingParameterValues():
                needPrint = self.table.checkingEnteredValues()
            if needPrint:
                vacancies = self.file.parserCSVforTable()
                if len(vacancies) > 0:
                    if self.table.parameterSort != "":
                        self.table.isReverseSort = self.table.processingSortOrder()
                        self.table.sortingVacancies(vacancies)
                    self.table.print_vacancies(vacancies)
                else:
                    print("Нет данных")

        if outputSelection == "Статистика":
            self.statistics = Statistics()
            asynchrony = MultiprocessingByYear(self.statistics)
            asynchrony.asynchronousProcessing()
            vacancies = self.statistics.print_vacancies()
            #report = Report(self.statistics.nameProfession)
            #report.generate_excel(vacancies)
            #report.generate_image(vacancies)
            #report.generate_pdf(vacancies)

class DataSet:
    """Класс для представления файла
    
    Attributes:
        file_name (str): Имя входящего файла
        heading (list): Список заголовков
        information (list): Список строк с вакансиями
        vacancies (list): Итоговый список вакансий
    """
    def __init__(self):
        """Инициализирует объект DataSet"""
        #self.file_name = input("Введите название файла: ")

    def parserCSVforReport(self, parameters):
        """Считывает входной файл, форматирует каждую вакансию и отправляет её на статистический анализ

        Args:
            parameters(Statistics): Объект классa Statistics, используется для анализа вакансий
        """
        with open(self.file_name, encoding='utf-8') as file:
            reader = csv.reader(file)
            self.heading = next(reader)
            self.heading[0] = "name"
            for line in reader:
                fits = True
                if len(line) < len(self.heading):
                    continue
                for check in line:
                    if len(check) == 0:
                        fits = False
                        break
                if fits:
                    vacancy = {self.heading[i]: line[i] for i in range(len(self.heading))}
                    parameters.filtering(vacancy)

    def parserCSVforTable(self):
        """Считывает входной файл, форматирует каждую вакансию, формируя общий список вакансий

        Returns:
            vacancies (list): Итоговый список вакансий
        """
        with open(self.file_name, encoding='utf-8') as file:
            if os.stat(self.file_name).st_size == 0:
                print("Пустой файл")
                sys.exit()
            reader = csv.reader(file)
            self.heading = next(reader)
            self.heading[0] = "name"
            self.information = []
            for line in reader:
                if len(line) < len(self.heading):
                    continue
                fits = True
                for check in line:
                    if len(check) == 0:
                        fits = False
                        break
                if fits:
                    self.information.append(line)
        self.translateHeading()
        self.vacancies = []
        tags = re.compile(r'<[^>]+>')
        for line in self.information:
            fits = True
            for key, value in enumerate(line):
                line[key] = ' '.join(re.sub(tags, '', value) \
                                     .replace('\n', '&&&&') \
                                     .replace('\r\n', ', ').split())
                if len(line[key]) == 0:
                    fits = False
                    break
            if fits:
                vacancy = {self.heading[i]: line[i] for i in range(len(self.heading))}
                self.vacancies.append(Vacancy(vacancy))
        return self.vacancies

    def translateHeading(self):
        """Переводит заголовки на русский язык при помощи словаря - dictTranslationHeading"""
        for i in range(len(self.heading)):
            for english, russian in dictTranslationHeading.items():
                if self.heading[i] == english:
                    self.heading[i] = russian

dictTranslationHeading = {"name": "Название",
                              "description": "Описание",
                              "key_skills": "Навыки",
                              "experience_id": "Опыт работы",
                              "premium": "Премиум-вакансия",
                              "employer_name": "Компания",
                              "salary_from": "Нижняя граница вилки оклада",
                              "salary_to": "Верхняя граница вилки оклада",
                              "salary_gross": "Оклад указан до вычета налогов",
                              "salary_currency": "Идентификатор валюты оклада",
                              "area_name": "Название региона",
                              "published_at": "Дата публикации вакансии"}