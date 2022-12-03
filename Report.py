from statistics import mean
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Border, Font, Side, Alignment
from jinja2 import Environment, FileSystemLoader
import pdfkit


class Statistics:
    def __init__(self):
        self.nameProfession = str(input("Введите название профессии: "))
        self.salaryLevel = {}
        self.numberVacancies = {}
        self.selectedSalaryLevel = {}
        self.selectedNumberVacancies = {}
        self.salariesСity = {}
        self.vacanciesСity = {}
        self.counts = 0
        self.years = []

    def filtering(self, vacancy: dict):
        year = int(vacancy['published_at'][0:4])
        self.counts += 1
        if year not in self.years:
            self.years.append(year)
        salary = int(mean((float(vacancy['salary_from']), float(vacancy['salary_to']))) * currency_to_rub[vacancy['salary_currency']])
        self.numberVacancies.update({year: self.numberVacancies.get(year, 0) + 1})
        self.salaryLevel.update({year: self.salaryLevel.get(year, []) + [salary]})
        if self.nameProfession in vacancy['name']:
            self.selectedNumberVacancies.update({year: self.selectedNumberVacancies.get(year, 0) + 1})
            self.selectedSalaryLevel.update({year: self.selectedSalaryLevel.get(year, []) + [salary]})
        self.vacanciesСity.update({vacancy['area_name']: self.vacanciesСity.get(vacancy['area_name'], 0) + 1})
        self.salariesСity.update({vacancy['area_name']: self.salariesСity.get(vacancy['area_name'], []) + [salary]})
        if len(self.selectedNumberVacancies) == 0:
            self.selectedNumberVacancies.update({year: 0})
            self.selectedSalaryLevel.update({year: []})

    def print_vacancies(self):
        salaryYear = {key: int(mean(value)) for key, value in self.salaryLevel.items()}
        numberVacancies = self.numberVacancies
        selectedSalaryYear = {key: (int(mean(value)) if len(value) > 0 else 0) for key, value in
                              self.selectedSalaryLevel.items()}
        selectedNumberVacancies = self.selectedNumberVacancies
        salaryCity = dict(sorted({key: int(mean(value)) for key, value in self.salariesСity.items()}.items(),
                                 key=lambda item: item[1], reverse=True)[0:10])
        vacanciesCity = dict(
            sorted({key: round(value / self.counts, 4) for key, value in self.vacanciesСity.items()}.items(),
                   key=lambda item: item[1], reverse=True)[0:10])

        print('Динамика уровня зарплат по годам:', salaryYear)
        print('Динамика количества вакансий по годам:', numberVacancies)
        print('Динамика уровня зарплат по годам для выбранной профессии:', selectedSalaryYear)
        print('Динамика количества вакансий по годам для выбранной профессии:', selectedNumberVacancies)
        print('Уровень зарплат по городам (в порядке убывания):', salaryCity)
        print('Доля вакансий по городам (в порядке убывания):', vacanciesCity)

        return [self.years, salaryYear, selectedSalaryYear, numberVacancies, selectedNumberVacancies, salaryCity,
                vacanciesCity]

