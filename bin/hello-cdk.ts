#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { EnergyConsumptionPredStack } from '../lib/energy-consumption-prediction-stack';
import { APIStack } from '../lib/api-stack';

// Hardcoding the ACC + Region since we aren't going to bother with comprehensive development support at this point
const ACCOUNT = "460407672535";
const REGION = "us-east-2";
const deploymentEnv = {
    account: ACCOUNT,
    region: REGION
};

const app = new cdk.App();

const energyConsumptionPredStack =  new EnergyConsumptionPredStack(
    app,
    'EnergyConsumptionPredStack',
    { env: deploymentEnv }
);

new APIStack(
    app,
    'ApiStack',
    {
        env: deploymentEnv,
        predictionService: energyConsumptionPredStack.output.serviceUrl
    }
);
