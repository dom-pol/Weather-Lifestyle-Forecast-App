import requests 

import csv 

import string 

import traceback 

import geopy 

from geopy.geocoders import Nominatim 

import openmeteo_requests 

import requests_cache 

from retry_requests import retry 

import os 

import math, threading, tkinter as tk 

import customtkinter as ctk 

from tkinter import * 

from PIL import Image, ImageTk 

import matplotlib 

matplotlib.use("TkAgg") 

import matplotlib.pyplot as plt 

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

import pandas as pd 

import numpy as np 

import Main_forecast as mp 

from activity_profiles import activity_profiles, activity_aliases 



def inp_cleanser(statement): #cleanses input 

    text = statement 

    str(text) 

    text  = text.lower() 

    text = text.replace(" ","") 

    for p in string.punctuation: #removes punctuation in the string 

        text = text.replace(p, "") 

    return text 

 

def get_location_coordinates1(location): 

    API_key = '5a72fc0031f6d0feac1e346a412a976d' #OpenWeatherMap API key 

    location = inp_cleanser(location) 

    url = f'https://api.openweathermap.org/data/2.5/weather?q=snowdonia,uk&APPID=5a72fc0031f6d0feac1e346a412a976d' 

    r = requests.get(url) #sends a get request to the server 

    if r.status_code == 200: #if the response is successful from server 

        data = r.json() #converts the response to json format 

        lat = data['coord']['lat'] #extracts latitude and longitude from the json data 

        lon = data['coord']['lon'] 

        print(f"Coordinates of {location} are: Latitude: {lat}, Longitude: {lon}") 

    else: 

        print("Error in the HTTP request") 

 

def get_location_coordinates(location): 

    location = inp_cleanser(location) 

    loc = Nominatim(user_agent="GetLoc") 

    getLoc = loc.geocode(location) #gets the location 

    print(f"Coordinates of {location} are: Latitude: {getLoc.latitude}, Longitude: {getLoc.longitude}") 

    return getLoc.latitude, getLoc.longitude 

 

def openweather_call_weather(lat, lon): 

    API_key = '5a72fc0031f6d0feac1e346a412a976d' #OpenWeatherMap API key 

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&APPID={API_key}&units=metric' 

    print(url) 

    r = requests.get(url) #sends a get request to the server 

    if r.status_code == 200: #if the response is successful from server 

        data = r.json() #converts the response to json format 

        weather_desc = data['weather'][0]['description'] #extracts weather description 

        temp = data['main']['temp'] #extracts temperature 

        humidity = data['main']['humidity'] #extracts humidity 

        wind_speed = data['wind']['speed'] #extracts wind speed 

        print(f"Weather Description: {weather_desc}") 

        print(f"Temperature (Celsius): {temp}") 

        print(f"Humidity (%): {humidity}") 

        print(f"Wind Speed (m/s): {wind_speed}") 

    else: 

        print("Error in the HTTP request") 

 

 