class Report:
    def __init__(self, nameProfession):
        self.vacanciesBook = Workbook()
        self.nameProfession = nameProfession
        self.statisticsYear = self.vacanciesBook.active
        self.statisticsYear.title = "Статистика по годам"
        self.statisticsYear.append(
            ['Год', 'Средняя зарплата', f'Средняя зарплата - {self.nameProfession}', 'Количество вакансий',
             f'Количество вакансий - {nameProfession}'])
        self.statisticsCity = self.vacanciesBook.create_sheet("Статистика по городам")
        self.statisticsCity.append(['Город', 'Уровень зарплат', '', 'Город', 'Доля вакансий'])
        self.column = ['A', 'B', 'C', 'D', 'E']

    def styleSetting(self):
        self.font_size = 11
        ft = Font(bold=True, size=self.font_size)
        borders = Border(left=Side(border_style='thin', color='00000000'),
                         right=Side(border_style='thin', color='00000000'),
                         top=Side(border_style='thin', color='00000000'),
                         bottom=Side(border_style='thin', color='00000000'))

        for row in self.statisticsYear.rows:
            for cell in row:
                if cell.value:
                    cell.border = borders
        for row in self.statisticsCity.rows:
            for cell in row:
                if cell.value:
                    cell.border = borders

        for i in self.column:
            self.statisticsYear[f'{i}1'].font, self.statisticsCity[f'{i}1'].font = ft, ft
        for i in range(2, 12):
            self.statisticsCity[f'E{i}'].alignment = Alignment(horizontal='right')

        Report.editWidthColumn(self, self.statisticsYear)
        Report.editWidthColumn(self, self.statisticsCity)

        self.statisticsCity.column_dimensions['C'].width = 2

    def editWidthColumn(self, sheet):
        colsDict = {}
        for row in sheet.rows:
            for cell in row:
                if cell.value:
                    colsDict[cell.column_letter] = max((colsDict.get(cell.column_letter, 0), len(str(cell.value))))
        for col, value in colsDict.items():
            sheet.column_dimensions[col].width = value + 2

    def generate_excel(self, dataList: list):

        for year in dataList[0]:
            self.statisticsYear.append(
                [year, dataList[1][year], dataList[2][year], dataList[3][year], dataList[4][year]])

        for key, value in dataList[5].items():
            self.statisticsCity.append({'A': key, 'B': value})
        for key, value in dataList[6].items():
            self.statisticsCity.append({'D': key, 'E': "{:.2f}%".format(float(value * 100))})

        self.statisticsCity.move_range('D12:E21', rows=-10)

        Report.styleSetting(self)
        self.vacanciesBook.save('report.xlsx')

    def generate_image(self, dataList: list):

        x = np.arange(min(dataList[0]), max(dataList[0]) + 1) - 0.25

        plt.rc('font', size=8)
        width = 0.5
        plt.subplot(2, 2, 1)
        plt.title('Уровень зарплат по годам')
        salaryYear = plt.bar(x, dataList[1].values(), width)
        selectedSalaryYear = plt.bar(x + width, dataList[2].values(), width)
        plt.grid(axis='y')
        plt.xticks(dataList[0], rotation=90, horizontalalignment='center')
        plt.legend([salaryYear, selectedSalaryYear], ['средняя з/п', f'з/п {self.nameProfession}'])

        plt.subplot(2, 2, 2)
        plt.title('Количество вакансий по годам')
        plt.xticks(dataList[0], rotation=90, horizontalalignment='center')
        plt.grid(axis='y')
        numberVacancies = plt.bar(x, dataList[3].values(), width)
        selectedNumberVacancies = plt.bar(x + width, dataList[4].values(), width)
        plt.legend([numberVacancies, selectedNumberVacancies],
                   ['Количество вакансий', f'Количество вакансий \n {self.nameProfession}'])

        plt.subplot(2, 2, 3)
        plt.title('Уровень зарплат по городам')
        salaryCityIndex = [key.replace(" ", "\n").replace("-", "-\n") for key in dataList[5].keys()]
        salaryCityValues = list(dataList[5].values())
        plt.yticks(horizontalalignment='right', verticalalignment="center", fontsize=6)
        plt.gca().invert_yaxis()
        plt.barh(salaryCityIndex, salaryCityValues)

        plt.subplot(2, 2, 4)
        plt.title('Доля вакансий по городам')
        others = 1 - sum(dataList[6].values())
        vacanciesCity = dataList[6].values() if others == 0 else [others] + list(dataList[6].values())
        labels = dataList[6].keys() if others == 0 else ['Другие'] + list(dataList[6].keys())
        plt.pie(vacanciesCity, labels=labels, textprops={"fontsize": 6})

        plt.tight_layout()
        plt.savefig('graph.png', dpi=250)

    def generate_pdf(self, dataList: list):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("pdf_template.html")

        pdf_template = template.render(
            {'nameProfessonal': self.nameProfession, 'image_file': 'graph.png', 'dataList': dataList})

        config = pdfkit.configuration(wkhtmltopdf=r'C:\wkhtmltox\bin\wkhtmltopdf.exe')
        pdfkit.from_string(pdf_template, 'report.pdf', configuration=config, options={'enable-local-file-access': ""})

currency_to_rub = {"AZN": 35.68,
                       "BYR": 23.91,
                       "EUR": 59.90,
                       "GEL": 21.74,
                       "KGS": 0.76,
                       "KZT": 0.13,
                       "RUR": 1,
                       "UAH": 1.64,
                       "USD": 60.66,
                       "UZS": 0.0055,}