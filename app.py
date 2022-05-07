from flask import Flask, render_template
import requests
import json
import python_weather

# average pace, weekly miles ran, sprint times
# most frequented running routes
# local weather information to the user based on a zip code
# breakdown of activity types 

app = Flask(__name__)

# 61154779 ashank athlete id

@app.route('/')
async def home():
    # with open('api.json', 'a') as f:
    #     f.write(json.dumps(r))
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client(format=python_weather.IMPERIAL)

    # fetch a weather forecast from a city
    weather = await client.find("61820")

    # returns the current day's forecast temperature (int)
    print(weather.current.temperature)

    # get the weather forecast for a few days
    for forecast in weather.forecasts:
        print(str(forecast.date), forecast.sky_text, forecast.temperature)

    # close the wrapper once done
    await client.close()

    return render_template('layout.html')


if __name__ == '__main__':
    app.run(debug=True, port='8888')