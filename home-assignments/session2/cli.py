import click
from weather import Weather, Unit

def print_weather(p_city, p_weather, p_unit, p_days):
    weather_info = p_weather.forecast
    weather_condition = p_weather.condition.text
    count = 0
    for day in range(int(p_days)+1):
        if day == 0:
            print('The weather in ' + p_city + ' today is ' + weather_condition +
            ' with temperatures trailing from ' + weather_info[day].low + '-' + weather_info[day].high + ' ' +
                  p_unit.lower())
        else:
            if count == 0:
                print('Forecast for the next ' + p_days + ' days')
                count += 1
            print(weather_info[day].date + ' ' + weather_condition + ' with temperatures trailing from ' +
                  weather_info[day].low + '-' + weather_info[day].high + ' ' + p_unit.lower())

def parse_forecast_days_range(mixed_range):
    if '+' in mixed_range:
        days = mixed_range.split('+')[1]
    elif mixed_range == 'TODAY':
        days = 0
    return days

@click.command()
@click.option('--city', help='City for which forecast is needed')
@click.option('--forecast', help='Time range for the forecast.\n'
                                'Options:\n '
                                '1.TODAY.\n'
                                '2.TODAY+X(X-Number of days,'
                                 'Max number of days is 9)')
@click.option('-c', 'forecast_unit', flag_value='CELSIUS', help='Show temperature in Celsius')
@click.option('-f', 'forecast_unit', flag_value='FAHRENHEIT', help='Show temperature in Fahrenheit')

def get_weather(city, forecast, forecast_unit):
    """forecast for the next X days based on city and forecast(date) parameters."""
    forecast_time_range = parse_forecast_days_range(forecast)
    city_weather_info = Weather(unit=getattr(Unit, forecast_unit)).lookup_by_location(city)
    print_weather(city, city_weather_info, forecast_unit, forecast_time_range)

if __name__ == '__main__':
    get_weather()
