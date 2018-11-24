import click
from weather import Weather, Unit

TODAY = 0

def print_weather(city, weather, unit, days):
    weather_info = weather.forecast
    weather_condition = weather.condition.text
    # count parameter was added to avoid printing line num' 17 more than once.
    count = 0
    for day in range(int(days)+1):
        if day is TODAY:
            print("The weather in {city} today is {condition} with temperatures trailing from {low} - {high} {unit}"
                  .format(city=city, condition=weather_condition, low=weather_info[day].low,
                          high=weather_info[day].high, unit=unit.lower()))
        else:
            if count == 0:
                print('Forecast for the next ' + days + ' days')
                count += 1
            print(weather_info[day].date + ' ' + weather_condition + ' with temperatures trailing from ' +
                  weather_info[day].low + '-' + weather_info[day].high + ' ' + unit.lower())

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
