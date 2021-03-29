# infra

Infrastructure

## Other useful commands (not CDK related)

Remove all pycache folders and pyc files:

```
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
```

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template

## Local Testing

### Setup

Make sure you have Python 3.8+ installed, then run: `pip3 install -r requirements.pip`

### Execution

Run `./test.sh`

### Example Curl Requests

Given an API endpoint, the following are sample curl requests:

```
curl -X POST -H "Content-Type: application/json" --data '{"prediction_parameters":{"start_date": "2020-05-12", "end_date": "2020-05-17", "setup_days": "5", "teardown_days": "2", "forecast_attendance": "10000", "is_audio": "1"}}' https://ewibuq9g18.execute-api.us-east-2.amazonaws.com/user/submit_prediction

curl -X GET https://ewibuq9g18.execute-api.us-east-2.amazonaws.com/user

curl -X POST -H "Content-Type: application/json" --data '{"cc_info":{"sqft": "100000"}}' https://ewibuq9g18.execute-api.us-east-2.amazonaws.com/user/submit_cc_info
```
