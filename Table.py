import re
import prettytable
import datetime
import doctest


class Salary:
    """Класс для представления зарплаты.

    Attributes:
        salary_from (str): Нижняя граница вилки оклада
        salary_to (str): Верхняя граница вилки оклада
        salary_gross (str): Оклад указан до вычета налогов
        salary_currency (str): Валюта оклада
    """
    def __init__(self, vacancy: dict):
        """Инициализирует объект Salary, выполняет форматирование для целочисленных полей

        Args:
            vacancy (dict): Вакансия
        """
        self.salary_from = '{0:,}'.format(int(float(vacancy["Нижняя граница вилки оклада"]))).replace(',', ' ')
        self.salary_to = '{0:,}'.format(int(float(vacancy["Верхняя граница вилки оклада"]))).replace(',', ' ')
        self.salary_gross = dictTranslationTaxes[vacancy["Оклад указан до вычета налогов"]]
        self.salary_currency = dictTranslationСurrency[vacancy["Идентификатор валюты оклада"]]

    def convertsToRub(self):
        """Вычисляет среднюю зарплату и конвертирует её в рубли при помощи словаря - currency_to_rub

        Returns:
            float: средняя зарплата в рублях
        """
        return currency_to_rub[self.salary_currency] * (int(self.salary_from.replace(' ', '')) + int(self.salary_to.replace(' ', ''))) / 2

class Vacancy:
    """Класс для представления вакансии.

    Attributes:
        name (str): Название вакансии
        description (str): Описание вакансии
        key_skills (list): Список навыков
        experience_id (str): Опыт работы
        premium (bool or str): Премиум-вакансия
        employer_name (str): Название компании
        salary (Salary): Вся информация о зарплате
        area_name (str): Название региона
        published_at (datetime): Дата публикации вакансии
        str_skills (str): Строка навыков
    """
    def __init__(self, vacancy: dict):
        """Инициализирует объект Vacancy, выполняет форматирование различных полей с помощью функций и словарей: dictTranslationExperience и dictTranslationBool 

        Args:
            vacancy (dict): Вакансия
        """
        self.name = vacancy['Название']
        self.description = Vacancy.croppingСharacters(vacancy["Описание"], 100)
        self.key_skills = re.split("\n", vacancy["Навыки"].replace('&&&&', '\n'))
        self.experience_id = dictTranslationExperience[vacancy["Опыт работы"]]
        self.premium = dictTranslationBool[vacancy["Премиум-вакансия"]]
        self.employer_name = vacancy['Компания']
        self.salary = Salary(vacancy)
        self.area_name = vacancy['Название региона']
        self.published_at = datetime.datetime.strptime(vacancy["Дата публикации вакансии"], "%Y-%m-%dT%H:%M:%S%z")
        self.str_skills = Vacancy.croppingСharacters(vacancy["Навыки"].replace('&&&&', '\n'), 100)


    # def formatterDataDatetime(data: str):
    #     """Преобразует дату и время с помощью библиотеки datetime. Самый быстрый вариант, занял 0.007 sec
    #
    #     Args:
    #         data (str): строка с датой в формате Y-m-dTH:M:S+z
    #
    #     Returns:
    #         datetime: дата в формате %Y-%m-%dT%H:%M:%S%z
    #     """
    #     return datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S%z")

    # def formatterDataStr(data: str):
    #     """Преобразует дату в строку. Не самый быстрый вариант, занял 0.019 sec
    #
    #     Args:
    #         data (str): строка с датой в формате Y-m-dTH:M:S+z
    #
    #     Returns:
    #         str: дата в формате {d}.{m}.{y}
    #     """
    #     d = data[:4]
    #     m = data[5:7]
    #     y = data[8:10]
    #     return f'{d}.{m}.{y}'

    # def formatterDataRe(data : str):
    #     """Преобразует дату в строку. Не самый быстрый вариант, занял 0.018 sec
    #
    #     Args:
    #         data (str): строка с датой в формате Y-m-dTH:M:S+z
    #
    #     Returns:
    #         str: дата в формате {d}.{m}.{y}
    #     """
    #     yyyy, mm, dd, h, m, ss, *_ = re.split(r'[T:.-]', data)
    #     return f'{dd}/{mm}/{yyyy}'


    def croppingСharacters(message: str, maxLen : int):
        """Отвечает за то, чтобы строка была не более заданной длины.

        Args:
            message (str): Строка, которую необходимо проверить (при необходимости - обрезать)
            maxLen (int): Максимальная длина строки

        Returns:
            message (str): Обработанная строка

        >>> Vacancy.croppingСharacters('Это абсурд, враньё: череп, скелет, коса.', 20)
        'Это абсурд, враньё: ...'
        >>> Vacancy.croppingСharacters('Простишь ли мне ревнивые мечты...', 40)
        'Простишь ли мне ревнивые мечты...'
        >>> Vacancy.croppingСharacters('«Он сошел вниз, избегая подолгу смотреть на нее, как на солнце, но он видел ее, как солнце, и не глядя» [Цитата из романа Льва Толстого «Анна Каренина».]', 100)
        '«Он сошел вниз, избегая подолгу смотреть на нее, как на солнце, но он видел ее, как солнце, и не гля...'
        >>> Vacancy.croppingСharacters('предпочитаю думать ни о чем', 0)
        '...'
        """
        if len(message) >= maxLen:
            return message[:maxLen] + "..."
        return message

    def returnsValues(self, parameter):
        """Возвращает значение атрибута вакансии для сортировки и фильтрации
        
        Args:
            parameter (str): Искомый параметр

        Returns:
            parameter (str): Искомое значение
        """
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
                   "Дата публикации вакансии": self.published_at}
        return heading.get(parameter)

