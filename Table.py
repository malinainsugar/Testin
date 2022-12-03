import re
import prettytable
import datetime


class Salary:
    def __init__(self, vacancy: dict):
        self.salary_from = '{0:,}'.format(int(float(vacancy["Нижняя граница вилки оклада"]))).replace(',', ' ')
        self.salary_to = '{0:,}'.format(int(float(vacancy["Верхняя граница вилки оклада"]))).replace(',', ' ')
        self.salary_gross = dictTranslationTaxes[vacancy["Оклад указан до вычета налогов"]]
        self.salary_currency = dictTranslationСurrency[vacancy["Идентификатор валюты оклада"]]

    def convertsToRub(lowerBound: int, upperBound: int, currency: str):
        return currency_to_rub[currency] * (int(upperBound.replace(' ', '')) + int(lowerBound.replace(' ', ''))) / 2

class Vacancy:
    def __init__(self, vacancy: dict):
        self.name = vacancy['Название']
        self.description = Vacancy.croppingСharacters(vacancy["Описание"], 100)
        self.key_skills = re.split("\n", Vacancy.formatterSkills(vacancy["Навыки"]))
        self.experience_id = dictTranslationExperience[vacancy["Опыт работы"]]
        self.premium = dictTranslationBool[vacancy["Премиум-вакансия"]]
        self.employer_name = vacancy['Компания']
        self.salary = Salary(vacancy)
        self.area_name = vacancy['Название региона']
        self.published_at = Vacancy.formatterData(vacancy["Дата публикации вакансии"])
        self.str_skills = Vacancy.croppingСharacters(Vacancy.formatterSkills(vacancy["Навыки"]), 100)

    def croppingСharacters(message: str, maxLen):
        if len(message) >= maxLen:
            return message[:maxLen] + "..."
        return message

    def formatterSkills(skills: str):
        return skills.replace('&&&&', '\n')

    def formatterData(data: str):
        return datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S%z")

    def returnsValues(self, parameterSort):
        heading = {"Название": self.name,
                   "Описание": self.description,
                   "Опыт работы": self.experience_id,
                   "Премиум-вакансия": self.premium,
                   "Компания": self.employer_name,
                   "Нижняя граница вилки оклада": self.salary.salary_from,
                   "Верхняя граница вилки оклада": self.salary.salary_to,
                   "Оклад указан до вычета налогов": self.salary.salary_gross,
                   "Идентификатор валюты оклада": self.salary.salary_currency,
                   "Название региона": self.area_name,
                   "Дата публикации вакансии": self.published_at, }
        return heading.get(parameterSort)

