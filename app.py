from flask import Flask, render_template, request, url_for, redirect
import requests
import json
import python_weather

# average pace, weekly miles ran, sprint times
# most frequented running routes
# local weather information to the user based on a zip code
# breakdown of activity types

zip_code = None
mile_goal = None

app = Flask(__name__)

# 61154779 ashank athlete id


@app.route('/', methods=['GET', 'POST'])
async def home():
    global zip_code
    global mile_goal

    if request.method == 'POST':
        zip = str(request.form['zip'])
        zip_code = zip
        client = python_weather.Client(format=python_weather.IMPERIAL)

        # fetch a weather forecast from a city
        weather = await client.find(zip)

        forecasts = []
        for f in weather.forecasts[2:]:
            dic = {}
            dic['date'] = f.date.strftime("%B %d, %Y")
            dic['sky_text'] = f.sky_text
            dic['temperature'] = f.temperature

            forecasts.append(dic)

        await client.close()

        if mile_goal is not None:
            return render_template('general.html', need_input=False, current_temp=weather.current.temperature, forecasts=forecasts, need_miles=False, miles=mile_goal)
        else:
            return render_template('general.html', need_input=False, current_temp=weather.current.temperature, forecasts=forecasts, need_miles=True)
    else:
        zip_code = None
        if mile_goal is not None:
            return render_template('general.html', need_input=True, need_miles=False, miles=mile_goal)
        else:
            return render_template('general.html', need_input=True, need_miles=True)


@app.route('/goal', methods=['GET', 'POST'])
async def goal():
    global zip_code
    global mile_goal

    if request.method == 'POST':
        miles = str(request.form['miles'])
        mile_goal = miles

        if zip_code is not None:
            client = python_weather.Client(format=python_weather.IMPERIAL)

            # fetch a weather forecast from a city
            weather = await client.find(zip_code)

            forecasts = []
            for f in weather.forecasts[2:]:
                dic = {}
                dic['date'] = f.date.strftime("%B %d, %Y")
                dic['sky_text'] = f.sky_text
                dic['temperature'] = f.temperature

                forecasts.append(dic)

            await client.close()

            return render_template('general.html', need_input=False, current_temp=weather.current.temperature, forecasts=forecasts, miles=miles, need_miles=False)
        else:
            return render_template('general.html', need_input=True, miles=miles, need_miles=False)
    else:
        mile_goal = None
        if zip_code is not None:
            client = python_weather.Client(format=python_weather.IMPERIAL)

            # fetch a weather forecast from a city
            weather = await client.find(zip_code)

            forecasts = []
            for f in weather.forecasts[2:]:
                dic = {}
                dic['date'] = f.date.strftime("%B %d, %Y")
                dic['sky_text'] = f.sky_text
                dic['temperature'] = f.temperature

                forecasts.append(dic)

            await client.close()

            return render_template('general.html', need_input=False, current_temp=weather.current.temperature, forecasts=forecasts, need_miles=True)
        else:
            return render_template('general.html', need_input=True, need_miles=True)


if __name__ == '__main__':
    app.run(debug=True, port='8888')
