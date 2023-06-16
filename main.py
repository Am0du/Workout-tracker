import os
import requests
import datetime as dt


date = dt.datetime.now()
date_now = date.strftime('%d/%m/%G')
time = date.strftime('%H:%M:%S')

API_ID = os.environ.get('Nutri_id')
API_key = os.environ.get('Nutri_key').encode('ascii', 'ignore')
GENDER = 'male'
WEIGHT = 70.0
HEIGHT = 175.0
AGE = 23

header = {
    'x-app-id': API_ID,
    'x-app-key': API_key,
}

exercise = input('tell me which exercises you did: ')

body = {
    'query':  exercise,
    'gender': GENDER,
    'weight_kg': WEIGHT,
    'height_cm': HEIGHT,
    'age': AGE,
}

nutri_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
response1 = requests.post(url=nutri_endpoint, json=body, headers=header)
data = response1.json()

exercise = data['exercises'][0]['name'].title()
duration = data['exercises'][0]['duration_min']
calories = data['exercises'][0]['nf_calories']

sheety_endpoint = 'https://api.sheety.co/83daaf75f16afaf1f4f9dafd89828b12/workoutTracking/sheet1'

body = {
    'sheet1': {
        'date': date_now,
        'time': time,
        'exercise': exercise,
        'duration': duration,
        'calories': calories,
    }

}

response = requests.post(url=sheety_endpoint, json=body)
print(response.text)
