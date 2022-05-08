from flask import Flask, render_template, request, url_for, redirect
import requests
import json
import python_weather
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime, timedelta

matplotlib.use('Agg')
plt.gcf().subplots_adjust(bottom=0.2)

# average pace, weekly miles ran, sprint times
# most frequented running routes
# local weather information to the user based on a zip code
# breakdown of activity types

zip_code = None
mile_goal = None
total_distance = 0

app = Flask(__name__)

# 61154779 ashank athlete id


@app.route('/', methods=['GET', 'POST'])
async def home():
    global zip_code
    global mile_goal
    global total_distance

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
            return render_template('general.html', need_input=False, current_temp=weather.current.temperature, forecasts=forecasts, need_miles=False, miles=mile_goal,  met_goal=total_distance >= float(mile_goal), total_distance=total_distance)
        else:
            return render_template('general.html', need_input=False, current_temp=weather.current.temperature, forecasts=forecasts, need_miles=True)
    else:
        zip_code = None
        if mile_goal is not None:
            return render_template('general.html', need_input=True, need_miles=False, miles=mile_goal,  met_goal=total_distance >= float(mile_goal), total_distance=total_distance)
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

            return render_template('general.html', need_input=False, current_temp=weather.current.temperature, forecasts=forecasts, miles=miles, need_miles=False, met_goal=total_distance >= float(miles), total_distance=total_distance)
        else:
            return render_template('general.html', need_input=True, miles=miles, need_miles=False,  met_goal=total_distance >= float(miles), total_distance=total_distance)
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

def get_df():
    col_names = ['id','type']
    activities = pd.DataFrame(columns=col_names)
    page = 1

    after = get_seven_days_date()
    global total_distance
    total_distance = 0
    while True:
        url = 'https://www.strava.com/api/v3/athlete/activities'
        headers = {'Authorization': 'Bearer be3a2cd478c838388bc13ea45cfa92e1e16b4f52'}
        params = {'page': page, 'after': after}

        r = requests.get(url, headers=headers, params=params)
        r = r.json()

        if (not r):
            break

        for x in range(len(r)):
            activities.loc[x + (page-1)*30,'id'] = r[x]['id']
            activities.loc[x + (page-1)*30,'type'] = r[x]['type']
            total_distance += r[x]['distance']
        page += 1
    total_distance /= 1609
    return activities

def activity_graph():
    df = get_df()
    x = df['type'].value_counts().plot(kind='bar', color=['blue', 'red', 'orange', 'green', 'purple', 'yellow'])

    plt.savefig('static/plot.png')


def get_seven_days_date():
    date = datetime.today() - timedelta(days=7)

    return date.timestamp()



if __name__ == '__main__':
    print(get_seven_days_date())
    activity_graph()
    app.run(debug=True, port='8888')
