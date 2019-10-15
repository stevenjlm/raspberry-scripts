import json
import logging
import urllib.request
import re
import LedBlink as ledb

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
QUERY_FILE = "./query.txt"
BAD_WEATHER = ["rain", "storm"]
BAD_WIND = 20
N_PERIODS = 2
# Weather check frequency
T_CHECK = 2*3600 # sec

log_format = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger('')
log.setLevel(logging.INFO)

terminal_handler = logging.StreamHandler()
terminal_handler.setFormatter(log_format)
log.addHandler(terminal_handler)

def load_query_url():
    with open(QUERY_FILE) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    api_url = content[0]
    return api_url

def call_nsw(url):
    contents = urllib.request.urlopen(url).read()
    return json.loads(contents.strip())

def extract_n_periods(forecast, n):
    return forecast["properties"]["periods"][:n]

def n_period_contains_string(forecast, n, match_string):
    props = extract_n_periods(forecast, n)
    all_forecast = ""
    for prop in props:
        detailed_forecast = prop["detailedForecast"]
        all_forecast = all_forecast + detailed_forecast.lower()
    match = all_forecast.find(match_string)
    if match == -1:
        return False
    else:
        return True

def check_bad_weather(forecast):
    for word in BAD_WEATHER:
        found_word = n_period_contains_string(forecast, N_PERIODS, word)
        if found_word == True:
            return True
    return False

def check_n_periods_wind(forecast):
    props = extract_n_periods(forecast, N_PERIODS)
    for prop in props:
        wind_speed = prop["windSpeed"]
        numbers = re.split("[^0-9]", wind_speed)
        numbers = [n for n in numbers if n != '']
        max_wind = max(numbers)
        if int(max_wind) > BAD_WIND:
            return True
    return False

def monitor_step(ldi):
    api_url = load_query_url()
    forecast = call_nsw(api_url)
    bad_weather = check_bad_weather(forecast)
    bad_wind = check_n_periods_wind(forecast)
    check_the_weather = bad_weather or bad_wind
    if check_the_weather:
        log.info("CAREFUL: You should check the weather before riding")
        ldi.led_on(T_CHECK)
    else:
        log.info("OK:      Weather should be ok to ride")
        ldi.pulse_down(T_CHECK)
    
def main():
    log.debug('Starting nsw query loop')
    ldi = ledb.LedInterface()
    while True:
        monitor_step(ldi)

if __name__ == "__main__":
    main()
