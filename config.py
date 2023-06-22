import configparser

config = configparser.ConfigParser()
config.read('config.ini')


DB_DRIVER = config.get('DB', 'driver')
DB_URL = config.get('DB', 'url')
RESERVATION_MAX_DURATON_HOURS = config.getint('Application', 'reservation_max_duration_hours')
RESERVATION_MAX_IN_FUTURE_HOURS = config.getint('Application', 'reservation_max_in_future_hours')

