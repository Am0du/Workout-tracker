import os
import requests
import datetime as dt
from tkinter import *
from tkinter import messagebox


API_ID = ''     # id from Nutritionix api
API_key = ''    # key from Nutrionix api remember to add .encode('ascii', 'ignore') to the key
name = ''
gender = ''     # Gender
weight = 0      # weight in Kg
height = 0      # height in cm
age = 0         # age

date = dt.datetime.now()
date_now = date.strftime('%d/%m/%G')
time = date.strftime('%H:%M:%S')
exercise = ''


def submit():
    global exercise, age, weight, height, name, gender
    exercise = entry.get()
    age = int(age_entry.get())
    weight = float(weight_entry.get())
    height = float(height_entry.get())
    gender = gender_entry.get()
    name = name_entry.get()
    window.destroy()


window = Tk()
window.title('Workout Logger')
window.config(pady=50, padx=50)

name_label = Label(text='NAME:')
name_label.grid(column=0, row=0, sticky='w')
name_entry = Entry()
name_entry.grid(column=1, row=0, pady=10,)

gender_label = Label(text='GENDER:')
gender_label.grid(column=0, row=1, sticky='w')
gender_entry = Entry()
gender_entry.grid(column=1, row=1, pady=10,)

weight_label = Label(text='WEIGHT(kg):')
weight_label.grid(column=0, row=2, sticky='w')
weight_entry = Entry()
weight_entry.grid(column=1, row=2, pady=10,)

height_label = Label(text='HEIGHT(cm):')
height_label.grid(column=0, row=3, sticky='w')
height_entry = Entry()
height_entry.grid(column=1, row=3, pady=10,)

age_label = Label(text='AGE:')
age_label.grid(column=0, row=4, sticky='w')
age_entry = Entry()
age_entry.grid(column=1, row=4, pady=10,)


label = Label(text='Tell me which exercise you carry out today:')
label.grid(column=0, row=5,)
entry = Entry(width=50)
entry.grid(column=0, row=6, columnspan=2, pady=10,)

button = Button(text='Submit', command=submit)
button.grid(column=0, row=7, columnspan=2, pady=10)
window.mainloop()

header = {
    'x-app-id': API_ID,
    'x-app-key': API_key,
}

body = {
    'query':  exercise,
    'gender': gender,
    'weight_kg': weight,
    'height_cm': height,
    'age': age,
}

nutri_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
response1 = requests.post(url=nutri_endpoint, json=body, headers=header)
data = response1.json()

exercise = data['exercises'][0]['name'].title()
duration = data['exercises'][0]['duration_min']
calories = data['exercises'][0]['nf_calories']

sheety_endpoint = '' #Endpoint from sheety

# This should correspond with your google sheet field
body = {
    'sheet1': {
        'name': name,
        'date': date_now,
        'time': time,
        'exercise': exercise,
        'duration': duration,
        'calories': calories,
    }

}

is_ok = messagebox.askokcancel(title='Do you want to log this:',
                               message=f'Date: {date_now}\nTime: {time}\nExercise: {exercise}'
                                       f'\nDuration: {duration}\nCalories: {calories}',
                               icon='question')

if is_ok:
    response = requests.post(url=sheety_endpoint, json=body)
