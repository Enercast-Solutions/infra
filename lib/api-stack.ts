import * as cdk from '@aws-cdk/core';
import * as apigatewayv2 from '@aws-cdk/aws-apigatewayv2';
import * as apigatewayv2_integrations from '@aws-cdk/aws-apigatewayv2-integrations';
import * as lambda from '@aws-cdk/aws-lambda';
import * as lambdaPython from '@aws-cdk/aws-lambda-python';
import * as dynamodb from '@aws-cdk/aws-dynamodb';
import * as apigatewayv2_authorizers from '@aws-cdk/aws-apigatewayv2-authorizers';

export interface APIStackProps {
    env: cdk.Environment;
    predictionService: string;
}

export class APIStack extends cdk.Stack {

    constructor(scope: cdk.Construct, id: string, props: APIStackProps) {
        super(scope, id, props);

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

        const contactUsRequestsTable = new dynamodb.Table(this, 'ContactUsRequests', {
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

        const submitContactUs = new lambdaPython.PythonFunction(this, 'SubmitContactUsHandler', {
            runtime: lambda.Runtime.PYTHON_3_8,
            handler: 'handler',
            entry: 'api',
            index: 'submit_contact_us.py',
            tracing: lambda.Tracing.ACTIVE,
            environment: {
                "CONTACT_US_REQUESTS_TABLE_NAME": contactUsRequestsTable.tableName
            }
        });
        contactUsRequestsTable.grantReadWriteData(submitContactUs);

        // -----------------------------
        // ------------ API ------------
        // -----------------------------
        // NOTE: The following authorizer information is using the infrastructure deployed by Amplify
        const authorizer = new apigatewayv2_authorizers.HttpJwtAuthorizer({
            jwtAudience: ['18dbpvsphlv3pl0vqq49vnfhn6', '2ocbukrlahfa5l9d595llbtfm5'],
            jwtIssuer: 'https://cognito-idp.us-east-2.amazonaws.com/us-east-2_qtBoat5ir',
        });

        const api = new apigatewayv2.HttpApi(this, 'Api', {
            defaultAuthorizer: authorizer,
            corsPreflight: {
                allowHeaders: ['Authorization', 'Content-Type'],
                allowMethods: [
                    apigatewayv2.CorsHttpMethod.GET,
                    apigatewayv2.CorsHttpMethod.HEAD,
                    apigatewayv2.CorsHttpMethod.OPTIONS,
                    apigatewayv2.CorsHttpMethod.POST
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

        api.addRoutes({
            path: '/user/submit_contact_us',
            methods: [apigatewayv2.HttpMethod.POST],
            integration: new apigatewayv2_integrations.LambdaProxyIntegration({
                handler: submitContactUs
            })
        });
    }
}
