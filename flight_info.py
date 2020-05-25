class FlightInfo:
    """Class for flight information"""
    def __init__(self, number, start, end, company, depart_datetime,
                 arrival_datetime, duration, aircraft_type):
        self.number = number
        self.start = start
        self.end = end
        self.company = company
        self.depart_datetime = depart_datetime
        self.arrival_datetime = arrival_datetime
        self.duration = duration
        self.aircraft_type = (aircraft_type if aircraft_type is not None
                              else 'Тип самолета неизвестен')

    def __str__(self):
        raw_str = ('{flight}, {company}\nStart:{start}\n' +
                   'End:{end}\n' +
                   '{depart_time} - {arrival_time} ({duration})' +
                   '\n{aircraft_type}')

        return (raw_str.format(
                    flight=self.number,
                    start=self.start,
                    end=self.end,
                    company=self.company,
                    depart_time=self.depart_datetime,
                    arrival_time=self.arrival_datetime,
                    duration=self.duration,
                    aircraft_type=self.aircraft_type))
