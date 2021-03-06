# avia-searcher

Версия 1

Автор: Макаров Егор, КН-202

### Описание

Консольная утилита для поиска прямых рейсов между аэропортами. Работает на HTTP-запросах к API Яндекс.Расписаний

### Перед первым запуском

1. Сформировать ключ в [Кабинете разработчика](https://developer.tech.yandex.ru/) API Яндекса
2. Вставить ключ в файл `config.txt`

### Как работать с программой

Просто запустите avia_searcher.py и введите дату и IATA-коды аэропортов
отправления и прибытия.

`-h` — вызов справки

### Пример запуска

```
>python avia_searcher.py
Введите IATA-код аэропорта отправления: SVX
Введите IATA-код аэропорта прибытия: VKO
Введите дату вылета в формате YYYY-MM-DD: 2020-08-25
________________________________________________________________________________
Найдено рейсов: 2
================================================================================
| 1 | DP 406, Победа                                                           |
|------------------------------------------------------------------------------|
| Екатеринбург, Кольцово                 Москва, Внуково                       |
| (SVX)                    ==========>   (VKO)                                 |
| 25/08/2020 06:55                       25/08/2020 07:30                      |
|------------------------------------------------------------------------------|
| Boeing 737-800 | Длительность рейса: 2 ч 35 мин                              |
================================================================================
| 2 | DP 404, Победа                                                           |
|------------------------------------------------------------------------------|
| Екатеринбург, Кольцово                 Москва, Внуково                       |
| (SVX)                    ==========>   (VKO)                                 |
| 25/08/2020 07:55                       25/08/2020 08:30                      |
|------------------------------------------------------------------------------|
| Boeing 737-800 | Длительность рейса: 2 ч 35 мин                              |
================================================================================
Указано местное время.
Часовой пояс аэропорта вылета: UTC+5
Часовой пояс аэропорта прилета: UTC+3

   Данные предоставлены сервисом Яндекс.Расписания > http://rasp.yandex.ru
```