import * as cdk from '@aws-cdk/core';
import * as apigatewayv2 from '@aws-cdk/aws-apigatewayv2';
import * as apigatewayv2_integrations from '@aws-cdk/aws-apigatewayv2-integrations';
import * as cognito from '@aws-cdk/aws-cognito';
import * as lambda from '@aws-cdk/aws-lambda';
import * as lambdaPython from '@aws-cdk/aws-lambda-python';
import * as dynamodb from '@aws-cdk/aws-dynamodb';

export interface APIStackProps {
    env: cdk.Environment;
    predictionService: string;
}

export class APIStack extends cdk.Stack {

    constructor(scope: cdk.Construct, id: string, props: APIStackProps) {
        super(scope, id, props);

        // ------------------------------
        // ------------ AUTH ------------
        // ------------------------------
        const userPool = new cognito.UserPool(this, 'UserPool', {
            userPoolName: 'enercast-userpool',
            selfSignUpEnabled: true,
            signInAliases: {
                username: true,
                email: true
            }
        });

        const userPoolClient1 = userPool.addClient('react-client', {
            preventUserExistenceErrors: true
        });

        /*const apiAuth = new apigateway.CognitoUserPoolsAuthorizer(this, 'UserPoolAuthorizer', {
            cognitoUserPool: [userPool]
        });*/

        // ----------------------------------
        // ------------ DynamoDB ------------
        // ----------------------------------
        const userTable = new dynamodb.Table(this, 'UserTable', {
            billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
            partitionKey: {
                name: 'ID',
                type: dynamodb.AttributeType.STRING
            }
        });

        // --------------------------------
        // ------------ LAMBDA ------------
        // --------------------------------
        const defaultHandler = new lambda.Function(this, 'DefaultHandler', {
            runtime: lambda.Runtime.PYTHON_3_8,
            handler: 'default.handler',
            code: lambda.Code.fromAsset('api')
        });

        const getUserHandler = new lambdaPython.PythonFunction(this, 'GetUserHandler', {
            runtime: lambda.Runtime.PYTHON_3_8,
            handler: 'handler',
            entry: 'api',
            index: 'get_user.py',
            tracing: lambda.Tracing.ACTIVE,
            environment: {
                "USER_TABLE_NAME": userTable.tableName
            }
        });
        userTable.grantReadWriteData(getUserHandler);

        const submitPredictionHandler = new lambdaPython.PythonFunction(this, 'SubmitPredictionHandler', {
            runtime: lambda.Runtime.PYTHON_3_8,
            handler: 'handler',
            entry: 'api',
            index: 'submit_prediction.py',
            tracing: lambda.Tracing.ACTIVE,
            environment: {
                "USER_TABLE_NAME": userTable.tableName,
                "PREDICTION_SERVICE_ENDPOINT": props.predictionService
            }
        });
        userTable.grantReadWriteData(submitPredictionHandler);

        const submitCCInfoHandler = new lambdaPython.PythonFunction(this, 'SubmitCCInfoHandler', {
            runtime: lambda.Runtime.PYTHON_3_8,
            handler: 'handler',
            entry: 'api',
            index: 'submit_cc_info.py',
            tracing: lambda.Tracing.ACTIVE,
            environment: {
                "USER_TABLE_NAME": userTable.tableName
            }
        });
        userTable.grantReadWriteData(submitCCInfoHandler);

        // -----------------------------
        // ------------ API ------------
        // -----------------------------
        const api = new apigatewayv2.HttpApi(this, 'Api', {
            corsPreflight: {
                allowHeaders: ['Authorization', 'Content-Type'],
                allowMethods: [
                    apigatewayv2.HttpMethod.GET,
                    apigatewayv2.HttpMethod.HEAD,
                    apigatewayv2.HttpMethod.OPTIONS,
                    apigatewayv2.HttpMethod.POST
                ],
                allowCredentials: false,
                allowOrigins: ['*'],
                maxAge: cdk.Duration.days(1),
            },
        });

        new cdk.CfnOutput(this, 'ApiEndpoint', {
            value: api.apiEndpoint
        });

        api.addRoutes({
            path: '/user',
            methods: [apigatewayv2.HttpMethod.GET],
            integration: new apigatewayv2_integrations.LambdaProxyIntegration({
                handler: getUserHandler
            })
        });

        api.addRoutes({
            path: '/user/submit_prediction',
            methods: [apigatewayv2.HttpMethod.POST],
            integration: new apigatewayv2_integrations.LambdaProxyIntegration({
                handler: submitPredictionHandler
            })
        });

        api.addRoutes({
            path: '/user/submit_cc_info',
            methods: [apigatewayv2.HttpMethod.POST],
            integration: new apigatewayv2_integrations.LambdaProxyIntegration({
                handler: submitCCInfoHandler
            })
        });
    }
}