class Table:
    def __init__(self):
        self.parameterFilter = str(input("Введите параметр фильтрации: "))
        self.parameterSort = input("Введите параметр сортировки: ")
        self.isReverseSort = input("Обратный порядок сортировки (Да / Нет): ")
        self.borders = list(map(int, input("Введите диапазон вывода: ").split()))
        self.requiredColumns = list(input("Введите требуемые столбцы: ").split(", "))

    def checkingParameterValues(self):
        self.isFilter = True
        self.needPrint = True
        if self.parameterFilter == '':
            self.isFilter = False
        elif ":" not in self.parameterFilter:
            print("Формат ввода некорректен")
            self.needPrint = False
        return self.isFilter, self.needPrint

    # Проверка валидности вводимых данных
    def checkingEnteredValues(self):
        heading = ["№", "Название", "Нижняя граница вилки оклада", "Верхняя граница вилки оклада",
                   "Оклад указан до вычета налогов", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия",
                   "Компания", "Оклад", "Название региона", "Дата публикации вакансии", "",
                   "Идентификатор валюты оклада"]
        if self.isFilter:
            self.parameterFilter = list(self.parameterFilter.split(": "))
            if self.parameterFilter[0] not in heading and self.parameterFilter[0] != "Оклад":
                print("Параметр поиска некорректен")
                self.needPrint = False
        if self.parameterSort not in heading:
            print("Параметр сортировки некорректен")
            self.needPrint = False
        elif self.isReverseSort not in ["Да", "Нет", ""]:
            print("Порядок сортировки задан некорректно")
            self.needPrint = False
        return self.needPrint, self.parameterFilter

    # Обработка поля ввода обратной сортировки
    def processingSortOrder(self):
        if self.isReverseSort == "":
            return False
        else:
            return dictTranslationBool[self.isReverseSort]

    def sortedSkills(self, obje):
        return len(obje.key_skills)

    # Сортировка ваканский
    def sortingVacancies(self, vacancies_list: list):
        if self.parameterSort == "Навыки":
            return vacancies_list.sort(key=lambda vacancy: len(vacancy.key_skills), reverse=self.isReverseSort)
        if self.parameterSort == "Опыт работы":
            return vacancies_list.sort(key=lambda vacancy: dictSortionExperience[vacancy.experience_id],
                                       reverse=self.isReverseSort)
        if self.parameterSort == "Оклад":
            return vacancies_list.sort(
                key=lambda vacancy: Salary.convertsToRub(vacancy.salary.salary_from, vacancy.salary.salary_to,
                                                         vacancy.salary.salary_currency), reverse=self.isReverseSort)
        return vacancies_list.sort(key=lambda vacancy: vacancy.returnsValues(self.parameterSort),
                                   reverse=self.isReverseSort)

    # Форматирование границ таблицы
    def formattingBorders(self, s: list, vacancies: list):
        if len(s) == 0:
            return 0, len(vacancies)
        if len(s) == 1:
            return s[0] - 1, len(vacancies)
        return s[0] - 1, s[1] - 1

    # Форматирование колонок таблицы
    def formattingFields(self):
        if self.requiredColumns == ['']:
            return self.vacanciesTable.field_names
        self.requiredColumns.insert(0, "№")
        return self.requiredColumns

    # Печать таблицы
    def print_vacancies(self, data_vacancies: list):
        self.vacanciesTable = prettytable.PrettyTable()
        maxWidth = 20
        self.vacanciesTable.field_names = ["№", "Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия",
                                           "Компания", "Оклад", "Название региона", "Дата публикации вакансии"]
        self.vacanciesTable._max_width = {"№": 2, "Название": maxWidth, "Описание": maxWidth,
                                          "Навыки": maxWidth, "Опыт работы": maxWidth, "Премиум-вакансия": maxWidth,
                                          "Компания": maxWidth, "Оклад": maxWidth, "Название региона": maxWidth,
                                          "Дата публикации вакансии": maxWidth}
        self.vacanciesTable.align = "l"
        self.vacanciesTable.hrules = prettytable.ALL
        self.vacanciesTable.header = True
        counter = 1
        startingNumberVacancy, finalNumberVacancy = self.formattingBorders(self.borders, data_vacancies)
        for vacancy in data_vacancies:
            rows = [counter, vacancy.name, vacancy.description, vacancy.str_skills, vacancy.experience_id,
                    vacancy.premium, vacancy.employer_name,
                    f'{vacancy.salary.salary_from} - {vacancy.salary.salary_to} ({vacancy.salary.salary_currency}) ({vacancy.salary.salary_gross})',
                    vacancy.area_name, vacancy.published_at.strftime("%d.%m.%Y")]
            if self.isFilter == False:
                counter += 1
                self.vacanciesTable.add_row(rows)
            else:
                if self.parameterFilter[0] == 'Оклад':
                    if int(vacancy.salary.salary_to.replace(' ', '')) >= int(self.parameterFilter[1]) and int(
                            vacancy.salary.salary_from.replace(' ', '')) <= int(self.parameterFilter[1]):
                        counter += 1
                        self.vacanciesTable.add_row(rows)
                elif self.parameterFilter[0] == 'Навыки':
                    skills = self.parameterFilter[1]
                    isEnterSkills = True
                    skills = list(skills.split(", "))
                    for skill in skills:
                        if skill not in vacancy.key_skills:
                            isEnterSkills = False
                            break
                    if isEnterSkills == True:
                        counter += 1
                        self.vacanciesTable.add_row(rows)
                elif self.parameterFilter[0] == "Дата публикации вакансии":
                    if vacancy.published_at.strftime("%d.%m.%Y") == self.parameterFilter[1]:
                        counter += 1
                        self.vacanciesTable.add_row(rows)
                elif vacancy.returnsValues(self.parameterFilter[0]) == self.parameterFilter[1]:
                    counter += 1
                    self.vacanciesTable.add_row(rows)
        if len(self.vacanciesTable.rows) != 0:
            print(self.vacanciesTable.get_string(start=startingNumberVacancy, end=finalNumberVacancy,
                                                 ﬁelds=self.formattingFields()))
        else:
            print("Ничего не найдено")

currency_to_rub = {"Манаты": 35.68,
                   "Белорусские рубли": 23.91,
                   "Евро": 59.90,
                   "Грузинский лари": 21.74,
                   "Киргизский сом": 0.76,
                   "Тенге": 0.13,
                   "Рубли": 1,
                   "Гривны": 1.64,
                   "Доллары": 60.66,
                   "Узбекский сум": 0.0055
                    }

dictTranslationExperience = {"noExperience": "Нет опыта",
                             "between1And3": "От 1 года до 3 лет",
                             "between3And6": "От 3 до 6 лет",
                             "moreThan6": "Более 6 лет"}

dictSortionExperience = {"Нет опыта": 1,
                         "От 1 года до 3 лет": 2,
                         "От 3 до 6 лет": 3,
                         "Более 6 лет": 4}

dictTranslationСurrency = {"AZN": "Манаты",
                           "BYR": "Белорусские рубли",
                           "EUR": "Евро",
                           "GEL": "Грузинский лари",
                           "KGS": "Киргизский сом",
                           "KZT": "Тенге",
                           "RUR": "Рубли",
                           "UAH": "Гривны",
                           "USD": "Доллары",
                           "UZS": "Узбекский сум"}

dictTranslationBool = {"True": "Да",
                       "False": "Нет",
                       "Да": True,
                       "Нет": False,
                       "FALSE": "Нет",
                       "TRUE" : "Да"}

dictTranslationTaxes = {"False": "С вычетом налогов",
                        "True": "Без вычета налогов",
                        "FALSE" : "С вычетом налогов",
                        "TRUE" : "Без вычета налогов"}