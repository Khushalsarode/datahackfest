import requests

API_BASE_URL = "http://api.weatherapi.com/v1"
API_KEY = "e0da29cbdf884babbb9123743231510"

def fetch_weather_data(location):
    try:
        url = f"{API_BASE_URL}/current.json?key={API_KEY}&q={location}&alerts=yes"
        response = requests.get(url)
        data = response.json()

        return data

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

if __name__ == "__main__":
    location = "New York"  # You can change the location to any city or area you want
    weather_data = fetch_weather_data(location)

    if weather_data:
        print("Weather Data:")
        print(f"Location: {weather_data['location']['name']}, {weather_data['location']['region']}, {weather_data['location']['country']}")
        print(f"Local Time: {weather_data['location']['localtime']}")
        print(f"Temperature: {weather_data['current']['temp_c']}°C ({weather_data['current']['temp_f']}°F)")
        print(f"Condition: {weather_data['current']['condition']['text']}")
        print(f"Wind: {weather_data['current']['wind_mph']} mph ({weather_data['current']['wind_kph']} kph), {weather_data['current']['wind_dir']}")
        print(f"Pressure: {weather_data['current']['pressure_mb']} mb ({weather_data['current']['pressure_in']} in)")
        print(f"Humidity: {weather_data['current']['humidity']}%")
        print(f"UV Index: {weather_data['current']['uv']}")
        print(f"Cloud Cover: {weather_data['current']['cloud']}%")
        print(f"Feels Like: {weather_data['current']['feelslike_c']}°C ({weather_data['current']['feelslike_f']}°F)")
        print(f"Visibility: {weather_data['current']['vis_km']} km ({weather_data['current']['vis_miles']} miles)")
        print(f"Gust Speed: {weather_data['current']['gust_mph']} mph ({weather_data['current']['gust_kph']} kph)")

        if 'alerts' in weather_data:
            alerts = weather_data['alerts']['alert']
            if alerts:
                print("Weather Alerts:")
                for alert in alerts:
                    print(f"Headline: {alert['headline']}")
                    print(f"Type: {alert['msgtype']}")
                    print(f"Severity: {alert['severity']}")
                    print(f"Urgency: {alert['urgency']}")
                    print(f"Areas: {alert['areas']}")
                    print(f"Category: {alert['category']}")
                    print(f"Certainty: {alert['certainty']}")
                    print(f"Event: {alert['event']}")
                    print(f"Effective Date: {alert['effective']}")
                    print(f"Expires: {alert['expires']}")
                    print(f"Description: {alert['desc']}")
                    print(f"Instruction: {alert['instruction']}")
                    print("\n")
            else:
                print("No weather alerts for this location.")
        else:
            print("No weather alerts for this location.")
    else:
        print("Weather data not available.")
