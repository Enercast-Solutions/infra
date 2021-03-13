from sklearn.linear_model import Ridge
from flask import Flask
from flask import request
import pickle
from typing import Any, List
import math
import json
from datetime import datetime
app = Flask(__name__)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


def process_request(data: dict) -> List[Any]:
    # Model parameters:
    # ['Event Days', 'SQFT per Event', 'Forecast Attendance', 'avgTmp', 'Total Days (In-Out)', 'isAudio', 'sqrtAttn']

    start_iso_date = datetime.strptime(data["start_date"],'%Y-%m-%d')
    end_iso_date = datetime.strptime(data["end_date"],'%Y-%m-%d')

    duration_in_s = (end_iso_date - start_iso_date).total_seconds()
    duration_days = divmod(duration_in_s, 86400)[0]

    total_days = duration_days + int(data["setup_days"]) + int(data["teardown_days"])

    # Calculate temperature of event
    avgGATmp = [35, 40, 46, 54, 63, 70, 72, 72, 67, 56, 44, 41]
    event_temperature = (avgGATmp[start_iso_date.month - 1] + avgGATmp[end_iso_date.month - 1]) / 2.0


    return [[
        duration_days,
        int(data["sqft"]),
        int(data["forecast_attendance"]),
        event_temperature,
        total_days,
        int(data["is_audio"]),
        math.sqrt(int(data["forecast_attendance"]))
    ]]


def predict(data: List[List[Any]]) -> float:
    return model.predict(data)


@app.route('/')
def index():
    return "<h1>Hello, World!</h1>"


@app.route('/health')
def health():
    return ""


@app.route('/energy_consumption_prediction', methods=["POST"])
def energy_consumption_prediction():
    data = process_request(request.get_json())
    prediction = str(predict(data)[0])

    return json.dumps({"energy_consumption_kwh": prediction})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
