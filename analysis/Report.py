from statistics import mean
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Border, Font, Side, Alignment
from jinja2 import Environment, FileSystemLoader
import pdfkit
from collections import Counter

class Statistics:
    """Класс, представляющий методы для статистического анализа данных

    Attributes:
        nameProfession (list): Название профессии, которую нужно проанализировать
        salaryYear (dict): Динамика уровня зарплат по годам
        numberVacancies (dict): Динамика количества вакансий по годам
        selectedSalaryYear (dict): Динамика уровня зарплат по годам для выбранной профессии
        selectedNumberVacancies (dict): Динамика количества вакансий по годам для выбранной профессии
        salaryCity (dict): Уровень зарплат по городам
        vacanciesCity (dict): Доля вакансий по городам
        counts (int): Счётчик вакансий
        years (list): Список представленных лет
        skills (dict): Словарь топ-10 навыков по годам
    """
    def __init__(self):
        """Инициализирует объект Statistics"""
        #self.nameProfession = str(input("Введите название профессии: "))
        self.nameProfession = ['QA-инженер', 'тестировщик', 'qa', 'test', 'тест', 'quality assurance']
        self.salaryYear = {}
        self.numberVacancies = {}
        self.selectedSalaryYear = {}
        self.selectedNumberVacancies = {}
        self.salaryCity = {}
        self.vacanciesCity = {}
        self.counts = 0
        self.years = []
        self.skills = {}

    def filtering(self, vacancy: dict):
        """Анализирует данные вакансии, обновляет счетчики в словарях. 
        С помощью словаря currency_to_rub переводит зарплату в рубли.

        Args:
            vacancy (dict): Анализируемая вакансия
        """
        year = int(vacancy['published_at'][6:])
        self.counts += 1
        if year not in self.years:
            self.years.append(year)
        salary = int(vacancy['salary'])
        self.numberVacancies.update({year: self.numberVacancies.get(year, 0) + 1})
        self.salaryYear.update({year: self.salaryYear.get(year, []) + [salary]})
        for i in self.nameProfession:
            if i.lower() in vacancy['name'].lower():
                self.selectedNumberVacancies.update({year: self.selectedNumberVacancies.get(year, 0) + 1})
                self.selectedSalaryYear.update({year: self.selectedSalaryYear.get(year, []) + [salary]})
                if len(vacancy['key_skills']) != 0:
                    self.skills.update({year : self.skills.get(year, []) + vacancy['key_skills'].split('&&&&')})
                break
        self.vacanciesCity.update({vacancy['area_name']: self.vacanciesCity.get(vacancy['area_name'], 0) + 1})
        self.salaryCity.update({vacancy['area_name']: self.salaryCity.get(vacancy['area_name'], []) + [salary]})
        if len(self.selectedNumberVacancies) == 0:
            self.selectedNumberVacancies.update({year: 0})
            self.selectedSalaryYear.update({year: []})

    def print_vacancies(self):
        """Производит вывод полученных данных в консоль и выгрузку в базу данных statistics
        
        Returns:
            dict: Список полученных данных 
        """

        self.years.sort()
        salaryYear = dict(sorted({key: int(mean(value)) for key, value in self.salaryYear.items()}.items(), key = lambda item: item[0]))
        numberVacancies = dict(sorted(self.numberVacancies.items(), key = lambda item: item[0]))
        selectedSalaryYear = dict(sorted({key: (int(mean(value)) if len(value) > 0 else 0) for key, value in self.selectedSalaryYear.items()}.items(), key = lambda item: item[0]))
        selectedNumberVacancies = dict(sorted(self.selectedNumberVacancies.items(), key = lambda item: item[0]))
        for year, skills in self.skills.items():
            skills = Counter(skills)
            skills = dict(sorted(skills.items(), key = lambda item: item[1], reverse=True)[:10])
            self.skills.update({year : skills})
        self.skills = dict(sorted(self.skills.items(), key = lambda item: item[0]))
        salaryCity = dict(sorted({key: int(mean(value)) for key, value in self.salaryCity.items()}.items(), key=lambda item: item[1], reverse=True)[0:10])
        vacanciesCity = dict(sorted({key: round(value / self.counts, 4) for key, value in self.vacanciesCity.items()}.items(), key=lambda item: item[1], reverse=True)[0:10])

        print('Динамика уровня зарплат по годам:', salaryYear)
        print('Динамика количества вакансий по годам:', numberVacancies)
        print('Динамика уровня зарплат по годам для выбранной профессии:', selectedSalaryYear)
        print('Динамика количества вакансий по годам для выбранной профессии:', selectedNumberVacancies)
        print('Уровень зарплат по городам (в порядке убывания):', salaryCity)
        print('Доля вакансий по городам (в порядке убывания):', vacanciesCity)
        print(self.skills)
        print(self.years)

        return {'years': self.years, 'salaryYear': salaryYear, 'numberVacancies': numberVacancies,
        'selectedSalaryYear': selectedSalaryYear, 'selectedNumberVacancies': selectedNumberVacancies, 'skills': self.skills}

        


