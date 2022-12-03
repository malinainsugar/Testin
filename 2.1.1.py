import csv
import re
import datetime
import os
import sys
from statistics import mean
from openpyxl import Workbook
from openpyxl.styles import Border, Font, Side, Alignment


class report:
    def __init__(self, nameProfession):
        self.vacanciesBook = Workbook()
        self.statisticsYear = self.vacanciesBook.active
        self.statisticsYear.title = "Статистика по годам"
        self.statisticsYear.append(['Год', 'Средняя зарплата', f'Средняя зарплата - {nameProfession}', 'Количество вакансий', f'Количество вакансий - {nameProfession}'])
        self.statisticsCity = self.vacanciesBook.create_sheet("Статистика по городам")
        self.statisticsCity.append(['Город', 'Уровень зарплат', '', 'Город', 'Доля вакансий'])
        self.column = ['A', 'B', 'C', 'D', 'E']

    def styleSetting (self):
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
          self.statisticsYear[f'{i}1'].font, self.statisticsCity[f'{i}1'].font  = ft, ft
        for i in range(2, 12):
          self.statisticsCity[f'E{i}'].alignment = Alignment(horizontal='right')
          
        
        report.editWidthColumn(self, self.statisticsYear)
        report.editWidthColumn(self, self.statisticsCity)

        self.statisticsCity.column_dimensions['C'].width = 2
    
    def editWidthColumn (self, sheet):
      colsDict = {}
      for row in sheet.rows:
          for cell in row:
              if cell.value:
                  colsDict[cell.column_letter] = max((colsDict.get(cell.column_letter, 0), len(str(cell.value))))    
      for col, value in colsDict.items():
          sheet.column_dimensions[col].width = value + 2

    def generate_excel(self, dataList : list):

      for year in dataList[0]:
        self.statisticsYear.append([year, dataList[1][year], dataList[2][year], dataList[3][year], dataList[4][year]])

      for key, value in dataList[5].items():
        self.statisticsCity.append({'A' : key, 'B' : value})
      for key, value in dataList[6].items():
        self.statisticsCity.append({'D' : key, 'E' : "{:.2f}%".format(float(value * 100))})

      self.statisticsCity.move_range('D12:E21', rows=-10)

      report.styleSetting(self)
      self.vacanciesBook.save('report.xlsx')



#class DataSet - отвечает за чтение и подготовку данных из CSV-файла (универсальный парсер CSV)
class DataSet:
  def __init__(self):
    #self.file_name = input("Введите название файла: ")
    self.file_name = 'vacancies_medium.csv'

  def universalParserCSV(self, parameters):
    with open(self.ﬁle_name, encoding='utf-8') as file:
      reader = csv.reader(file)
      self.heading = next(reader)
      self.heading[0] = "name"
      self.vacancies = []
      self.vibr = []
      for line in reader:
        fits = True
        if len(line) < len(self.heading):
          continue
        for check in line:
          if len(check) == 0:
            fits = False
            break
        if fits:
          vacancy = {self.heading[i]:line[i] for i in range(len(self.heading)) if self.heading[i] in ['name','salary_from','salary_to','salary_currency','area_name','published_at']}
          InputConect.filtering(parameters, vacancy)

#class InputConect - отвечает за обработку параметров
class InputConect:
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

  def filtering(self, vacancy : dict):
      year = int(vacancy['published_at'][0:4])
      self.counts += 1
      if year not in self.years:
        self.years.append(year)
      salary = int(mean((float(vacancy['salary_from']), float(vacancy['salary_to']))) * currency_to_rub[vacancy['salary_currency']])
      self.numberVacancies.update({year : self.numberVacancies.get(year, 0) + 1})
      self.salaryLevel.update({year : self.salaryLevel.get(year, []) + [salary]})
      if self.nameProfession in vacancy['name']:
        self.selectedNumberVacancies.update({year : self.selectedNumberVacancies.get(year, 0) + 1})
        self.selectedSalaryLevel.update({year : self.selectedSalaryLevel.get(year, []) + [salary]})
      self.vacanciesСity.update({vacancy['area_name'] : self.vacanciesСity.get(vacancy['area_name'], 0) + 1})
      self.salariesСity.update({vacancy['area_name'] :  self.salariesСity.get(vacancy['area_name'], []) + [salary]})
      if len(self.selectedNumberVacancies) == 0:
        self.selectedNumberVacancies.update({year : 0})
        self.selectedSalaryLevel.update({year : []})

  def print_vacancies(self):
    salaryYear = {key: int(mean(value)) for key, value in self.salaryLevel.items()}
    numberVacancies = self.numberVacancies
    selectedSalaryYear = {key: (int(mean(value)) if len(value) > 0 else 0) for key, value in self.selectedSalaryLevel.items()}
    selectedNumberVacancies = self.selectedNumberVacancies
    salaryCity = dict(sorted({key: int(mean(value)) for key, value in self.salariesСity.items()}.items(), key=lambda item: item[1], reverse=True)[0:10])
    vacanciesCity = dict(sorted({key: round(value / self.counts, 4) for key, value in self.vacanciesСity.items()}.items(), key=lambda item: item[1], reverse=True)[0:10])

    print('Динамика уровня зарплат по годам:', salaryYear)
    print('Динамика количества вакансий по годам:', numberVacancies)
    print('Динамика уровня зарплат по годам для выбранной профессии:', selectedSalaryYear)
    print('Динамика количества вакансий по годам для выбранной профессии:', selectedNumberVacancies)
    print('Уровень зарплат по городам (в порядке убывания):', salaryCity)
    print('Доля вакансий по городам (в порядке убывания):', vacanciesCity)

    return [self.years ,salaryYear, selectedSalaryYear, numberVacancies, selectedNumberVacancies, salaryCity, vacanciesCity]


currency_to_rub = { "AZN": 35.68,
                      "BYR": 23.91,
                      "EUR": 59.90,
                      "GEL": 21.74,
                      "KGS": 0.76,
                      "KZT": 0.13,
                      "RUR": 1,
                      "UAH": 1.64,
                      "USD": 60.66,
                      "UZS": 0.0055,}

def dataProcessing():
  file = DataSet()
  parameters = InputConect()

  file.universalParserCSV(parameters)
  dataList = parameters.print_vacancies()
  wb = report(parameters.nameProfession)
  wb.generate_excel(dataList)

dataProcessing()
