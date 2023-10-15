import secrets
import string
from flask import Flask, render_template, request, jsonify
import requests
import plotly
import plotly.graph_objs as go
import plotly.offline
from datetime import datetime


app = Flask(__name__)

# Generate a random string of characters for the secret key
def generate_secret_key(length=24):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

# Use the generated key as your secret_key
app.secret_key = generate_secret_key()

# Replace with your WeatherAPI API key
API_BASE_URL = "http://api.weatherapi.com/v1"  # Your base API URL
API_KEY = "e0da29cbdf884babbb9123743231510"  # Your API key

# Initialize Flask-Bootstrap
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

def custom_date(value, format='%B %d, %Y, %H:%M %p'):
    return value.strftime(format)

app.jinja_env.filters['custom_date'] = custom_date


@app.route('/')
def index():
    return render_template('home.html')

def fetch_weather_data(location):
    try:
        url = f"{API_BASE_URL}/current.json?key={API_KEY}&q={location}&alerts=yes"
        response = requests.get(url)
        data = response.json()

        return data

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

@app.route('/weatheralert', methods=['GET', 'POST'])
def weatheralert():
    location = ""
    weather_data = None

    if request.method == 'POST':
        location = request.form.get('location')
        if location:
            weather_data = fetch_weather_data(location)

    return render_template('Weatheralert.html', location=location, weather_data=weather_data)

# Function to calculate carbon footprint
# Function to calculate carbon footprint
def calculate_carbon_footprint(distance, transportation_type):
    url = "https://carbonfootprint1.p.rapidapi.com/"
    querystring = {"distance": distance, "type": transportation_type}
    headers = {
        "X-RapidAPI-Key": "4fe4b14bdbmshe8068f54bb0cc81p1fece2jsn256608c15e0d",
        "X-RapidAPI-Host": "carbonfootprint1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    result = response.json()

    return result


@app.route('/carbonfootprint', methods=['GET', 'POST'])
def carbonfootprint():
    result = None

    if request.method == 'POST':
        distance = request.form.get('distance')
        transportation_type = request.form.get('transportation_type')

        if distance and transportation_type:
            result = calculate_carbon_footprint(distance, transportation_type)

    return render_template('carbonfootprint.html', result=result)

@app.route('/calculate', methods=["GET", "POST"])
def calculate():
    bmi_result = {}  # Default values for BMI
    absi_result = {}  # Default values for ABSI
    ibw_result = {}   # Default values for IBW

    if request.method == "POST":
        # Get form data
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        waist = float(request.form.get('waist'))
        gender = request.form.get('gender')
        age = int(request.form.get('age'))

        # BMI calculation
        bmi_url = "https://mega-fitness-calculator1.p.rapidapi.com/bmi"
        bmi_querystring = {
            "weight": weight,
            "height": height
        }

        # ABSI calculation
        absi_url = "https://mega-fitness-calculator1.p.rapidapi.com/absi"
        absi_querystring = {
            "weight": weight,
            "height": height,
            "waist": waist,
            "age": age,
            "gender": gender
        }

        # IBW calculation
        ibw_url = "https://mega-fitness-calculator1.p.rapidapi.com/ibw"
        ibw_querystring = {
            "weight": weight,
            "height": height,
            "gender": gender
        }

        headers = {
            "X-RapidAPI-Key": "4fe4b14bdbmshe8068f54bb0cc81p1fece2jsn256608c15e0d",
            "X-RapidAPI-Host": "mega-fitness-calculator1.p.rapidapi.com"
        }

        bmi_response = requests.get(bmi_url, headers=headers, params=bmi_querystring)
        absi_response = requests.get(absi_url, headers=headers, params=absi_querystring)
        ibw_response = requests.get(ibw_url, headers=headers, params=ibw_querystring)

        # Debugging: Print the responses from the API
        print("BMI API response:", bmi_response.text)
        print("ABSI API response:", absi_response.text)
        print("IBW API response:", ibw_response.text)

        bmi_result = bmi_response.json()
        absi_result = absi_response.json()
        ibw_result = ibw_response.json()

    return render_template('bmi.html', bmi_result=bmi_result, absi_result=absi_result, ibw_result=ibw_result)

@app.route('/currency_converter', methods=['GET', 'POST'])
def currency_converter():
    conversion_result = None
    currency_chart = None

    if request.method == 'POST':
        from_currency = request.form.get('from_currency')
        to_currency = request.form.get('to_currency')
        amount = float(request.form.get('amount'))

        # Fetch the latest exchange rate using the RapidAPI service
        url = "https://currency-exchange.p.rapidapi.com/exchange"
        querystring = {"from": from_currency, "to": to_currency, "q": str(amount)}
        headers = {
            "X-RapidAPI-Key": "4fe4b14bdbmshe8068f54bb0cc81p1fece2jsn256608c15e0d",
            "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        conversion_rate = response.json()

        # Create a Plotly line chart for currency comparison
        currency_chart = create_currency_chart(from_currency, to_currency)

        conversion_result = f"{amount} {from_currency} = {conversion_rate:.2f} {to_currency}"

    return render_template('currencyconversion.html', conversion_result=conversion_result, currency_chart=currency_chart)

def create_currency_chart(from_currency, to_currency):
    # This is a dummy chart, you can modify it as needed
    trace = go.Scatter(x=[from_currency, to_currency], y=[1, 0.75], mode='lines+markers')

    chart = plotly.offline.plot([trace], output_type="div")

    return chart




if __name__ == '__main__':
    app.run(debug=True)
