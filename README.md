# Автор: Трефелова Алина

(Я не понимаю, какой файл дан в задании с целевыми показателями и данными для вывода, потому что в единственном vacancies.csv, который нам давали на контесте только один год - 2022 (и в vacancies_medium.csv тоже), а в том файле, который был дан в 5.3 (1.6.3), vacancies_by_year.csv - от 2007 до 2022, и обрабатывается он намного дольше, чем 3сек. Если данные, которые даны нам в примере - просто пример и вывод должен быть не таким, то простите пожалуйста, но я правда не понимаю...)

## Тестирование:

- Отчёт о тестировании на doctest

![](Screenshots/doctest.PNG)

- Отчёт о тестировании на unittest

![](Screenshots/unittest.PNG)

## Профилирование:
### Без многопроцессорной обработки

- При печати вакансий

![](Screenshots/vacanciesProfile.PNG)

- При генерации отчёта
(Здесь профилирование было с файлом vacancies_medium)

![](Screenshots/statisticsProfile.PNG)

- При форматировании даты: 

Функция formatterDataDatetime

![](Screenshots/datetimeProfile.PNG)

Функция formatterDataStr

![](Screenshots/strProfile.PNG)

Функция formatterDataRe (переименована)

![](Screenshots/reProfile.PNG)

### Concurrent futures

![](Screenshots/multiProfile.PNG)

## Разделённые csv-файлы:

![](Screenshots/separateFiles.PNG)