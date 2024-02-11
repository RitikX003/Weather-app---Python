from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather_data(city)
        return render_template('weather.html', city=city, weather_data=weather_data)

def get_weather_data(city):
    api_key = '8ab0c99327e85a3a42ce55eab49633cf'
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        weather_data = response.json()

        if 'weather' not in weather_data:
            return {'error': 'City not found'}

        main_weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']

        return {'main_weather': main_weather, 'description': description, 'temperature': temperature}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {'error': 'Error fetching weather data'}

@app.route('/autocomplete/<prefix>', methods=['GET'])
def autocomplete(prefix):
    api_key = '8ab0c99327e85a3a42ce55eab49633cf'
    api_url = f'http://api.openweathermap.org/data/2.5/find?q={prefix}&type=like&mode=json&appid={api_key}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        cities_data = response.json().get('list', [])
        suggestions = [city['name'] for city in cities_data]

        return jsonify({'suggestions': suggestions})

    except requests.exceptions.RequestException as e:
        print(f"Error fetching autocomplete data: {e}")
        return jsonify({'suggestions': []})

if __name__ == '__main__':
    app.run(debug=True)
