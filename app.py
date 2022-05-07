from flask import Flask, render_template, request, url_for, redirect
import requests
import json
import python_weather

# average pace, weekly miles ran, sprint times
# most frequented running routes
# local weather information to the user based on a zip code
# breakdown of activity types

app = Flask(__name__)

# 61154779 ashank athlete id


@app.route('/', methods=['GET', 'POST'])
async def home():
    # zip_code_given = False
    # with open('api.json', 'a') as f:
    #     f.write(json.dumps(r))
    # declare the client. format defaults to metric system (celcius, km/h, etc.)

    if request.method == 'POST':
        zip = request.form['zip']
        client = python_weather.Client(format=python_weather.IMPERIAL)

        # fetch a weather forecast from a city
        weather = await client.find(str(zip))

        forecasts = []
        for f in weather.forecasts[2:]:
            dic = {}
            dic['date'] = f.date.strftime("%B %d, %Y")
            dic['sky_text'] = f.sky_text
            dic['temperature'] = f.temperature

            forecasts.append(dic)

        await client.close()

        return render_template('general.html', need_input=False, current_temp=weather.current.temperature, forecasts=forecasts)
    else:
        return render_template('general.html', need_input=True)


if __name__ == '__main__':
    app.run(debug=True, port='8888')
