# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 15:20:11 2016

@author: ODA
"""

import math
import sqlite3

# Initialize the EV model databese
conn = sqlite3.connect('ev.sqlite3')
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS Model
    (name TEXT, C_efficiency REAL, F_efficiency REAL)''')

# add_new_model : Add a new model to the model table (used for test)
def add_new_model(name, C, F):
    cur.execute('INSERT INTO Model (name, C_efficiency, F_efficiency) VALUES (?, ?, ?)',
                (name, C, F))
    conn.commit()

# display_all_models : display all models in the model table (used for test)
def display_all_models():
    cur.execute('SELECT * FROM Model')
    for row in cur:
        print(row)


""" Get 24-hour load profile for EV charging

    Parameters
    ----------
    distance : float
        Daily driving distance in km
    ev_name : string
        Name of EV
    charger_type : int
        Type of charger
        -level 1 : 0
        -level 2 (25amp): 1
        -level 2 (40amp): 2
        -level 2 (50amp): 3

    Returns
    ----------
    load_profile : list
        24-hour load profile when charging is requested
"""
charging_load_data = [1.39982502187227, 4.7976011994003, 7.19729043183743, 9.6045197740113]
resolution = 2  # The number of hourly devision for load profile

def get_ev_load_profile(distance, ev_name, charger_type):
    cur.execute('SELECT C_efficiency, F_efficiency FROM Model WHERE name = ? LIMIT 1', (ev_name, ))
    charging_efficiency, fuel_efficiency = cur.fetchone()
    charging_load = charging_load_data[charger_type]
    energy_consumption = fuel_efficiency * distance
    charging_time = energy_consumption * resolution / (charging_load * charging_efficiency)
    charging_time = int(math.ceil(charging_time))   #round up the time

    if charging_time < 24*resolution:
        load_profile = [charging_load]*charging_time + [0]*(24*resolution-charging_time)
    else:
        load_profile = [charging_load]*24*resolution
        
    return load_profile
    
    