import csv

class Separation:
    """Класс для представления и разделения файла
    
    Attributes:
        file_name (str): Имя входящего файла
        heading (list): Список заголовков
        years (set): Список лет
    """
    def __init__(self):
        """Инициализирует объект Separation"""
        self.file_name = input("Введите название файла: ")
        self.years = set()

    def separateCsv(self):
        """Считывает входной файл и разделяет его на несколько файлов по годам"""
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
                    year = line[-1][:4]
                    w_File = open(f'./years-csv/{year}.csv', 'a', encoding='utf-8')
                    with w_File:
                        writer = csv.writer(w_File, lineterminator="\r")
                        if year not in self.years:
                            self.years.add(year)
                            writer.writerow(self.heading)
                            writer.writerow(line)
                        else:
                            writer.writerow(line)
                            print(year)

separation = Separation()
separation.separateCsv()