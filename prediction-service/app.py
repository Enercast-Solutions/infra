from flask import Flask
from flask import request
import pickle
import joblib
from typing import Any, List, Tuple
import math
import json
from datetime import datetime
from datetime import timedelta
app = Flask(__name__)

energy_consumption_pred_model = joblib.load("xgboost.joblib.dat")
cost_pred_model = joblib.load("PricingModel.joblib.dat")


def calculate_duration_days(start_date, end_date) -> int:
    # we add a day because all days are indexed at time = 0
    duration_in_s = (end_date - start_date).total_seconds() + 86400

    return divmod(duration_in_s, 86400)[0]


def calculate_avg_temp(start_date, end_date) -> float:
    avgGATmp = [35, 40, 46, 54, 63, 70, 72, 72, 67, 56, 44, 41]

    return (avgGATmp[start_date.month - 1] + avgGATmp[end_date.month - 1]) / 2.0


def calculate_is_summer(date) -> int:
    return int(date.month >= 6 and date.month <= 9)


def calculate_is_weekend(date) -> int:
    return int(date.weekday() == 5 or date.weekday() == 6)


def predict_energy_consumption(data: dict) -> float:
    # energy_consumption_pred_model parameters:
    # [‘SQFT per Event’, ‘Forecast Attendance’, ‘avgTmp’, ‘Total Days (In-Out)’, ‘specialEquip’, ‘sqrtAttn’]

    start_iso_date = datetime.strptime(data["start_date"],'%Y-%m-%d')
    end_iso_date = datetime.strptime(data["end_date"],'%Y-%m-%d')

    duration_days = calculate_duration_days(start_iso_date, end_iso_date)

    total_days = duration_days + int(data["setup_days"]) + int(data["teardown_days"])

    event_temperature = calculate_avg_temp(start_iso_date, end_iso_date)

    pred_data = [
        int(data["sqft"]),
        int(data["forecast_attendance"]),
        event_temperature,
        total_days,
        int(data["is_audio"]),
        math.sqrt(int(data["forecast_attendance"]))
    ]

    return energy_consumption_pred_model.predict(pred_data)[0] * duration_days


def predict_cost(data: dict, energy_consumed: float) -> float:
    # energy_consumption_pred_model parameters:
    # [‘SQFT per Event’, ‘Forecast Attendance’, ‘isSummer’, ‘Total Days (In-Out)’, ‘specialEquip’, ‘sqrtAttn’, ‘isWeekend’, ‘Energy Used (kWh)’, ‘EventDayNumber’, ‘Weekend kWh’, ‘Summer weekday kwh’, ‘Summer weekend kwh’, ‘avgTmp’ ]

    start_iso_date = datetime.strptime(data["start_date"],'%Y-%m-%d')
    end_iso_date = datetime.strptime(data["end_date"],'%Y-%m-%d')

    duration_days = calculate_duration_days(start_iso_date, end_iso_date)

    energy_consumed_per_day = energy_consumed / duration_days

    total_days = duration_days + int(data["setup_days"]) + int(data["teardown_days"])

    event_temperature = calculate_avg_temp(start_iso_date, end_iso_date)

    total_cost = 0.0
    for i in range(int(duration_days)):
        event_day = start_iso_date + timedelta(days=i)

        is_summer = calculate_is_summer(event_day)
        is_weekend = calculate_is_weekend(event_day)

        pred_data = [
            int(data["sqft"]),
            int(data["forecast_attendance"]),
            is_summer,
            total_days,
            int(data["is_audio"]),
            math.sqrt(int(data["forecast_attendance"])),
            is_weekend,
            energy_consumed_per_day,
            i,
            is_weekend * energy_consumed_per_day,
            is_summer * (not is_weekend) * energy_consumed_per_day,
            is_summer * is_weekend * energy_consumed_per_day,
            event_temperature
        ]

        total_cost += cost_pred_model.predict(pred_data)[0]

    return total_cost


def predict_baseline_cost(data: dict) -> float:
    baseline_cost_weekday = [1195.07, 1244.49, 1076.39, 1026.48, 1033.19, 2670.87, 2877.0, 2966.68, 2687.91, 918.55, 958.32, 1073.86]
    baseline_cost_weekend = [1065.32, 1095.21, 1085.02, 1067.74]

    start_iso_date = datetime.strptime(data["start_date"],'%Y-%m-%d')
    end_iso_date = datetime.strptime(data["end_date"],'%Y-%m-%d')

    duration_days = calculate_duration_days(start_iso_date, end_iso_date)

    total_cost = 0.0
    for i in range(int(duration_days)):
        event_day = start_iso_date + timedelta(days=i)

        is_summer = calculate_is_summer(event_day)
        is_weekend = calculate_is_weekend(event_day)

        if not is_summer or not is_weekend:
            total_cost += baseline_cost_weekday[event_day.month - 1]
        elif is_weekend:
            total_cost += baseline_cost_weekend[event_day.month - 6]

    return total_cost


@app.route('/')
def index():
    return "<h1>Hello, World!</h1>"


@app.route('/health')
def health():
    return ""


@app.route('/energy_consumption_prediction', methods=["POST"])
def energy_consumption_prediction():
    energy_consumed = predict_energy_consumption(request.get_json())
    cost = predict_cost(request.get_json(), energy_consumed)
    baseline_cost = predict_baseline_cost(request.get_json())

    return json.dumps({
        "energy_consumption_kwh": str(energy_consumed),
        "energy_consumption_cost": str(cost),
        "energy_consumption_baseline_cost": str(baseline_cost)
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