def openmeteo_call_weather(lat, lon): 

    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600) #1 hour cache expiration 

    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2) #retry session with 5 retries and exponential backoff 

    openmeteo = openmeteo_requests.Client(session = retry_session) #initialize openmeteo client with retry session 

    url = "https://api.open-meteo.com/v1/forecast" #target URL for openmeteo API 

    params = {  #parameters for the API request 

        "latitude": lat, 

        "longitude": lon, 

        "daily": ["temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_sum", "precipitation_hours", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant"], 

        "hourly": ["temperature_2m", "cloud_cover_low", "cloud_cover", "cloud_cover_mid", "cloud_cover_high", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation", "rain", "showers", "snowfall", "hail", "pressure_msl", "surface_pressure", "visibility", "cloud_cover_2m", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"], 

        "models": "ukmo_seamless", 

        "timezone": "auto", 

    } 

    responses = openmeteo.weather_api(url, params=params) #make request to openmeteo API 

    response = responses[0] #get the first response from the list 

    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E") #coordinates 

    print(f"Elevation: {response.Elevation()} m asl") #elevation above sea level 

    Elevation = response.Elevation() 

    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s") #timezone offset in seconds 

     

    #format for weather dictionary {latitude, longitude, time, temperature_2m, etc.} 

    Weather_dict = {} 

    hourly_data = response.Hourly() #get hourly_data data 

 

    hourly_temperature_2m = hourly_data.Variables(0).ValuesAsNumpy() 

    hourly_cloud_cover_low = hourly_data.Variables(1).ValuesAsNumpy() 

    hourly_cloud_cover = hourly_data.Variables(2).ValuesAsNumpy() 

    hourly_cloud_cover_mid = hourly_data.Variables(3).ValuesAsNumpy() 

    hourly_cloud_cover_high = hourly_data.Variables(4).ValuesAsNumpy() 

    hourly_relative_humidity_2m = hourly_data.Variables(5).ValuesAsNumpy() 

    hourly_dew_point_2m = hourly_data.Variables(6).ValuesAsNumpy() 

    hourly_apparent_temperature = hourly_data.Variables(7).ValuesAsNumpy() 

    hourly_precipitation = hourly_data.Variables(8).ValuesAsNumpy() 

    hourly_rain = hourly_data.Variables(9).ValuesAsNumpy() 

    hourly_showers = hourly_data.Variables(10).ValuesAsNumpy() 

    hourly_snowfall = hourly_data.Variables(11).ValuesAsNumpy() 

    hourly_hail = hourly_data.Variables(12).ValuesAsNumpy() 

    hourly_pressure_msl = hourly_data.Variables(13).ValuesAsNumpy() 

    hourly_surface_pressure = hourly_data.Variables(14).ValuesAsNumpy() 

    hourly_visibility = hourly_data.Variables(15).ValuesAsNumpy() 

    hourly_cloud_cover_2m = hourly_data.Variables(16).ValuesAsNumpy() 

    hourly_wind_speed_10m = hourly_data.Variables(17).ValuesAsNumpy() 

    hourly_wind_direction_10m = hourly_data.Variables(18).ValuesAsNumpy() 

    hourly_wind_gusts_10m = hourly_data.Variables(19).ValuesAsNumpy() 

 

    hourly_data = {"date": pd.date_range(  

        start = pd.to_datetime(hourly_data.Time(), unit = "s", utc = True),  

        end = pd.to_datetime(hourly_data.TimeEnd(), unit = "s", utc = True),  

        freq = pd.Timedelta(seconds = hourly_data.Interval()), 

        inclusive = "left" 

    )} 

 

    hourly_data["temperature_2m"] = hourly_temperature_2m 

    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low 

    hourly_data["cloud_cover"] = hourly_cloud_cover 

    hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid 

    hourly_data["cloud_cover_high"] = hourly_cloud_cover_high 

    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m 

    hourly_data["dew_point_2m"] = hourly_dew_point_2m 

    hourly_data["apparent_temperature"] = hourly_apparent_temperature 

    hourly_data["precipitation"] = hourly_precipitation 

    hourly_data["rain"] = hourly_rain 

    hourly_data["showers"] = hourly_showers 

    hourly_data["snowfall"] = hourly_snowfall 

    hourly_data["hail"] = hourly_hail 

    hourly_data["pressure_msl"] = hourly_pressure_msl 

    hourly_data["surface_pressure"] = hourly_surface_pressure 

    hourly_data["visibility"] = hourly_visibility 

    hourly_data["cloud_cover_2m"] = hourly_cloud_cover_2m 

    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m 

    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m 

    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m 

 

    daily_data = response.Daily() #get daily data 

 

    daily_temperature_2m_max = daily_data.Variables(0).ValuesAsNumpy() 

    daily_temperature_2m_min = daily_data.Variables(1).ValuesAsNumpy() 

    daily_apparent_temperature_max = daily_data.Variables(2).ValuesAsNumpy() 

    daily_apparent_temperature_min = daily_data.Variables(3).ValuesAsNumpy() 

    daily_sunrise = daily_data.Variables(4).ValuesAsNumpy() 

    daily_sunset = daily_data.Variables(5).ValuesAsNumpy() 

    daily_rain_sum = daily_data.Variables(6).ValuesAsNumpy() 

    daily_showers_sum = daily_data.Variables(7).ValuesAsNumpy() 

    daily_snowfall_sum = daily_data.Variables(8).ValuesAsNumpy() 

    daily_precipitation_sum = daily_data.Variables(9).ValuesAsNumpy() 

    daily_precipitation_hours = daily_data.Variables(10).ValuesAsNumpy() 

    daily_precipitation_probability_max = daily_data.Variables(11).ValuesAsNumpy() 

    daily_wind_speed_10m_max = daily_data.Variables(12).ValuesAsNumpy() 

    daily_wind_gusts_10m_max = daily_data.Variables(13).ValuesAsNumpy() 

    daily_wind_direction_10m_dominant = daily_data.Variables(14).ValuesAsNumpy() 

 

    daily_data = {"date": pd.date_range(  

        start = pd.to_datetime(daily_data.Time(), unit = "s", utc = True), 

        end = pd.to_datetime(daily_data.TimeEnd(), unit = "s", utc = True), 

        freq = pd.Timedelta(seconds = daily_data.Interval()), 

        inclusive = "left" 

    )} 

 

    daily_data["temperature_2m_max"] = daily_temperature_2m_max #adds the temperature_2m_max data to the daily_data dictionary 

    daily_data["temperature_2m_min"] = daily_temperature_2m_min 

    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max 

    daily_data["apparent_temperature_min"] = daily_apparent_temperature_min 

    daily_data["sunrise"] = daily_sunrise 

    daily_data["sunset"] = daily_sunset 

    daily_data["rain_sum"] = daily_rain_sum 

    daily_data["showers_sum"] = daily_showers_sum 

    daily_data["snowfall_sum"] = daily_snowfall_sum 

    daily_data["precipitation_sum"] = daily_precipitation_sum 

    daily_data["precipitation_hours"] = daily_precipitation_hours 

    daily_data["precipitation_probability_max"] = daily_precipitation_probability_max 

    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max 

    daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max 

    daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant 

 

    hourly_dataframe = pd.DataFrame(data = hourly_data) 

    hourly_dataframe.to_feather('hourly_weather_data.feather') #saves the dataframe to a feather file #reads the dataframe from the feather file 

    hourly_dataframe_feather = pd.read_feather('hourly_weather_data.feather') #reads the dataframe from the feather file 

    hourly_dataframe_feather.to_clipboard() #copies the dataframe to clipboard 

 

    daily_dataframe = pd.DataFrame(data = daily_data) 

    daily_dataframe.to_feather('daily_weather_data.feather') #saves the dataframe to a feather file 

    daily_dataframe_feather = pd.read_feather('daily_weather_data.feather') #reads the dataframe from the feather file 

    #daily_dataframe_feather.to_clipboard() #copies the dataframe to clipboard 

    print(daily_precipitation_probability_max) 

 

    return hourly_dataframe, daily_dataframe, Elevation 

 

def another_source(): 

    pass 

 

# Graphical representations of data 

fig = plt.figure() 

 

def get_datas(): 

    hourly_dataframe_feather = pd.read_feather('hourly_weather_data.feather') #reads the dataframe from the feather file 

    daily_dataframe_feather = pd.read_feather('daily_weather_data.feather') 

    hourly_data_record = hourly_dataframe_feather.to_numpy() 

    print("hourly_data_record:", hourly_data_record)  

    daily_data_record = daily_dataframe_feather.to_numpy() 

    return hourly_dataframe_feather, daily_dataframe_feather, hourly_data_record, daily_data_record 

 

def bar_charts(hourly_dataframe_feather, daily_dataframe_feather): 

    get_datas() 

    hourly_temperature_arr = hourly_dataframe_feather['temperature_2m'].to_numpy() 

    daily_temperature_max = daily_dataframe_feather['temperature_2m_max'].to_numpy() 

    print("daily_temperature_max:", daily_temperature_max) 

    daily_temperature_min = daily_dataframe_feather['temperature_2m_min'].to_numpy() 

    daily_hours = hourly_dataframe_feather['date'].to_numpy() 

    daily_days = daily_dataframe_feather['date'].to_numpy() 

     

    bar_1 = fig.add_subplot(2,2,1, facecolor="white") 

    bar_1.bar(daily_hours, hourly_temperature_arr, color="teal", width=0.03) 

    bar_1.set_xlabel("Date") 

    bar_1.set_ylabel("Temperature (°C)") 

    bar_1.set_title("Hourly Temperature") 

 

    bar_2 = fig.add_subplot(2,2,2, facecolor="white") 

    x = np.arange(len(daily_days)) 

    bar_2_width = 0.35 

    bar_2.bar(x - bar_2_width/2, daily_temperature_max, color="darkgreen", width=bar_2_width, label="Max Temp") 

    bar_2.bar(x + bar_2_width/2, daily_temperature_min, color="lightgreen", width=bar_2_width, label="Min Temp") 

    bar_2.set_xlabel("Date") 

    bar_2.set_ylabel("Temperature (°C)") 

    bar_2.set_title("Daily Temperature Max/Min") 

    bar_2.legend(title="Temperature") 

 

    plt.show() 

    pass 

 

    daily_precipitation_probability_arr = daily_dataframe_feather['precipitation_probability_max'].to_numpy() 

    bar_3 = fig.add_subplot(2,1,2, facecolor="white") 

    bar_3.bar(daily_hours, daily_precipitation_probability_arr, color="green", width=0.35) 

    bar_3.set_xlabel("Date") 

    bar_3.set_ylabel("Precipitation Probability (%)") 

    bar_3.set_title("Weekly Precipitation Probability") 

 

 

def user_interface(): 

    pass 

 

def lifestyle_forecast(daily_dataframe, hourly_dataframe, user_activity, elevation, is_daily=False): 

    """    choice = input("Hourly or daily forecast? ").strip().lower() 

 

    user_terrain = { 

        "terrain_type": input("Enter terrain type (mountain, coastal, trail, road): ").strip().lower(), 

        "exposure":     input("Enter exposure level (low, medium, high): ").strip().lower(), 

        "slope":        input("Enter slope (flat, moderate, steep, verysteep): ").strip().lower(), 

        "remoteness":   input("Enter remoteness (urban, rural, wilderness): ").strip().lower(), 

    } """ 

 

    user_terrain = { 

        "terrain_type": "mountain", 

        "exposure": "high", 

        "slope": "steep", 

        "remoteness": "wilderness" 

    } 

    choice = "daily" 

 

    # validate inputs 

    validated_activity = Validate_activity(user_activity) 

    if not validated_activity: 

        return 

    validated_terrain = Validate_terrain(user_terrain) 

    if not validated_terrain: 

        return 

 

    #load daily or hourlydataframes from feather files 

    if choice == "hourly": 

        df = hourly_dataframe 

        is_daily = False 

    elif choice == "daily": 

        df = daily_dataframe 

        is_daily = True 

    else: 

        print("Invalid choice. Please enter 'hourly' or 'daily'.") 

        return 

 

    # Score each row and print a summary 

    for i, row in df.iterrows(): 

        record = row.to_dict() # convert the row to a dictionary for easier handling 

        validated_record = Validate_weather_data(record) 

        if not validated_record: 

            continue 

        rating, score, breakdown = Prepare_data( 

    validated_record, 

    validated_activity, 

    validated_terrain, 

    elevation, 

    is_daily=is_daily 

) #calls the Prepare_data function to get the rating, score, and breakdown for the current record 

        print(f"\n[{record.get('date', i)}] → {rating.upper()}  (score: {score})") #prints the date, rating, and score for the current record 

        for var, info in breakdown.items(): #prints the breakdown of each variable's raw value and rating 

            print(f"  {var:35s} {info['raw']:>7.1f}  →  {info['rating']}") 

 

#input_handler functions down below 

def input_handler(record, user_activity, user_terrain): 

    validated_weather_data = Validate_weather_data(record) 

    validated_activity = Validate_activity(user_activity) 

    validated_terrain = Validate_terrain(user_terrain) 

    #normalized_data = Normalize_data(validated_weather_data) 

 

    return validated_weather_data, validated_activity, validated_terrain 

 

def Validate_weather_data(record): 

    if not record: 

        return False 

 

    record = record.copy() 

    record.pop("date", None) 

 

    for key, value in record.items(): 

        if value is None: 

            return False 

        try: 

            record[key] = float(value) 

        except: 

            return False 

 

    return record  

 

def Validate_activity(user_activity): 

    if inp_cleanser(user_activity) in activity_aliases: 

        return activity_aliases[inp_cleanser(user_activity)] 

    else: 

        print("Error: Invalid activity. Please choose from:", list(activity_aliases.keys())) 

        return False 

         

def Validate_terrain(user_terrain): 

    terrains = ["mountain", "coastal", "trail", "road", "urban", "rural", "wilderness"] 

    exposures = ["low", "medium", "high"] 

    slopes = ["flat", "moderate", "steep", "verysteep"] 

    remoteness = ["urban", "rural", "wilderness"] 

    if user_terrain.get("terrain_type", "Unknown").lower().strip() not in terrains: 

        print("Error: Invalid terrain. Please choose from:", terrains) 

        return False 

    elif user_terrain.get("exposure", "Unknown").lower().strip() not in exposures: 

        print("Error: Invalid exposure. Please choose from:", exposures) 

        return False 

    elif user_terrain.get("slope", "Unknown").lower().strip() not in slopes: 

        print("Error: Invalid slope. Please choose from:", slopes) 

        return False 

    elif user_terrain.get("remoteness", "Unknown").lower().strip() not in remoteness: 

        print("Error: Invalid remoteness. Please choose from:", remoteness) 

        return False 

    return user_terrain 

 

def Risk_scorer(filtered_weather_data, activity_profile): #IMPORTANT: This function is CORE 

    pass 

 

HOURLY_VARIABLE_MAP = { 

    "temperature_2m":        "temperature", 

    "wind_speed_10m":        "wind_speed", 

    "wind_gusts_10m":        "wind_gusts", 

    "precipitation":         "precipitation", 

    "visibility":            "visibility", 

    "relative_humidity_2m":  "humidity", 

    "snowfall":              "snowfall", 

} 

 

DAILY_VARIABLE_MAP = { 

    "temperature_2m_max":            "temperature", 

    "wind_speed_10m_max":            "wind_speed", 

    "wind_gusts_10m_max":            "wind_gusts", 

    "precipitation_sum":             "precipitation", 

    "precipitation_probability_max": "precipitation_probability", 

    "snowfall_sum":                  "snowfall", 

} 

def in_range(value, range_tuple): 

    "True if value falls within (low, high) inclusive." 

    low, high = range_tuple 

    return low <= value <= high 

 

def classify_variable(value, thresholds): 

    def check(ranges, val): 

        if not isinstance(ranges, list): 

            ranges = [ranges] 

        return any(in_range(val, r) for r in ranges) 

 

    if check(thresholds.get("dangerous", []), value): 

        return "dangerous", 2 

    if check(thresholds.get("uncomfortable", []), value): 

        return "uncomfortable", 1 

    if check(thresholds.get("comfortable", []), value): 

        return "comfortable", 0 

    return "unknown", 0   # outside all ranges — treat as comfortable 

 

#returns a dictionary {variable_name: multiplier} and a flat risk adder 

# and weather_data: dictionary of {threshold_key: float} for the current record 

def evaluate_terrain_modifiers(activity_profile, weather_values, user_terrain, elevation): 

    multipliers = {}   # {variable: multiplier} 

    flat_add = 0.0 

 

    for mod_name, mod in activity_profile.get("terrain_modifiers", {}).items(): 

        condition = mod.get("condition", {}) 

        triggered = True # assume modifier is triggered until a condition check fails 

 

        # terrain/exposure/slope/remoteness checks 

        if "exposure" in condition: 

            print(user_terrain) 

            if user_terrain.get("exposure") != condition["exposure"]: 

                triggered = False 

        if "remoteness" in condition: 

            if user_terrain.get("remoteness") != condition["remoteness"]: 

                triggered = False 

        if "slope" in condition: 

            allowed = condition["slope"] 

            if isinstance(allowed, str): 

                allowed = [allowed] 

            if user_terrain.get("slope") not in allowed: 

                triggered = False 

        if "min_elevation" in condition: 

            if elevation < condition["min_elevation"]: 

                triggered = False 

 

    # weather value checks 

        if "max_visibility" in condition: 

            if weather_values.get("visibility", 1000000) > condition["max_visibility"]: 

                triggered = False 

        if "min_precipitation" in condition: 

            if weather_values.get("precipitation", 0) < condition["min_precipitation"]: 

                triggered = False 

        if "max_temperature" in condition: 

            if weather_values.get("temperature", 999) > condition["max_temperature"]: 

                triggered = False 

        if "min_temperature" in condition: 

            if weather_values.get("temperature", -999) < condition["min_temperature"]: 

                triggered = False 

        if "min_humidity" in condition: 

            if weather_values.get("humidity", 0) < condition["min_humidity"]: 

                triggered = False 

        if not triggered: 

            continue 

 

        # apply multipliers 

        for var, mult in mod.get("multipliers", {}).items(): 

            if var == "ALL": 

                # stored separately — applied to total score 

                multipliers["__score__"] = multipliers.get("__score__", 1.0) * mult 

            else: 

                multipliers[var] = multipliers.get(var, 1.0) * mult 

 

        #add flat risk adders 

        flat_add += mod.get("flat_risk_add", 0)  

 

    return multipliers, flat_add 

 

def Get_activity_profile(validated_activity): 

    if validated_activity in activity_profiles: 

        validated_activity = activity_aliases[validated_activity] 

 

    if validated_activity not in activity_profiles: 

        print("Error: Activity profile not found for activity:", validated_activity) 

        raise ValueError("Activity profile not found for activity:", validated_activity) 

    validated_activity = activity_aliases[validated_activity] 

    validated_activity_profile = activity_profiles[validated_activity] 

    return validated_activity, validated_activity_profile 

 

def Calculate_variable_risk(variable_value, variable_thresholds): 

    """Returns numeric risk score 0 (comfortable), 1 (uncomfortable), 2 (dangerous).""" 

    score = classify_variable(variable_value, variable_thresholds) 

    return score 

 

def Risk_evaluator(weather_record, activity_name, user_terrain, elevation, is_daily=False): 

    """ 

    Core risk evaluator: 

    weather_record : dict  — {column_name: value} for one time step 

    activity_name  : str   — canonical activity name e.g. 'hiking' 

    user_terrain   : dict  — {terrain_type, exposure, slope, remoteness} 

    elevation      : float — metres above sea level 

    Returns: 

        overall_rating : str  — 'comfortable', 'uncomfortable', 'dangerous' or 'unknown' 

        score          : float — raw numeric score (higher = worse) 

        breakdown      : dict — per-variable classification 

    """ 

 

    # Validate activity and get profile 

    if activity_name not in activity_profiles: 

        raise ValueError(f"No profile for activity: {activity_name}") 

 

    activity_profile = activity_profiles[activity_name] 

    thresholds = activity_profile["weather_thresholds"] 

 

    variable_map = DAILY_VARIABLE_MAP if is_daily else HOURLY_VARIABLE_MAP 

 

    # build a weather_values dict keyed by threshold name for modifier checks 

    weather_values = {} 

    for col, key in variable_map.items(): 

        if col in weather_record: 

            weather_values[key] = weather_record[col] 

 

    # get terrain modifier multipliers and flat adder 

    multipliers, flat_add = evaluate_terrain_modifiers( 

        activity_profile, weather_values, user_terrain, elevation 

    ) 

 

    breakdown = {} 

    total_score = 0.0 

    variables_checked = 0 

 

 

    #avoid crash if weather_record is missing variables or has invalid data 

    for col, threshold_key in variable_map.items(): 

        if threshold_key not in thresholds: 

            continue 

        if col not in weather_record: 

            continue 

 

        raw_value = weather_record[col] 

        if raw_value is None or (isinstance(raw_value, float) and np.isnan(raw_value)): 

            continue 

 

        # apply any per-variable terrain multiplier to the raw value 

        var_mult = multipliers.get(threshold_key, 1.0) 

        adjusted_value = raw_value * var_mult 

 

        label, score = classify_variable(adjusted_value, thresholds[threshold_key]) 

        breakdown[threshold_key] = { 

            "raw": round(float(raw_value), 2), 

            "adjusted": round(float(adjusted_value), 2), 

            "rating": label, 

            "score": score, 

        } 

        total_score += score 

        variables_checked += 1 

 

    if variables_checked == 0: 

        print("[warning] No variables were matched — check column names vs Variable_remap") 

        return "unknown", 0.0, {} 

     

    # apply score-level multiplier 

    total_score *= multipliers.get("__score__", 1.0) 

    total_score += flat_add 

 

    # normalise to 0–2 scale 

    avg_score = total_score / variables_checked 

 

    if avg_score >= 1.5 or any(v["score"] == 2 for v in breakdown.values()): 

        overall = "dangerous" 

    elif avg_score >= 0.6: 

        overall = "uncomfortable" 

    else: 

        overall = "comfortable" 

 

    return overall, round(avg_score, 3), breakdown 

 

def Prepare_data(validated_weather_record, validated_activity, validated_terrain, elevation, is_daily=False): 

    """ 

    Runs the full pipeline for one weather record. 

    Returns (overall_rating, score, breakdown). 

    """ 

    return Risk_evaluator( 

        weather_record=validated_weather_record, 

        activity_name=validated_activity, 

        user_terrain=validated_terrain, 

        elevation=elevation, 

        is_daily=is_daily 

    ) 

 

def output_lifestyle_forecast(): 

    pass 

 

def gui(): 

    pass 

 

def run(): 

    Location = input("Enter the location you want the weather for or type 1 for coordinate input: ") 

    if Location == "1": 

        lat = float(input("Enter latitude: ")) 

        lon = float(input("Enter longitude: ")) 

        openmeteo_call_weather(lat, lon) 

    else: 

        inp_cleanser(Location) 

        openmeteo_call_weather(get_location_coordinates(Location)[0], get_location_coordinates(Location)[1]) 

#testing function 

def run_test_program(): 

    Location = "London" 

    Location = inp_cleanser(Location) 

    openmeteo_call_weather(get_location_coordinates(Location)[0], get_location_coordinates(Location)[1]) 

    hourly_dataframe_feather, daily_dataframe_feather, _, _ = get_datas() 

    bar_charts(hourly_dataframe_feather, daily_dataframe_feather) 

 

def run_test_lifestyle_forecast(): 

    Location = "London" 

    Location = inp_cleanser(Location) 

    _, _, elevation = openmeteo_call_weather( 

        get_location_coordinates(Location)[0], 

        get_location_coordinates(Location)[1] 

    ) 

    hourly_df, daily_df, _, _ = get_datas() 

    user_terrain = { 

        "terrain_type": "mountain", 

        "exposure": "high", 

        "slope": "steep", 

        "remoteness": "wilderness" 

    } 

    validated_activity = Validate_activity("hiking") 

    validated_terrain = Validate_terrain(user_terrain) 

    lifestyle_forecast(daily_df, hourly_df, "hiking", elevation, is_daily=True) 

    """for i, row in daily_df.iterrows(): 

        record = row.to_dict() 

        validated_record = Validate_weather_data(record.copy()) 

        if not validated_record: 

            continue 

        overall, score, breakdown = Prepare_data( 

            record, 

            validated_activity, 

            validated_terrain, 

            elevation=elevation, 

            is_daily=True 

        ) 

        print(f"\n[{record.get('date', i)}] = {overall} ({score})") 

        print(" Breakdown:", breakdown)""" 

 

#palettes and UI config 

class Cfg: 

    theme     = "Dark" 

    font_size = "medium"   # small, medium, large 

    temp_unit = "°C"       # °C, °F, K 

    wind_unit = "km/h"     # km/h, mph, m/s 

    pres_unit = "hPa"      # hPa, mb, inHg 

    vis_unit  = "m"        # m, km, mi 

 

PALETTES = { 

    "Dark":  dict(BG="#0d1b2a", CARD="#1a2940", CARD2="#1e3050", BORD="#243550", 

                  TXT="#ffffff", MUTED="#8899aa", ACNT="#2b7fff", ctk_mode="dark"), 

    "Light": dict(BG="#f0f4f8", CARD="#ffffff",  CARD2="#e4edf6", BORD="#c8d8ea", 

                  TXT="#0d1b2a", MUTED="#556677", ACNT="#1a6fd4", ctk_mode="light"), 

    "BW":    dict(BG="#ffffff",  CARD="#f0f0f0",  CARD2="#e0e0e0", BORD="#bbbbbb", 

                  TXT="#000000", MUTED="#555555", ACNT="#222222", ctk_mode="light"), 

} 

FONT_sizes = {"small": -3, "medium": 0, "large": 3} 

 

def Palette(k):  return PALETTES[Cfg.theme][k] 

def fs(n): return n + FONT_sizes[Cfg.font_size] 

def F(sz, w="normal"): return ctk.CTkFont(size=fs(sz), weight=w) 

 

#Unit converters in settings tab 

def conv_temp(c): 

    try: 

        v = float(c) 

        u = Cfg.temp_unit 

        if u == "°F": v = v*9/5+32 

        elif u == "K": v += 273.15 

        return f"{v:.1f} {u}" 

    except: return "—" 

 

def conv_wind(kmh): 

    try: 

        v = float(kmh) 

        u = Cfg.wind_unit 

        if u == "mph": v *= 0.621371 

        elif u == "m/s": v /= 3.6 

        return f"{v:.1f} {u}" 

    except: return "—" 

 

def conv_pres(hpa): 

    try: 

        v = float(hpa) 

        u = Cfg.pres_unit 

        if u == "inHg": v *= 0.02953 

        return f"{v:.1f} {u}" 

    except: return "—" 

 

def conv_vis(m): 

    try: 

        v = float(m) 

        u = Cfg.vis_unit 

        if u == "km": v /= 1000 

        elif u == "mi": v /= 1609.34 

        return f"{v:.1f} {u}" 

    except: return "—" 

 

def fmt_col(col, val): #dsipatches the right converter based on column name 

    if any(k in col for k in ("temperature","dew_point","apparent")): return conv_temp(val) 

    if any(k in col for k in ("wind_speed","wind_gusts")):            return conv_wind(val) 

    if "pressure" in col:   return conv_pres(val) 

    if "visibility" in col: return conv_vis(val) 

    try: return f"{float(val):.1f}" 

    except: return "—" 

 

#Shared weather data  

_hdf = _ddf = None 

_elev = 0.0; _city = "—" 

 

def _load_feather(): 

    global _hdf, _ddf 

    try: 

        _hdf = pd.read_feather("hourly_weather_data.feather") 

        _ddf = pd.read_feather("daily_weather_data.feather") 

        return True 

    except: return False 

 

#Condition detection 

def get_cond(row): 

    def g(k): return float(row.get(k, 0) or 0) 

    prec  = g("precipitation") + g("precipitation_sum") + g("rain") + g("rain_sum") 

    cloud = g("cloud_cover") 

    gusts = g("wind_gusts_10m") + g("wind_gusts_10m_max") 

    prob  = g("precipitation_probability_max") 

    if gusts > 55 or (prec > 1.5 and cloud > 70): return "stormy" 

    if prec > 0.5 or prob > 70:                    return "rainy" 

    if cloud > 60:                                  return "cloudy" 

    return "sunny" 

 

# Canvas weather icons colours 

SC = "#f5a623"; CC = "#99b0c8"; RC = "#3a88cc"; LC = "#ffe040"; DC = "#5a6a7a" 

 

# UI COMPONENTS 

def card(p, **kw): #Custom frame with default styling 

    kw.setdefault("fg_color", Palette("CARD")); kw.setdefault("corner_radius", 14) 

    return ctk.CTkFrame(p, **kw) 

 

def lbl(p, t, size=13, w="normal", c=None, **kw): #Custom label with default styling 

    return ctk.CTkLabel(p, text=t, text_color=c or Palette("TXT"), font=F(size, w), **kw) 

 

def pill_toggle(parent, options, var, cmd): # returns a frame of toggle buttons for the given options, linked to var and cmd 

    f = ctk.CTkFrame(parent, fg_color=Palette("BORD"), corner_radius=12) 

    btns = {} 

    def sel(v): 

        var.set(v) 

        for k,b in btns.items(): b.configure(fg_color=Palette("CARD2") if k==v else "transparent") 

        cmd(v) 

 

    for txt,v in options: 

        b = ctk.CTkButton(f, text=txt, width=70, height=26, fg_color="transparent", 

        hover_color=Palette("CARD2"), text_color=Palette("TXT"), corner_radius=10, 

        font=F(11), command=lambda v=v: sel(v)) 

        b.pack(side="left", padx=2, pady=2); btns[v] = b 

    sel(var.get()); return f 

 

DAILY_MAP  = {"temperature_2m_max":("🌡","Temp Max"),"temperature_2m_min":("🌡","Temp Min"), 

               "apparent_temperature_max":("🌡","Feels Max"),"apparent_temperature_min":("🌡","Feels Min"), 

               "precipitation_sum":("🌧","Precipitation"),"precipitation_probability_max":("☔","Rain %"), 

               "wind_speed_10m_max":("💨","Wind Max"),"wind_gusts_10m_max":("💨","Gust Max"), 

               "snowfall_sum":("❄","Snowfall"),"rain_sum":("🌧","Rain Total")} 

HOURLY_MAP = {"temperature_2m":("🌡","Temperature"),"apparent_temperature":("🌡","Feels Like"), 

               "relative_humidity_2m":("💧","Humidity"),"precipitation":("🌧","Precipitation"), 

               "wind_speed_10m":("💨","Wind Speed"),"wind_gusts_10m":("💨","Wind Gusts"), 

               "cloud_cover":("☁","Cloud Cover"),"visibility":("👁","Visibility"), 

               "pressure_msl":("⏱","Pressure"),"dew_point_2m":("💦","Dew Point"),"snowfall":("❄","Snowfall")} 

 

# TAB 1 — WEATHER 

class WeatherTab(ctk.CTkFrame): 

    def __init__(self, master): 

        super().__init__(master, fg_color=Palette("BG"), corner_radius=0) 

        self._sel=0; self._mode=ctk.StringVar(value="daily"); self._panel=ctk.StringVar(value="7day") 

        self._build() 

        self 

        if _load_feather(): self._refresh() 

 

    def _build(self): #Sets up UI components and layout for the weather tab 

        self.grid_columnconfigure(0,weight=3); self.grid_columnconfigure(1,minsize=285); self.grid_rowconfigure(0,weight=1) 

        L = ctk.CTkFrame(self, fg_color="transparent") 

        L.grid(row=0,column=0,sticky="nsew",padx=(0,10)) 

        for r,w in [(0,0),(1,0),(2,0),(3,1),(4,0)]: L.grid_rowconfigure(r,weight=w) 

        L.grid_columnconfigure(0,weight=1) 

 

        # Search 

        sb = card(L,fg_color=Palette("CARD2"),corner_radius=30,height=44) 

        sb.grid(row=0,column=0,sticky="ew",pady=(0,10)); sb.grid_propagate(False) 

        self.search = ctk.CTkEntry(sb,placeholder_text="Search for cities…",fg_color="transparent", 

        border_width=0,text_color=Palette("TXT"),placeholder_text_color=Palette("MUTED"),font=F(13)) 

        self.search.pack(side="left",fill="both",expand=True,padx=16) 

        self.search.bind("<Return>",lambda _: self._fetch()) 

        ctk.CTkButton(sb,text="Search",width=80,height=30,fg_color=Palette("ACNT"),hover_color="#1a5fd0", 

        corner_radius=20,font=F(12),command=self._fetch).pack(side="right",padx=6,pady=7) 

         

        # The hero 

        hero = card(L,fg_color=Palette("CARD2"),height=160); hero.grid(row=1,column=0,sticky="ew",pady=(0,10)); hero.grid_propagate(False) 

        info = ctk.CTkFrame(hero,fg_color="transparent"); info.place(relx=0.03,rely=0.1) 

        self.city_lbl = lbl(info,"—",size=30,w="bold"); self.city_lbl.pack(anchor="w") 

        self.rain_lbl = lbl(info,"Chance of rain: —",size=12,c=Palette("MUTED")); self.rain_lbl.pack(anchor="w",pady=(2,5)) 

        self.temp_lbl = lbl(info,"—",size=36,w="bold"); self.temp_lbl.pack(anchor="w") 

 

        # Hourly strip 

        ts = card(L); ts.grid(row=2,column=0,sticky="ew",pady=(0,10)) 

        lbl(ts,"TODAY'S FORECAST",size=10,c=Palette("MUTED")).pack(anchor="w",padx=16,pady=(12,4)) 

        self.strip = ctk.CTkScrollableFrame(ts,fg_color="transparent",orientation="horizontal",height=106) 

        self.strip.pack(fill="x",padx=8,pady=(0,10)) 

 

        # Conditions 

        cc = card(L); cc.grid(row=3,column=0,sticky="nsew"); cc.grid_columnconfigure(0,weight=1); cc.grid_rowconfigure(1,weight=1) 

        top = ctk.CTkFrame(cc,fg_color="transparent"); top.grid(row=0,column=0,sticky="ew",padx=16,pady=(12,4)) 

        lbl(top,"AIR CONDITIONS",size=10,c=Palette("MUTED")).pack(side="left") 

        self.vars_f = ctk.CTkScrollableFrame(cc,fg_color="transparent",height=160) 

        self.vars_f.grid(row=1,column=0,sticky="nsew",padx=8,pady=(0,8)) 

        pill_toggle(top,[("Daily","daily"),("Hourly","hourly")],self._mode,lambda _:self._build_vars()).pack(side="right") 

        self.status = lbl(L,"",size=11,c=Palette("MUTED")); self.status.grid(row=4,column=0,pady=(4,0)) 

 

        # Right panel 

        R = card(self,corner_radius=18); R.grid(row=0,column=1,sticky="nsew") 

        R.grid_rowconfigure(1,weight=1); R.grid_columnconfigure(0,weight=1) 

        rt = ctk.CTkFrame(R,fg_color="transparent"); rt.grid(row=0,column=0,sticky="ew",padx=14,pady=(14,4)) 

        self.panel_lbl = lbl(rt,"7-DAY FORECAST",size=10,c=Palette("MUTED")); self.panel_lbl.pack(side="left") 

        self.fcast = ctk.CTkScrollableFrame(R,fg_color="transparent") 

        self.fcast.grid(row=1,column=0,sticky="nsew",padx=6,pady=(0,8)) 

        pill_toggle(rt,[("7-Day","7day"),("Hourly","hourly")],self._panel,lambda _:self._build_panel()).pack(side="right") 

 

    def _fetch(self): #Fetches the weather data for location entered in search bar 

        loc = self.search.get().strip() 

        if not loc: return 

        self.status.configure(text="Fetching…") 

        def run(): 

            global _hdf,_ddf,_elev,_city 

            try: 

                from geopy.geocoders import Nominatim 

                geo = Nominatim(user_agent="WeatherApp").geocode(loc) 

                if not geo: raise ValueError("Location not found") 

                _hdf,_ddf,_elev = mp.openmeteo_call_weather(geo.latitude,geo.longitude) 

                _city = geo.address.split(",")[0].strip() 

                self.after(0,self._refresh) 

                self.after(0,lambda: self.status.configure(text=f"Elev: {_elev:.0f} m asl")) 

            except Exception as e: 

                self.after(0,lambda: self.status.configure(text=f"Error: {e}")) 

        threading.Thread(target=run,daemon=True).start() 

 

    def _refresh(self): #Updates the UI with fetched weather data 

        if _ddf is None: return 

        r0 = _ddf.iloc[0].to_dict() 

        self.city_lbl.configure(text=_city) 

        self.temp_lbl.configure(text=conv_temp(r0.get("temperature_2m_max","—"))) 

        rain = float(r0.get("precipitation_probability_max",0) or 0) 

        self.rain_lbl.configure(text=f"Chance of rain: {rain:.0f}%") 

        cond = get_cond(r0) 

        self._build_strip(); self._build_vars(); self._build_panel() 

 

    def _build_strip(self): #Builds the strip showing hourly forecast 

        for w in self.strip.winfo_children(): w.destroy() 

        if _hdf is None: return 

        today = _hdf[_hdf["date"].dt.date == _hdf["date"].dt.date.iloc[0]].head(8) 

        for _,row in today.iterrows(): 

            c = ctk.CTkFrame(self.strip,fg_color=Palette("CARD2"),corner_radius=12,width=80) 

            c.pack(side="left",padx=4); c.pack_propagate(False) 

            lbl(c,pd.Timestamp(row["date"]).strftime("%I%p").lstrip("0"),size=11,c=Palette("MUTED")).pack(pady=(8,2)) 

            cv = tk.Canvas(c,width=32,height=32,highlightthickness=0) 

            lbl(c,conv_temp(row.get("temperature_2m","—")),size=11,w="bold").pack(pady=(2,8)) 

 

    def _build_vars(self): #Builds the list of weather variables 

        for w in self.vars_f.winfo_children(): w.destroy() 

        df = _ddf if self._mode.get()=="daily" else _hdf 

        vm = DAILY_MAP if self._mode.get()=="daily" else HOURLY_MAP 

        if df is None: return 

        row = df.iloc[self._sel].to_dict() 

        for i,(col,(icon,name)) in enumerate(vm.items()): 

            r,c = divmod(i,3); self.vars_f.grid_columnconfigure(c,weight=1) 

            cell = ctk.CTkFrame(self.vars_f,fg_color=Palette("CARD2"),corner_radius=10) 

            cell.grid(row=r,column=c,padx=3,pady=3,sticky="ew") 

            inner = ctk.CTkFrame(cell,fg_color="transparent"); inner.pack(padx=10,pady=7,fill="x") 

            lbl(inner,f"{icon}  {name}",size=11,c=Palette("MUTED"),anchor="w").pack(anchor="w") 

            lbl(inner,fmt_col(col,row.get(col,"—")),size=14,w="bold",anchor="w").pack(anchor="w") 

  

    def _build_panel(self): #Builds right panel showing 7-day or hourly forecast 

        for w in self.fcast.winfo_children(): w.destroy() 

        is7 = self._panel.get()=="7day" 

        self.panel_lbl.configure(text="7-DAY FORECAST" if is7 else "HOURLY FORECAST") 

        (self._build_7day if is7 else self._build_hourly)() 

 

    def _build_7day(self): #Builds 7-day forecast in the right panel 

        if _ddf is None: return 

        names=["Today","Mon","Tue","Wed","Thu","Fri","Sat","Sun","Mon","Tue"] 

        for i,row in _ddf.head(7).iterrows(): 

            rd = row.to_dict(); sel = (i==self._sel) 

            r = ctk.CTkFrame(self.fcast,fg_color=Palette("CARD2") if sel else "transparent",corner_radius=10) 

            r.pack(fill="x",padx=4,pady=2) 

            lbl(r,names[i] if i<len(names) else pd.Timestamp(row["date"]).strftime("%a"), 

                size=12,c=Palette("TXT") if sel else Palette("MUTED"),width=52,anchor="w").pack(side="left",padx=(10,0)) 

            cv = tk.Canvas(r,width=28,height=28,highlightthickness=0) 

            cond_txt = get_cond(rd).capitalize() 

            lbl(r,cond_txt,size=12,w="bold",width=62).pack(side="left") 

            lbl(r,f"/{conv_temp(row.get('temperature_2m_min','—'))}",size=11,c=Palette("MUTED")).pack(side="right",padx=(0,10)) 

            lbl(r,conv_temp(row.get("temperature_2m_max","—")),size=13,w="bold").pack(side="right",padx=2) 

            r.bind("<Button-1>",lambda _,idx=i: self._select(idx)) 

            ctk.CTkFrame(self.fcast,fg_color=Palette("BORD"),height=1,corner_radius=0).pack(fill="x",padx=10) 

 

    def _build_hourly(self): #Builds hourly forecast in the right panel 

        if _hdf is None: return 

        for _,row in _hdf.head(24).iterrows(): 

            rd = row.to_dict() 

            r = ctk.CTkFrame(self.fcast,fg_color="transparent",corner_radius=10); r.pack(fill="x",padx=4,pady=2) 

            lbl(r,pd.Timestamp(row["date"]).strftime("%I:%M%p").lstrip("0"),size=12,c=Palette("MUTED"),width=72,anchor="w").pack(side="left",padx=(10,0)) 

            cv = tk.Canvas(r,width=26,height=26,highlightthickness=0) 

            lbl(r,get_cond(rd).capitalize(),size=12,width=58).pack(side="left") 

            lbl(r,conv_temp(row.get("temperature_2m","—")),size=13,w="bold").pack(side="right",padx=10) 

            ctk.CTkFrame(self.fcast,fg_color=Palette("BORD"),height=1,corner_radius=0).pack(fill="x",padx=10) 

 

    def _select(self,idx): self._sel=idx; self._build_vars(); self._build_panel() 

 

# TAB 2 LIFESTYLE 

class LifestyleTab(ctk.CTkFrame): 

    def __init__(self, master): 

        super().__init__(master,fg_color=Palette("BG"),corner_radius=0); self._build() 

 

    def _build(self): #Sets up UI components and layout for lifestyle forecast tab 

        self.grid_columnconfigure(0,weight=1); self.grid_rowconfigure(1,weight=1) 

        inp = card(self,fg_color=Palette("CARD2"),corner_radius=18); inp.grid(row=0,column=0,sticky="ew",pady=(0,12)) 

        inp.grid_columnconfigure(tuple(range(5)),weight=1) 

        lbl(inp,"Lifestyle Forecast",size=18,w="bold").grid(row=0,column=0,columnspan=5,padx=16,pady=(16,10),sticky="w") 

 

        self.act_var=ctk.StringVar(value="hiking"); self.terr_var=ctk.StringVar(value="mountain") 

        self.exp_var=ctk.StringVar(value="low"); self.slope_var=ctk.StringVar(value="flat") 

        self.rem_var=ctk.StringVar(value="urban"); self.mode_var=ctk.StringVar(value="daily") 

 

        for c,(label,var,opts) in enumerate([ 

            ("Activity",self.act_var,list(set(activity_aliases.values()))), 

            ("Terrain", self.terr_var,["mountain","coastal","trail","road","urban","rural","wilderness"]), 

            ("Exposure",self.exp_var, ["low","medium","high"]), 

            ("Slope",   self.slope_var,["flat","moderate","steep","verysteep"]), 

            ("Remoteness",self.rem_var,["urban","rural","wilderness"]), 

        ]): 

            lbl(inp,label,size=11,c=Palette("MUTED")).grid(row=1,column=c,padx=12,pady=(0,2),sticky="w") 

            ctk.CTkOptionMenu(inp,variable=var,values=opts,fg_color=Palette("CARD"),button_color=Palette("ACNT"), 

            button_hover_color="#1a5fd0",text_color=Palette("TXT"),dropdown_fg_color=Palette("CARD"), 

            dropdown_text_color=Palette("TXT"),corner_radius=10,font=F(12),width=130, 

            ).grid(row=2,column=c,padx=8,pady=(0,12),sticky="ew") 

 

        br = ctk.CTkFrame(inp,fg_color="transparent"); br.grid(row=3,column=0,columnspan=5,padx=12,pady=(0,14),sticky="w") 

        pill_toggle(br,[("Daily","daily"),("Hourly","hourly")],self.mode_var,lambda _:None).pack(side="left",padx=(0,12)) 

        ctk.CTkButton(br,text="Run Forecast ▶",width=140,height=34,fg_color=Palette("ACNT"),hover_color="#1a5fd0", 

        corner_radius=10,font=F(13),command=self._run).pack(side="left") 

        self.status=lbl(br,"",size=12,c=Palette("MUTED")); self.status.pack(side="left",padx=12) 

        self.results=ctk.CTkScrollableFrame(self,fg_color="transparent") 

        self.results.grid(row=1,column=0,sticky="nsew"); self.results.grid_columnconfigure(0,weight=1) 

 

    def _run(self): #Runs the lifestyle forecast based on user inputs and displays results in the right panel 

        if _ddf is None and _hdf is None: 

            self.status.configure(text="Fetch weather first (Weather tab)"); return 

        for w in self.results.winfo_children(): w.destroy() 

        is_daily = self.mode_var.get()=="daily"; df = _ddf if is_daily else _hdf 

        if df is None: self.status.configure(text="No data"); return 

        val_act  = mp.Validate_activity(self.act_var.get()) 

        val_terr = mp.Validate_terrain({"terrain_type":self.terr_var.get(),"exposure":self.exp_var.get(), 

                                        "slope":self.slope_var.get(),"remoteness":self.rem_var.get()}) 

        if not val_act or not val_terr: self.status.configure(text="Invalid inputs"); return 

        RC = {"comfortable":"#3ecf8e","uncomfortable":Palette("ACNT"),"dangerous":"#e05555","unknown":Palette("MUTED")} 

        n = 0 

        for i,row in df.iterrows(): 

            rec = mp.Validate_weather_data(row.to_dict()) 

            if not rec: continue 

            rating,score,breakdown = mp.Prepare_data(rec,val_act,val_terr,_elev,is_daily=is_daily) 

 

            c = card(self.results,fg_color=Palette("CARD"),corner_radius=12) 

            c.grid(row=n,column=0,sticky="ew",padx=4,pady=3); c.grid_columnconfigure(1,weight=1) 

 

            badge = ctk.CTkFrame(c,fg_color=RC.get(rating,Palette("MUTED")),corner_radius=8,width=120,height=30) 

            badge.grid(row=0,column=0,padx=(10,8),pady=8); badge.grid_propagate(False) 

            lbl(badge,rating.upper(),size=11,w="bold",c="#ffffff").place(relx=.5,rely=.5,anchor="center") 

            date_str = pd.Timestamp(row["date"]).strftime("%a %d %b  %H:%M") if "date" in row.index else str(i) 

            lbl(c,date_str,size=12,c=Palette("MUTED")).grid(row=0,column=1,sticky="w") 

            lbl(c,f"score:{score}",size=11,c=Palette("MUTED")).grid(row=0,column=2,padx=10) 

            pills=ctk.CTkFrame(c,fg_color="transparent"); pills.grid(row=1,column=0,columnspan=3,sticky="ew",padx=10,pady=(0,8)) 

 

            for var,info in breakdown.items(): 

                p=ctk.CTkFrame(pills,fg_color=Palette("CARD2"),corner_radius=8); p.pack(side="left",padx=3) 

                lbl(p,f"{var}  {info['raw']}",size=10,c=Palette("MUTED")).pack(padx=8,pady=(4,0)) 

                lbl(p,info["rating"],size=10,w="bold",c=RC.get(info["rating"],Palette("MUTED"))).pack(padx=8,pady=(0,4)) 

            n += 1 

        self.status.configure(text=f"Done — {n} rows scored") 

 

# TAB 3 — GRAPHS 

class GraphsTab(ctk.CTkFrame): 

    GRAPHS = [("Precip %","daily","precipitation_probability_max","bar","☔"), 

              ("Temperature","daily",["temperature_2m_max","temperature_2m_min"],"grouped","🌡"), 

              ("Hourly Temp","hourly","temperature_2m","line","🌡"), 

              ("Wind Speed","hourly","wind_speed_10m","line","💨"), 

              ("Humidity","hourly","relative_humidity_2m","line","💧"), 

              ("Cloud Cover","hourly","cloud_cover","area","☁"), 

              ("Precipitation","hourly","precipitation","bar","🌧"), 

              ("Visibility","hourly","visibility","line","👁")] 

 

    def __init__(self, master): 

        super().__init__(master,fg_color=Palette("BG"),corner_radius=0) 

        self._active=0; self._build() 

 

    def _build(self): #Sets up UI components and layout for the graphs tab 

        self.grid_columnconfigure(0,weight=1); self.grid_columnconfigure(1,minsize=195); self.grid_rowconfigure(0,weight=1) 

        L=ctk.CTkFrame(self,fg_color="transparent"); L.grid(row=0,column=0,sticky="nsew",padx=(0,10)) 

        L.grid_rowconfigure(1,weight=1); L.grid_columnconfigure(0,weight=1) 

        self.title_lbl=lbl(L,"Select a graph",size=22,w="bold"); self.title_lbl.grid(row=0,column=0,sticky="w",pady=(0,8)) 

        cc=card(L); cc.grid(row=1,column=0,sticky="nsew"); cc.grid_rowconfigure(0,weight=1); cc.grid_columnconfigure(0,weight=1) 

        self.fig,self.ax=plt.subplots(figsize=(7,4)) 

        self._style_fig() 

        self.mpl=FigureCanvasTkAgg(self.fig,master=cc) 

        self.mpl.get_tk_widget().grid(row=0,column=0,sticky="nsew",padx=8,pady=8) 

        R=card(self,corner_radius=18); R.grid(row=0,column=1,sticky="nsew") 

        lbl(R,"SELECT GRAPH",size=10,c=Palette("MUTED")).pack(anchor="w",padx=16,pady=(12,4)) 

        self._btns=[] 

        for i,(name,*_,icon) in enumerate(self.GRAPHS): 

            b=ctk.CTkButton(R,text=f"{icon}  {name}",anchor="w",fg_color="transparent",hover_color=Palette("CARD2"), 

                            text_color=Palette("TXT"),corner_radius=10,font=F(12),height=40,command=lambda i=i:self._plot(i)) 

            b.pack(fill="x",padx=8,pady=3); self._btns.append(b) 

 

    def _style_fig(self): #Applies styling to the matplotlib figure 

        bg=Palette("CARD"); self.fig.patch.set_facecolor(bg); self.ax.set_facecolor(Palette("BG")) 

        self.ax.tick_params(colors=Palette("MUTED")); [s.set_color(Palette("BORD")) for s in self.ax.spines.values()] 

 

    def _plot(self,idx): #Plots the selected graph based on idx and updates the right panel 

        self._active=idx 

        for i,b in enumerate(self._btns): b.configure(fg_color=Palette("CARD2") if i==idx else "transparent") 

        name,source,col,chart,_=self.GRAPHS[idx] 

        self.title_lbl.configure(text=name); self.ax.clear(); self._style_fig() 

        df=_ddf if source=="daily" else _hdf 

        if df is None: 

            self.ax.text(.5,.5,"No data — search a location first",ha="center",va="center", 

            color=Palette("MUTED"),transform=self.ax.transAxes) 

        else: 

            n=min(len(df),168); xs=df.head(n); x=np.arange(n); ac=Palette("ACNT") 

            if chart=="grouped": 

                self.ax.bar(x-.18,xs[col[0]].values,.35,color="#e05555",alpha=.85,label="Max") 

                self.ax.bar(x+.18,xs[col[1]].values,.35,color=ac,alpha=.85,label="Min") 

                self.ax.legend(framealpha=0,labelcolor=Palette("TXT")) 

            elif chart=="bar": self.ax.bar(x,xs[col].values,color=ac,alpha=.8) 

            elif chart=="area": 

                self.ax.fill_between(x,xs[col].values,alpha=.35,color=ac) 

                self.ax.plot(x,xs[col].values,color=ac,linewidth=1.5) 

            else: self.ax.plot(x,xs[col].values,color=ac,linewidth=2) 

            self.ax.set_ylabel(col if isinstance(col,str) else col[0],color=Palette("MUTED")) 

        self.fig.tight_layout(pad=1.5); self.mpl.draw() 

 

# TAB 4 — SETTINGS 

class SettingsTab(ctk.CTkFrame): 

    def __init__(self, master, on_apply): 

        super().__init__(master,fg_color=Palette("BG"),corner_radius=0) 

        self._apply_cb = on_apply; self._build() 

 

    def _build(self): 

        self.grid_columnconfigure((0,1),weight=1); self.grid_rowconfigure(0,weight=1) 

 

        # Left column 

        L=card(self,corner_radius=18); L.grid(row=0,column=0,sticky="nsew",padx=(0,10)) 

        self._sec(L,"Appearance") 

        self._thm_var=ctk.StringVar(value=Cfg.theme) 

        self._opt(L,"Theme",self._thm_var,["dark","light","bw"]) 

        self._sec(L,"Font Size") 

        self._fsz_var=ctk.StringVar(value=Cfg.font_size) 

        self._opt(L,"Text size",self._fsz_var,["small","medium","large"]) 

        self._sec(L,"Temperature Unit") 

        self._tmp_var=ctk.StringVar(value=Cfg.temp_unit) 

        self._opt(L,"Unit",self._tmp_var,["°C","°F","K"]) 

 

        # Right column 

        R=card(self,corner_radius=18); R.grid(row=0,column=1,sticky="nsew") 

        self._sec(R,"Wind Speed Unit") 

        self._wnd_var=ctk.StringVar(value=Cfg.wind_unit) 

        self._opt(R,"Unit",self._wnd_var,["km/h","mph","m/s"]) 

        self._sec(R,"Pressure Unit") 

        self._prs_var=ctk.StringVar(value=Cfg.pres_unit) 

        self._opt(R,"Unit",self._prs_var,["hPa","mb","inHg"]) 

        self._sec(R,"Visibility Unit") 

        self._vis_var=ctk.StringVar(value=Cfg.vis_unit) 

        self._opt(R,"Unit",self._vis_var,["m","km","mi"]) 

 

        # Apply button 

        btn_frame=ctk.CTkFrame(self,fg_color="transparent"); btn_frame.grid(row=1,column=0,columnspan=2,pady=12) 

        ctk.CTkButton(btn_frame,text="Apply Settings",width=180,height=40,fg_color=Palette("ACNT"), 

        hover_color="#1a5fd0",corner_radius=12,font=F(14,w="bold"), 

        command=self._apply).pack() 

        self._note=lbl(btn_frame,"",size=11,c=Palette("MUTED")); self._note.pack(pady=(6,0)) 

 

    def _sec(self,p,t): #Helper to create section headers in settings tab 

        lbl(p,t,size=12,w="bold",c=Palette("MUTED")).pack(anchor="w",padx=16,pady=(14,2)) 

        ctk.CTkFrame(p,fg_color=Palette("BORD"),height=1,corner_radius=0).pack(fill="x",padx=16,pady=(0,6)) 

 

    def _opt(self,p,label,var,opts): #Helper to create option rows in settings tab 

        row=ctk.CTkFrame(p,fg_color=Palette("CARD2"),corner_radius=12,height=46) 

        row.pack(fill="x",padx=12,pady=4); row.pack_propagate(False) 

        lbl(row,label,size=13).pack(side="left",padx=14) 

        ctk.CTkOptionMenu(row,variable=var,values=opts,fg_color=Palette("CARD"),button_color=Palette("ACNT"), 

        button_hover_color="#1a5fd0",text_color=Palette("TXT"),dropdown_fg_color=Palette("CARD"), 

        dropdown_text_color=Palette("TXT"),corner_radius=10,font=F(12),width=130, 

        ).pack(side="right",padx=10,pady=8) 

 

    def _apply(self): 

        Cfg.theme=self._thm_var.get(); Cfg.font_size=self._fsz_var.get() 

        Cfg.temp_unit=self._tmp_var.get(); Cfg.wind_unit=self._wnd_var.get() 

        Cfg.pres_unit=self._prs_var.get(); Cfg.vis_unit=self._vis_var.get() 

        ctk.set_appearance_mode(PALETTES[Cfg.theme]["ctk_mode"]) 

        self._note.configure(text="✓ Settings applied — rebuilding…") 

        self.after(200, self._apply_cb) 

 

# MAIN APP 

class App(ctk.CTk): 

    TABS = [("🌤","Weather"),("🏃","Lifestyle"),("📊","Graphs"),("⚙","Settings")] 

 

    def __init__(self): #Initializes main application window and sets up sidebar and pages 

        super().__init__() 

        self.title("Weather App"); self.geometry("1300x780"); self.minsize(960,620) 

        ctk.set_appearance_mode(PALETTES[Cfg.theme]["ctk_mode"]) 

        self.configure(fg_color=Palette("BG")) 

        self.grid_columnconfigure(1,weight=1); self.grid_rowconfigure(0,weight=1) 

        self._build_sidebar(); self._current=0; self._pages={}; self._rebuild() 

 

    #left sidebar with navigation buttons 

    def _build_sidebar(self): 

        self.sb=card(self,fg_color=Palette("CARD"),corner_radius=18,width=76) 

        self.sb.grid(row=0,column=0,sticky="ns",padx=(12,6),pady=12); self.sb.grid_propagate(False) 

        logo=card(self.sb,fg_color=Palette("ACNT"),corner_radius=14,width=46,height=46) 

        logo.pack(pady=(16,20)); logo.pack_propagate(False) 

        lbl(logo,"⛅",size=20).pack(expand=True) 

        self._nav_btns=[] 

        for i,(icon,name) in enumerate(self.TABS): 

            f=ctk.CTkFrame(self.sb,fg_color="transparent"); f.pack(pady=4) 

            b=ctk.CTkButton(f,text=icon,width=46,height=46,fg_color="transparent",hover_color=Palette("CARD2"), 

                            corner_radius=12,font=F(20),command=lambda i=i:self._show(i)); b.pack() 

            lbl(f,name,size=9,c=Palette("MUTED")).pack(); self._nav_btns.append(b) 

 

    def _rebuild(self): #rebuilds pages with updated settings and refreshes UI 

        for p in self._pages.values(): p.destroy() 

        self._pages={ 

            0: WeatherTab(self), 

            1: LifestyleTab(self), 

            2: GraphsTab(self), 

            3: SettingsTab(self, on_apply=self._on_settings_apply), 

        } 

        # update sidebar 

        self.sb.configure(fg_color=Palette("CARD")) 

        for i,b in enumerate(self._nav_btns): 

            b.configure(hover_color=Palette("CARD2"),fg_color=Palette("CARD2") if i==self._current else "transparent") 

        self.configure(fg_color=Palette("BG")) 

        self._show(self._current) 

 

    def _on_settings_apply(self): 

        self._rebuild() 

 

    # Show the page at index and hide others 

    def _show(self,idx): 

        for p in self._pages.values(): p.grid_forget() 

        self._pages[idx].grid(row=0,column=1,sticky="nsew",padx=(0,12),pady=12) 

        self._current=idx 

        for i,b in enumerate(self._nav_btns): 

            b.configure(fg_color=Palette("CARD2") if i==idx else "transparent") 

 

if __name__=="__main__": 

    App().mainloop() 