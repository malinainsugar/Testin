from unittest import TestCase
from Table import Salary, Table, Vacancy

class SalaryTests (TestCase):
    vacancy = {'Нижняя граница вилки оклада': 500,
    'Верхняя граница вилки оклада': 1000,
    'Оклад указан до вычета налогов': "False",
    'Идентификатор валюты оклада': "EUR"}
    
    def testSalaryType(self):
        self.assertEqual(type(Salary(SalaryTests.vacancy)).__name__, 'Salary')

    def testSalaryFrom(self):
        SalaryTests.vacancy['Нижняя граница вилки оклада'] = 1000
        self.assertEqual(Salary(SalaryTests.vacancy).salary_from, '1 000')

    def testSalaryTo(self):
        SalaryTests.vacancy['Верхняя граница вилки оклада'] = 2500
        self.assertEqual(Salary(SalaryTests.vacancy).salary_to, '2 500')

    def testSalaryGross(self):
        self.assertEqual(Salary(SalaryTests.vacancy).salary_gross, "С вычетом налогов")



    def testSalaryConvertsToRubEUR(self):
        self.assertEqual(Salary(SalaryTests.vacancy).convertsToRub(), 44925.0)

    def testSalaryConvertsToRubRUR(self):
        SalaryTests.vacancy['Нижняя граница вилки оклада'] = 3600.0
        SalaryTests.vacancy['Верхняя граница вилки оклада'] = 124000
        SalaryTests.vacancy['Идентификатор валюты оклада'] = 'RUR'
        self.assertEqual(Salary(SalaryTests.vacancy).convertsToRub(), 63800.0)

    def testSalaryConvertsToRubUSD(self):
        SalaryTests.vacancy['Нижняя граница вилки оклада'] = 12
        SalaryTests.vacancy['Верхняя граница вилки оклада'] = 59.5
        SalaryTests.vacancy['Идентификатор валюты оклада'] = 'USD'
        self.assertEqual(Salary(SalaryTests.vacancy).convertsToRub(), 2153.43)


class VacancyTests (TestCase):
    def testVacancyCroppingСharactersStandard(self):
        self.assertEqual(Vacancy.croppingСharacters('Это абсурд, враньё: череп, скелет, коса.', 20), 'Это абсурд, враньё: ...')

    def testVacancyCroppingСharactersLess(self):
        self.assertEqual(Vacancy.croppingСharacters('Простишь ли мне ревнивые мечты...', 40), 'Простишь ли мне ревнивые мечты...')

    def testVacancyCroppingСharactersLong(self):
        self.assertEqual(Vacancy.croppingСharacters('«Он сошел вниз, избегая подолгу смотреть на нее, как на солнце, но он видел ее, как солнце, и не глядя» [Цитата из романа Льва Толстого «Анна Каренина».]', 100), '«Он сошел вниз, избегая подолгу смотреть на нее, как на солнце, но он видел ее, как солнце, и не гля...')

    def testVacancyCroppingСharactersZero(self):
        self.assertEqual(Vacancy.croppingСharacters('предпочитаю думать ни о чем', 0), '...')


class TableTests (TestCase):
    def testTableFormattingBordersFromTo(self):
        self.assertEqual(Table.formattingBorders([10, 20], [ 1, 2, 3, 4, 5]), (9, 19))

    def testTableFormattingBordersStart(self):
        self.assertEqual(Table.formattingBorders([1], [ 2, 9, "fff"]), (0, 3))

    def testTableFormattingBordersOne(self):
        self.assertEqual(Table.formattingBorders([1], [2]), (0, 1))

    def testTableFormattingBordersdifferentTypes(self):
        self.assertEqual(Table.formattingBorders([13, 50], [ 2, [9, 7], "fff"]), (12, 49))



    Table.isReverseSort = ''
    def testProcessingSortOrder(self):
        self.assertEqual(Table.processingSortOrder(Table), False)

    Table.isReverseSort = 'Да'
    def testProcessingSortOrder(self):
        self.assertEqual(Table.processingSortOrder(Table), True)

    Table.isReverseSort = 'Нет'
    def testProcessingSortOrder(self):
        self.assertEqual(Table.processingSortOrder(Table), False)

