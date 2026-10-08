activity_profiles = {

    "hiking": {
    "weather_thresholds": {
        "temperature":               {"comfortable": (10, 20),   "uncomfortable": [(0, 9), (21, 30)],   "dangerous": [(-100, -1), (31, 100)]},
        "wind_speed":                {"comfortable": (0, 25),    "uncomfortable": [(26, 45)],            "dangerous": [(46, 200)]},
        "wind_gusts":                {"comfortable": (0, 35),    "uncomfortable": [(36, 55)],            "dangerous": [(56, 200)]},
        "precipitation":             {"comfortable": (0, 1),     "uncomfortable": [(1.01, 5)],           "dangerous": [(5.01, 200)]},
        "precipitation_probability": {"comfortable": (0, 40),    "uncomfortable": [(41, 70)],            "dangerous": [(71, 100)]},
        "visibility":                {"comfortable": (5000, 1000000),"uncomfortable": [(1000, 4999)],        "dangerous": [(0, 999)]},
        "snowfall":                  {"comfortable": (0, 0),     "uncomfortable": [(0.01, 0.99)],        "dangerous": [(1, 200)]},
    },
    "terrain_modifiers": {
        "high_exposure": {
            "condition": {"exposure": "high"},
            "multipliers": {"wind_speed": 1.25, "wind_gusts": 1.25}
        },
        "elevation_effect": {
            "condition": {"min_elevation": 800},
            "multipliers": {"ALL": 1.15}          # applies to final risk score
        },
        "remote_low_visibility": {
            "condition": {"remoteness": "wilderness", "max_visibility": 2000},
            "flat_risk_add": 1                     # adds directly to risk score
        },
        "slope_rain": {
            "condition": {"slope": ["steep", "verysteep"], "min_precipitation": 0.1},
            "flat_risk_add": 1
        },
    }
},

"cycling": {
    "weather_thresholds": {
        "temperature":               {"comfortable": (12, 22),    "uncomfortable": [(5, 11), (23, 30)],   "dangerous": [(-100, 4), (35, 100)]},
        "wind_speed":                {"comfortable": (0, 20),     "uncomfortable": [(21, 35)],            "dangerous": [(36, 49), (50, 200)]},
        "wind_gusts":                {"comfortable": (0, 30),     "uncomfortable": [(31, 50)],            "dangerous": [(51, 200)]},
        "precipitation":             {"comfortable": (0, 0),      "uncomfortable": [(0.01, 3)],           "dangerous": [(3.01, 200)]},
        "precipitation_probability": {"comfortable": (0, 30),     "uncomfortable": [(31, 60)],            "dangerous": [(61, 100)]},
        "visibility":                {"comfortable": (3000, 1000000), "uncomfortable": [(1000, 2999)],        "dangerous": [(0, 999)]},
        "humidity":                  {"comfortable": (20, 75),    "uncomfortable": [(76, 88)],            "dangerous": [(89, 100)]},
    },
    "terrain_modifiers": {
        "wet_steep_descent": {
            "condition": {"min_precipitation": 1.0, "slope": ["steep", "verysteep"]},
            "flat_risk_add": 2
        },
        "crosswind_exposed": {
            "condition": {"exposure": "high"},
            "multipliers": {"wind_speed": 1.3, "wind_gusts": 1.3}
        },
        "ice_risk": {
            "condition": {"max_temperature": 2, "min_precipitation": 0.1},
            "flat_risk_add": 2
        },
        "elevation_effect": {
            "condition": {"min_elevation": 800},
            "multipliers": {"__score__": 1.1}
        },
    }
},

"running": {
    "weather_thresholds": {
        "temperature":               {"comfortable": (8, 18),     "uncomfortable": [(0, 7), (19, 28)],   "dangerous": [(-100, -1), (29, 100)]},
        "wind_speed":                {"comfortable": (0, 20),     "uncomfortable": [(21, 35)],            "dangerous": [(36, 200)]},
        "wind_gusts":                {"comfortable": (0, 30),     "uncomfortable": [(31, 45)],            "dangerous": [(46, 200)]},
        "precipitation":             {"comfortable": (0, 0),      "uncomfortable": [(0.01, 3)],           "dangerous": [(3.01, 200)]},
        "precipitation_probability": {"comfortable": (0, 40),     "uncomfortable": [(41, 70)],            "dangerous": [(71, 100)]},
        "visibility":                {"comfortable": (2000, 1000000), "uncomfortable": [(500, 1999)],         "dangerous": [(0, 499)]},
        "humidity":                  {"comfortable": (30, 70),    "uncomfortable": [(71, 85)],            "dangerous": [(86, 100)]},
    },
    "terrain_modifiers": {
        "wet_ground": {
            "condition": {"min_precipitation": 0.1},
            "flat_risk_add": 1
        },
        "steep_downhill_rain": {
            "condition": {"min_precipitation": 0.1, "slope": ["steep", "verysteep"]},
            "flat_risk_add": 2
        },
        "heat_stress": {
            "condition": {"min_temperature": 26, "min_humidity": 75},
            "multipliers": {"__score__": 1.3}
        },
        "remote_injury_risk": {
            "condition": {"remoteness": "wilderness"},
            "multipliers": {"__score__": 1.1}
        },
    }
},
}

activity_aliases = {
    # hiking
    "hiking": "hiking", "hike": "hiking", "trekking": "hiking", "trek": "hiking",
    # cycling
    "cycling": "cycling", "cycle": "cycling", "bike": "cycling", "biking": "cycling",
    # running
    "running": "running", "run": "running", "jogging": "running", "jog": "running",
    # swimming
    "swimming": "swimming", "swim": "swimming",
    # walking
    "walking": "walking", "walk": "walking", "strolling": "walking", "stroll": "walking",
}

terrain_amplifiers = {
    "hiking": {
        "high_exposure_risk":{ "multipliers":{
            "wind_multiplier": 1.25,
            "gust_multiplier": 1.25
        }
        ,
        "arithmetics": {
            "wind_speed": 1,
            "wind_gusts": 1
        }
        },
        "slope_rain_interaction": 1,
        "elevation_effect": 1.15,
        "remote_low_visibility": 1
    },
}