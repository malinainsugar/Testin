import csv
import re
import datetime
import os
import sys
from statistics import mean
import matplotlib.pyplot as plt
import matplotlib as mlt
import numpy as np

class report:
    def generate_image(self, dataList : list, nameProffesion):

        x = np.arange(min(dataList[0]), max(dataList[0]) + 1) - 0.25

        vacanciesCity = {}

        for key, value in dataList[6].items():
            if len(vacanciesCity) <= 10:
                vacanciesCity.update({key: value})
            else:
                vacanciesCity.update({"Другие": vacanciesCity.get('Другие', value) + value})

        plt.rc('font', size=8)
        width = 0.5
        plt.subplot(2, 2, 1)
        plt.title('Уровень зарплат по годам')
        salaryYear = plt.bar(x, dataList[1].values(), width)
        selectedSalaryYear = plt.bar(x + width, dataList[2].values(), width)
        plt.grid(axis = 'y')
        plt.xticks(dataList[0], rotation=90, horizontalalignment='center')
        plt.legend([salaryYear, selectedSalaryYear], ['средняя з/п', f'з/п {nameProffesion}'])

        plt.subplot(2, 2, 2)
        plt.title('Количество вакансий по годам')
        plt.xticks(dataList[0], rotation=90, horizontalalignment='center')
        plt.grid(axis = 'y')
        numberVacancies = plt.bar(x, dataList[3].values(), width)
        selectedNumberVacancies = plt.bar(x + width, dataList[4].values(), width)
        plt.legend([numberVacancies, selectedNumberVacancies], ['Количество вакансий', f'Количество вакансий \n {nameProffesion}'])

        plt.subplot(2, 2, 3)
        plt.title('Уровень зарплат по городам')
        salaryCityIndex = [key.replace(" ","\n").replace("-","-\n") for key in dataList[5].keys()]
        salaryCityValues = list(dataList[5].values())
        plt.yticks( horizontalalignment='right', verticalalignment="center", fontsize=6)
        plt.gca().invert_yaxis()
        plt.barh(salaryCityIndex, salaryCityValues)

        plt.subplot(2, 2, 4)
        plt.title('Доля вакансий по городам')
        plt.pie(vacanciesCity.values(), labels = vacanciesCity.keys(), textprops={"fontsize":6})

        plt.tight_layout()


        plt.savefig('graph.png')
        


#class DataSet - отвечает за чтение и подготовку данных из CSV-файла (универсальный парсер CSV)
class DataSet:
  def __init__(self):
    self.file_name = input("Введите название файла: ")

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
    vacanciesCity = sorted({key: round(value / self.counts, 4) for key, value in self.vacanciesСity.items()}.items(), key=lambda item: item[1], reverse=True)

    print('Динамика уровня зарплат по годам:', salaryYear)
    print('Динамика количества вакансий по годам:', numberVacancies)
    print('Динамика уровня зарплат по годам для выбранной профессии:', selectedSalaryYear)
    print('Динамика количества вакансий по годам для выбранной профессии:', selectedNumberVacancies)
    print('Уровень зарплат по городам (в порядке убывания):', salaryCity)
    print('Доля вакансий по городам (в порядке убывания):', dict(vacanciesCity[0:10]))
    
    return [self.years ,salaryYear, selectedSalaryYear, numberVacancies, selectedNumberVacancies, salaryCity, dict(vacanciesCity)]


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

  graph = report()
  graph.generate_image(dataList, parameters.nameProfession)


dataProcessing()