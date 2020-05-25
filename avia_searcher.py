import json
import re
import sys
import urllib.request
from urllib.error import URLError, HTTPError
from airport_info import AirportInfo
from flight_info import FlightInfo

with open('config.txt') as file:
    API_KEY = file.read()
datetime_regex = re.compile(
    r'([\d]{4})-([\d]{2})-([\d]{2})T(\d\d:\d\d):\d\d([\+\-]\d\d):\d\d')


def stringify_duration(duration):
    """Converts seconds to Nh Nmin string"""
    duration /= 60
    hours = 0
    while duration >= 60:
        duration -= 60
        hours += 1

    return '{hours} ч {minutes} мин'.format(hours=hours, minutes=int(duration))


def stringify_flight_info(number, flight_info):
    """Visually complex, but makes output beautiful"""
    duration_string = stringify_duration(flight_info.duration)
    raw_str = ('=' * 80 +
               '\n| {num} | {flight_number}, {company}' +
               ' ' * (72-len(flight_info.number)-len(flight_info.company) -
                      len(str(number))) + '|' +
               '\n|' + '-'*78 + '|' +
               '\n| {from_city}, {from_airport}' +
               ' ' * 17 + '{to_city}, {to_airport}' + ' ' * (
                       56 - len(flight_info.start.name) -
                       len(flight_info.start.city) -
                       len(flight_info.end.name) -
                       len(flight_info.end.city)) + '|' +
               '\n| ({from_airport_code})' +
               ' ' * (len(flight_info.start.name) +
                      len(flight_info.start.city) - 2) +
               '  ==========>   ({to_airport_code})' +
               ' '*(53-len(flight_info.start.city) -
                    len(flight_info.start.name)) + '|' +
               '\n| {depart_datetime}' +
               ' ' * (len(flight_info.start.name) +
                      len(flight_info.start.city) + 2) +
               ' {arrival_datetime}' + ' ' * (42-len(flight_info.start.city) -
                                              len(flight_info.start.name)) +
               '|' +
               '\n|' + '-'*78 + '|' +
               '\n| {aircraft_type} | Длительность рейса: {duration}' +
               ' '*(54 - len(flight_info.aircraft_type) -
                    len(duration_string)) + '|')
    return raw_str.format(
        num=number,
        flight_number=flight_info.number,
        company=flight_info.company,
        from_city=flight_info.start.city,
        from_airport=flight_info.start.name,
        to_city=flight_info.end.city,
        to_airport=flight_info.end.name,
        from_airport_code=flight_info.start.iata_code,
        to_airport_code=flight_info.end.iata_code,
        depart_datetime=flight_info.depart_datetime,
        arrival_datetime=flight_info.arrival_datetime,
        aircraft_type=flight_info.aircraft_type,
        duration=duration_string
    )


def get_timezone_and_datetime(date_string):
    """Parse 2020-06-25T07:30:00+03:00 string"""
    raw_data = [x for x in datetime_regex.findall(date_string)[0]]
    datetime = '{day}/{month}/{year} {time}'.format(
        day=raw_data[2], month=raw_data[1], year=raw_data[0], time=raw_data[3])
    raw_timezone = raw_data[-1]
    if raw_timezone.find('+') != -1:
        timezone = int(raw_timezone[1:])
    else:
        timezone = -int(raw_timezone[1:])

    return datetime, timezone


def print_flights(flights, start_code, end_code):
    """Parse JSON and print flights info"""
    print('_' * 80)

    if len(flights) == 0:
        print('Не найдено прямых рейсов между аэропортами')
        return

    print('Найдено рейсов: {}'.format(len(flights)))

    number = 1
    for flight in flights:
        depart_datetime, from_utc = get_timezone_and_datetime(
            flight['departure'])
        arrival_datetime, to_utc = get_timezone_and_datetime(flight['arrival'])
        start_city, end_city = flight['thread']['title'].split(' — ')
        start = AirportInfo(flight['from']['title'], start_code, start_city,
                            from_utc)
        end = AirportInfo(flight['to']['title'], end_code, end_city, to_utc)
        flight_number = flight['thread']['number']
        aircraft_type = flight['thread']['vehicle']
        duration = flight['duration']
        company = flight['thread']['carrier']['title']
        flight_info = FlightInfo(flight_number, start, end, company,
                                 depart_datetime, arrival_datetime,
                                 duration, aircraft_type)

        print(stringify_flight_info(number, flight_info))
        number += 1

    print('=' * 80)

    epilogue = ('Указано местное время.\n' +
                'Часовой пояс аэропорта вылета: UTC{from_utc}\n' +
                'Часовой пояс аэропорта прилета: UTC{to_utc}\n' +
                '\n   Данные предоставлены сервисом Яндекс.Расписания > ' +
                'http://rasp.yandex.ru')
    from_utc = from_utc if from_utc < 0 else '+' + str(from_utc)
    to_utc = to_utc if to_utc < 0 else '+' + str(to_utc)
    print(epilogue.format(from_utc=from_utc, to_utc=to_utc))


def load_data(start_code, end_code, date):
    """Fetch data in JSON"""
    print('Ищем рейсы...\r', end='')

    link = ('https://api.rasp.yandex.net/v3.0/search/?from={start_code}' +
            '&to={end_code}&format=json&apikey={api_key}={date}' +
            '&transport_types=plane&system=iata')
    link = link.format(start_code=start_code, end_code=end_code,
                       api_key=API_KEY, date=date)

    try:
        with urllib.request.urlopen(link) as page:
            data = json.loads(page.read().decode('utf-8'))
    except (URLError, HTTPError) as err:
        print('Маршрут не найден.\n' +
              'Проверьте введенные данные и подключение к интернету')
        return None

    return data['segments']


def print_help():
    """-h, --help handler"""
    with open('help.txt', 'r', encoding='utf-8') as file:
        print(file.read())


def main(args):
    """Args handler"""
    if len(args) > 1 or len(args) == 1 and args[0] not in ['-h', '--help']:
        print('Неверный аргумент, используйте -h или --help для справки')
        return
    elif len(args) == 1 and args[0] in ['-h', '--help']:
        print_help()
        return

    start_code = input('Введите IATA-код аэропорта отправления: ')
    end_code = input('Введите IATA-код аэропорта прибытия: ')
    date = input('Введите дату вылета в формате YYYY-MM-DD: ')

    if re.fullmatch('\d\d\d\d-\d\d-\d\d', date) is None:
        print('Дата введена в неверном формате')
        return

    flights = load_data(start_code, end_code, date)
    if flights is None:
        return
    print_flights(flights, start_code, end_code)


if __name__ == '__main__':
    main(sys.argv[1:])
