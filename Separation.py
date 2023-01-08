import csv
from statistics import mean

class Separation:
    """Класс для представления и разделения файла
    
    Attributes:
        file_name (str): Имя входящего файла
        heading (list): Список заголовков
        years (set): Список лет
        currencies (set): Список входящих валют
    """
    def __init__(self):
        """Инициализирует объект Separation"""
        self.file_name = 'vacancies_with_skills.csv'
        self.years = set()
        self.currencies = ('USD', 'RUR', 'EUR', 'KZT', 'UAH', 'BYR')

    def separateCsv(self):
        """Считывает входной файл и разделяет его на несколько файлов по годам"""
        with open(self.file_name, encoding='utf-8') as file:
            reader = csv.reader(file)
            self.headingFrom = next(reader)
            self.headingFrom[0] = 'name'

            for line in reader:
                if len(line) < len(self.headingFrom):
                    continue

                if line[4] not in self.currencies:
                    continue

                if (line[2] != '' or line[3] != '') and line[4] in self.currencies:
                    date = f'{line[5][8:10]}.{line[5][5:7]}.{line[5][:4]}'

                    if self.curs[f'{line[5][:4]}-{line[5][5:7]}'][line[4]] != '':
                        if line[2] != '' and line[3] != '':
                            salary = int(mean((float(line[2]), float(line[3]))) * float(self.curs[f'{line[5][:4]}-{line[5][5:7]}'][line[4]]))
                        if line[2] != '':
                            salary = int(float(line[2]) * float(self.curs[f'{line[5][:4]}-{line[5][5:7]}'][line[4]]))
                        else:
                            salary = int(float(line[3]) * float(self.curs[f'{line[5][:4]}-{line[5][5:7]}'][line[4]]))
                    else:
                        continue
                else:
                    continue

                if len(line[1]) != 0:
                    line[1] = line[1].replace('\n', '&&&&')

                w_File = open(f'./years-csv/{date[6:]}.csv', 'a', encoding='utf-8')
                with w_File:
                    writer = csv.writer(w_File, lineterminator="\r")
                    if date[6:] not in self.years:
                        self.years.add(date[6:])
                        writer.writerow(self.headingTo)
                        writer.writerow([line[0], line[1], salary, date])
                        print(self.years)
                    else:
                        writer.writerow([line[0], line[1], salary, date])

    def parserCSVcur(self):
        """Считывает файл с валютами по месяцам"""
        with open('curs.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            self.headingC = next(reader)
            self.headingC[0] = "date"
            self.curs = {}
            for line in reader:
                cur = {self.headingC[i]: line[i] for i in range(len(self.headingC))}
                self.curs.update({cur['date'] : cur})

separation = Separation()
separation.parserCSVcur()
separation.separateCsv()