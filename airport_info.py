class AirportInfo:
    """Class for airport information"""
    def __init__(self, name, iata_code, city, utc):
        self.name = name
        self.iata_code = iata_code
        self.city = city
        self.utc = utc

    def __str__(self):
        return '({iata_code}) {name}, {city} / UTC{utc}'.format(
            iata_code=self.iata_code,
            name=self.name,
            city=self.city,
            utc=self.utc if self.utc < 0 else '+' + str(self.utc))
