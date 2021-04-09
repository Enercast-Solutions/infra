# Energy Consumption Prediction Task

Energy Consumption Prediction Task

## Deployment

NOTE: For security purposes, the model files (`*.pkl`) are NOT saved in Git. You need to Manually place these files in this directory before you build and deploy in order for everything to work properly. Currently, these files are named:

- `xgboost.joblib.dat` -- Energy consumption model
- `PricingModel.joblib.dat` -- Pricing model

## Build

`./build.sh`

## Run

`./run.sh`

## Test

Example queries (for local testing):

```
curl -X POST -H "Content-Type: application/json" -d '{"start_date": "2020-05-29", "end_date": "2020-06-4", "setup_days": "2", "teardown_days": "2", "sqft": "100000", "forecast_attendance": "5000", "is_audio": "0"}' localhost:5000/energy_consumption_prediction

curl -X POST -H "Content-Type: application/json" -d '{"start_date": "2020-06-10", "end_date": "2020-06-15", "setup_days": "2", "teardown_days": "2", "sqft": "100000", "forecast_attendance": "5000", "is_audio": "0"}' localhost:5000/energy_consumption_prediction

curl -X POST -H "Content-Type: application/json" -d '{"start_date": "2020-01-10", "end_date": "2020-01-15", "setup_days": "2", "teardown_days": "2", "sqft": "100000", "forecast_attendance": "5000", "is_audio": "0"}' localhost:5000/energy_consumption_prediction
```

Example queries for actual testing (given a sample URL):

```
curl -X POST -H "Content-Type: application/json" -d '{"start_date": "2020-01-10", "end_date": "2020-01-15", "setup_days": "2", "teardown_days": "2", "sqft": "100000", "forecast_attendance": "5000", "is_audio": "0"}' http://Energ-Energ-CCZ3G5BM264A-441679197.us-east-2.elb.amazonaws.com/energy_consumption_prediction
```
