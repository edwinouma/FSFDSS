from utils.prediction import predict_all

user_inputs = {

    "year": 2025,

    "debt_level": 150,
    "herd_size": 80,
    "crop_production": 500,

    "rainfall": 120,
    "ndvi": 0.45,
    "river_level": 3.5,

    "cmb": 120,
    "goat_price": 45000,
    "rice_price": 80,
    "sorghum_price": 60,
    "water_price": 10,

    "conflict_incidents": 5,
    "conflict_fatalities": 2,

    "livelihood_zone":
        "Bay Agropastoral"
}

results = predict_all(user_inputs)

print(results)