class Table:
    """Класс для представления таблицы

    Attributes:
        parameterFilter (str): Параметр фильтрации
        parameterSort (str): Параметр сортировки
        isReverseSort (str or bool): Обратный порядок сортировки (Да / Нет)
        borders (list): Диапазон вывода (строки)
        requiredColumns (list): Требуемые столбцы для вывода
        isFilter (bool): Нужна ли фильтрация
        needPrint (bool): Нужно ли печатать
        vacanciesTable (PrettyTable): Таблица
    """
    def __init__(self):
        """Инициализирует объект Table"""
        self.parameterFilter = str(input("Введите параметр фильтрации: "))
        self.parameterSort = input("Введите параметр сортировки: ")
        self.isReverseSort = input("Обратный порядок сортировки (Да / Нет): ")
        self.borders = list(map(int, input("Введите диапазон вывода: ").split()))
        self.requiredColumns = list(input("Введите требуемые столбцы: ").split(", "))

    def checkingParameterValues(self):
        """Проверяет корректность ввода параметра фильтрации

        Returns:
            needPrint (bool): Нужно ли печатать
        """
        self.isFilter = True
        self.needPrint = True
        if self.parameterFilter == '':
            self.isFilter = False
        elif ":" not in self.parameterFilter:
            print("Формат ввода некорректен")
            self.needPrint = False
        return self.needPrint

    def checkingEnteredValues(self):
        """Проверяет валидность вводимых данных
        
        Returns:
            needPrint (bool): Нужно ли печатать
        """
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
        return self.needPrint

    def processingSortOrder(self):
        """Обрабатывает поле ввода обратной сортировки
        
        Returns:
            isReverseSort (bool or str): Обратный порядок сортировки (Да / Нет)
        """
        if self.isReverseSort == "":
            return False
        else:
            return dictTranslationBool[self.isReverseSort]

    def sortingVacancies(self, vacancies_list: list):
        """Сортирует список вакансий
        
        Args:
            vacancies_list (list): Список ваканский, который необходимо отсортировать

        Returns:
            vacancies_list (list): Отсортированный список
        """
        if self.parameterSort == "Навыки":
            return vacancies_list.sort(key=lambda vacancy: len(vacancy.key_skills), reverse=self.isReverseSort)
        if self.parameterSort == "Опыт работы":
            return vacancies_list.sort(key=lambda vacancy: dictSortionExperience[vacancy.experience_id], reverse=self.isReverseSort)
        if self.parameterSort == "Оклад":
            return vacancies_list.sort(key=lambda vacancy: vacancy.convertsToRub(), reverse=self.isReverseSort)
        return vacancies_list.sort(key=lambda vacancy: vacancy.returnsValues(self.parameterSort), reverse=self.isReverseSort)

    def formattingBorders(s: list, vacancies: list):
        """Форматирует границы таблицы по длине
        
        Args:
            s (list): Границы таблицы
            vacancies (list): Список вакансий

        Returns:
            int, int: Границы таблицы

        >>> Table.formattingBorders([10, 20], [ 1, 2, 3, 4, 5])
        (9, 19)
        >>> Table.formattingBorders([1], [ 2, 9, "fff"])
        (0, 3)
        >>> Table.formattingBorders([1, 50], [ 2, [9, 7], "fff"])
        (0, 49)
        >>> Table.formattingBorders([1], [2])
        (0, 1)
        """
        if len(s) == 0:
            return 0, len(vacancies)
        if len(s) == 1:
            return s[0] - 1, len(vacancies)
        return s[0] - 1, s[1] - 1

    def formattingFields(self):
        """Определяет, заданны ли колонки таблицы

        Returns:
            list: Выводимые колонки
        """
        if self.requiredColumns == ['']:
            return self.vacanciesTable.field_names
        self.requiredColumns.insert(0, "№")
        return self.requiredColumns

    def print_vacancies(self, data_vacancies: list):
        """Печатает таблицу

        Args:
            data_vacancies (list): Список вакансий
        """
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
        startingNumberVacancy, finalNumberVacancy = Table.formattingBorders(self.borders, data_vacancies)
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