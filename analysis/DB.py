import sqlite3
import csv
import json
import pandas as pd


class DB:
    """Класс для работы с базами данных"""

    def citiesDB(salaryCity, vacanciesCity):
        """Заполняет таблицы salaryCity и vacanciesCity с результатами анализа по городам

        Args:
            salaryCity (dict) : Словарь уровней зарплат по городам
            vacanciesCity (dict) : Словарь количества вакансий по городам
        """
        conn = sqlite3.connect('statistics.db')
        cur = conn.cursor()

        for city in salaryCity:
            cur.execute("INSERT INTO salaryCity VALUES(?, ?);", (city, salaryCity[city]))
            conn.commit()

        for city in vacanciesCity:
            cur.execute("INSERT INTO vacanciesCity VALUES(?, ?);", (city, float(vacanciesCity[city] * 100)))
            conn.commit()

    def currenciesDB():
        """Заполняет таблицу currencies с данными о валютах"""

        conn = sqlite3.connect('statistics.db')
        cur = conn.cursor()

        with open('currencies.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            heading = next(reader)
            heading[0] = "date"
            currencies = {}
            for line in reader:
                currencies = {heading[i]: line[i] for i in range(len(heading))}
                cur.execute("INSERT INTO currencies VALUES(?, ?, ?, ?, ?, ?, ?);", (currencies['date'], currencies['USD'], currencies['KZT'], currencies['BYR'], currencies['UAH'], currencies['EUR'], currencies['RUR'], ))
                conn.commit()

    def yearsDB(dataList):
        """Заполняет таблицу years с результатами анализа по годам

        Args:
            dataList (dict) : Словарь словарей с результатами анализа
        """
        conn = sqlite3.connect('statistics.db')
        cur = conn.cursor()

        for year in dataList['years']:
            cur.execute("INSERT INTO currencies VALUES(?, ?, ?, ?, ?, ?);", (year, dataList['salaryYear'][year], dataList['numberVacancies'][year], dataList['selectedSalaryYear'][year], dataList['selectedNumberVacancies'][year], json.dumps(dataList['skills'][year])))
            conn.commit()  

    def vacanciesDB(self, file):
        """Заполняет таблицу vacancies вакансиями

        Args:
            file (str): Название файла для обработки
        """
        conn = sqlite3.connect('statistics.db')

        df = pd.read_csv(f'./cities-csv/{file}')
        df.to_sql('vacancies')

        conn.close()
