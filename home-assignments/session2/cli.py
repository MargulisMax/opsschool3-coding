import click
from weather import Weather, Unit

def print_weather(p_city, p_weather, p_unit, p_days):
    weather_info = p_weather.forecast
    weather_condition = p_weather.condition.text
    count = 0
    for day in range(int(p_days)+1):
        if day == 0:
            print('The weather in ' + p_city + ' today is ' + weather_condition +
            ' with temperatures trailing from ' + weather_info[day].low + '-' + weather_info[day].high + ' ' + p_unit)
        else:
            if count == 0:
                print('Forecast for the next ' + p_days + ' days')
                count += 1
            print(weather_info[day].date + ' ' + weather_condition + ' with temperatures trailing from ' +
                  weather_info[day].low + '-' + weather_info[day].high + ' ' + p_unit)

def unit_celsius():
    weather = Weather(unit=Unit.CELSIUS)
    unit_type = 'Celsius'
    return weather, unit_type

def unit_fahrenheit():
    weather = Weather(unit=Unit.FAHRENHEIT)
    unit_type = 'Fahrenheit'
    return weather, unit_type

def set_forecast_unit(unit_input):
    if unit_input == '-c':
        set_unit = unit_celsius()
    elif unit_input == '-f':
        set_unit = unit_fahrenheit()
    return set_unit

def parse_forecast_days_range(mixed_range):
    if '+' in mixed_range:
        days = mixed_range.split('+')[1]
    elif mixed_range == 'TODAY':
        days = 0
    return days

@click.command()
@click.option('--city', help='City for which forecast is needed')
@click.option('--forecast', type=(str, str), help='Time range for the forecast,'
                                                  'Options: TODAY, TODAY+X(X - stands for number of days)')

def get_weather(city, forecast):
    """forecast for the next X days based on city and forecast(date) parameters."""
    forecast_time_range = parse_forecast_days_range(forecast[0])
    chosen_unit = set_forecast_unit(forecast[1])
    city_weather_info = chosen_unit[0].lookup_by_location(city)
    print_weather(city, city_weather_info, chosen_unit[1], forecast_time_range)


if __name__ == '__main__':
    get_weather()
