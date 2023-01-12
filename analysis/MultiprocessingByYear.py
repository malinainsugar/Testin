import concurrent.futures as pool
import os
import csv

class MultiprocessingByYear:
    """Класс, представляющий мультипроцессорную обработку данных

    Attributes:
        statistics (Statistics) : объект, хранящий общие результаты анализа
    """

    def __init__(self, statistics):
        """Инициализирует объект MultiprocessingByYear
        
        Args:
            statistics (Statistics): Объект классa Statistics, используется для анализа вакансий
        """
        self.statistics = statistics

    def asynchronousProcessing(self):
        """Производит мультипроцессорную обработку"""
        files = os.listdir(path='./years-csv')
        with pool.ThreadPoolExecutor(max_workers=len(files)) as p:
            p.map(self.parserCSVByYear, files)

    def parserCSVByYear(self, file_name):
        """Считывает входной файл, форматирует каждую вакансию и отправляет её на статистический анализ

        Args:
            file_name (str): Название входного файла
        """
        with open(f'./years-csv/{file_name}', encoding='utf-8') as file:
            reader = csv.reader(file)
            self.heading = next(reader)
            self.heading[0] = "name"
            for line in reader:
                vacancy = {self.heading[i]: line[i] for i in range(len(self.heading))}
                self.statistics.filtering(vacancy)
            print(file_name)
                