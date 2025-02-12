from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# OpenWeatherMap API key
API_KEY = 'f52a14a5fc91216bc0d2ced63a928bf1'

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    # Debugging: Print full API response
    print("API Response:", data)

    if response.status_code != 200 or "main" not in data:
        print(f"Error: {data.get('message', 'Unknown error')}")
        return None

    weather = {
        "city": data.get("name", "Unknown"),
        "temperature": data["main"].get("temp", "N/A"),
        "description": data["weather"][0].get("description", "N/A") if "weather" in data else "N/A",
        "icon": data["weather"][0].get("icon", "") if "weather" in data else "",
        "humidity": data["main"].get("humidity", "N/A"),
        "wind_speed": data["wind"].get("speed", "N/A") if "wind" in data else "N/A"
    }
    return weather

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error_message = None

    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if not city:
            error_message = "Please enter a city name."
        else:
            weather = get_weather(city)
            if weather is None:
                error_message = "Could not fetch weather data. Please check the city name or try again later."

    return render_template('index.html', weather=weather, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