class Report:
    """Класс, генерирующий отчёт

    Attributes:
        nameProfession (str): Название профессии, которую нужно проанализировать
    """
    def __init__(self, nameProfession):
        """Инициализирует объект Report
        
        Args:
            nameProfession (str): Название профессии, которую нужно проанализировать
        """
        self.nameProfession = nameProfession

    def generate_excel(self, dataList: dict):
        """Генерирует Excel-файл (таблицу) со статистикой

        Args:
            dataList (dict): Данные о собранной статистике
        """
        vacanciesBook = Workbook()
        statisticsYear = vacanciesBook.active
        statisticsYear.title = "Статистика по годам"
        statisticsYear.append(
            ['Год', 'Средняя зарплата', f'Средняя зарплата - {self.nameProfession}', 'Количество вакансий',
             f'Количество вакансий - {self.nameProfession}'])
        statisticsCity = vacanciesBook.create_sheet("Статистика по городам")
        statisticsCity.append(['Город', 'Уровень зарплат', '', 'Город', 'Доля вакансий'])
        column = ['A', 'B', 'C', 'D', 'E']

        for year in dataList['years']:
            statisticsYear.append(
                [year, dataList['salaryYear'][year], dataList['selectedSalaryYear'][year], 
                    dataList['numberVacancies'][year], dataList['selectedNumberVacancies'][year]])

        for key, value in dataList['salaryCity'].items():
            statisticsCity.append({'A': key, 'B': value})
        for key, value in dataList['vacanciesCity'].items():
            statisticsCity.append({'D': key, 'E': "{:.2f}%".format(float(value * 100))})

        statisticsCity.move_range('D12:E21', rows=-10)

        self.styleSetting(statisticsYear, statisticsCity, column)
        vacanciesBook.save('report.xlsx')

    def styleSetting(self, statisticsYear, statisticsCity, column):
        """Настраивает внешний вид таблицы

        Args:
            statisticsYear (Workbook): Страница в таблице со статистикой по годам
            statisticsCity (Workbook): Страница в таблице со статистикой по городам
            column (list): Список столбцов в таблице
        """
        font_size = 11
        ft = Font(bold=True, size=font_size)
        borders = Border(left=Side(border_style='thin', color='00000000'),
                         right=Side(border_style='thin', color='00000000'),
                         top=Side(border_style='thin', color='00000000'),
                         bottom=Side(border_style='thin', color='00000000'))

        for row in statisticsYear.rows:
            for cell in row:
                if cell.value:
                    cell.border = borders
        for row in statisticsCity.rows:
            for cell in row:
                if cell.value:
                    cell.border = borders

        for i in column:
            statisticsYear[f'{i}1'].font, statisticsCity[f'{i}1'].font = ft, ft
        for i in range(2, 12):
            statisticsCity[f'E{i}'].alignment = Alignment(horizontal='right')

        self.editWidthColumn(statisticsYear)
        self.editWidthColumn(statisticsCity)

        statisticsCity.column_dimensions['C'].width = 2

    def editWidthColumn(self, sheet):
        """Отвечает за автоматическую ширину столбцов таблицы
        
        Args:
            sheet (Workbook): Форматируемая страница в Excel-файле
        """
        colsDict = {}
        for row in sheet.rows:
            for cell in row:
                if cell.value:
                    colsDict[cell.column_letter] = max((colsDict.get(cell.column_letter, 0), len(str(cell.value))))
        for col, value in colsDict.items():
            sheet.column_dimensions[col].width = value + 2

    def generate_image(self, dataList: dict):
        """Генерирует изображение со статистическими графиками

        Args:
            dataList (dict): Данные о собранной статистике
        """
        x = np.arange(min(dataList['years']), max(dataList['years']) + 1) - 0.25

        plt.rc('font', size=8)
        width = 0.5
        plt.subplot(2, 2, 1)
        plt.title('Уровень зарплат по годам')
        salaryYear = plt.bar(x, dataList['salaryYear'].values(), width)
        selectedSalaryYear = plt.bar(x + width, dataList['selectedSalaryYear'].values(), width)
        plt.grid(axis='y')
        plt.xticks(dataList['years'], rotation=90, horizontalalignment='center')
        plt.legend([salaryYear, selectedSalaryYear], ['средняя з/п', f'з/п {self.nameProfession}'])

        plt.subplot(2, 2, 2)
        plt.title('Количество вакансий по годам')
        plt.xticks(dataList['years'], rotation=90, horizontalalignment='center')
        plt.grid(axis='y')
        numberVacancies = plt.bar(x, dataList['numberVacancies'].values(), width)
        selectedNumberVacancies = plt.bar(x + width, dataList['selectedNumberVacancies'].values(), width)
        plt.legend([numberVacancies, selectedNumberVacancies],
                   ['Количество вакансий', f'Количество вакансий \n {self.nameProfession}'])

        plt.subplot(2, 2, 3)
        plt.title('Уровень зарплат по городам')
        salaryCityIndex = [key.replace(" ", "\n").replace("-", "-\n") for key in dataList['salaryCity'].keys()]
        salaryCityValues = list(dataList['salaryCity'].values())
        plt.yticks(horizontalalignment='right', verticalalignment="center", fontsize=6)
        plt.gca().invert_yaxis()
        plt.barh(salaryCityIndex, salaryCityValues)

        plt.subplot(2, 2, 4)
        plt.title('Доля вакансий по городам')
        others = 1 - sum(dataList['vacanciesCity'].values())
        vacanciesCity = dataList['vacanciesCity'].values() if others == 0 else [others] + list(dataList['vacanciesCity'].values())
        labels = dataList['vacanciesCity'].keys() if others == 0 else ['Другие'] + list(dataList['vacanciesCity'].keys())
        plt.pie(vacanciesCity, labels=labels, textprops={"fontsize": 6})

        plt.tight_layout()
        plt.savefig('graph.png', dpi=300)

    def generate_pdf(self, dataList: dict):
        """Генерирует pdf-отчёт

        Args:
            dataList (dict): Данные о собранной статистике
        """
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("pdf_template.html")

        pdf_template = template.render(
            {'nameProfessonal': self.nameProfession, 'image_file': 'graph.png', 'dataList': dataList})

        config = pdfkit.configuration(wkhtmltopdf=r'C:\wkhtmltox\bin\wkhtmltopdf.exe')
        pdfkit.from_string(pdf_template, 'report.pdf', configuration=config, options={'enable-local-file-access': ""})
