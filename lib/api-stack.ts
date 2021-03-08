import * as cdk from '@aws-cdk/core';
import * as apigatewayv2 from '@aws-cdk/aws-apigatewayv2';
import * as apigatewayv2_integrations from '@aws-cdk/aws-apigatewayv2-integrations';
import * as cognito from '@aws-cdk/aws-cognito';
import * as lambda from '@aws-cdk/aws-lambda';
import * as dynamodb from '@aws-cdk/aws-dynamodb';

export class APIStack extends cdk.Stack {

    constructor(scope: cdk.Construct, id: string, props: cdk.StackProps) {
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

        const getUserHandler = new lambda.Function(this, 'GetUserHandler', {
            runtime: lambda.Runtime.PYTHON_3_8,
            handler: 'get_user.handler',
            code: lambda.Code.fromAsset('api'),
            tracing: lambda.Tracing.ACTIVE,
            environment: {
                "USER_TABLE_NAME": userTable.tableName
            }
        });
        userTable.grantReadWriteData(getUserHandler);

        const submitPredictionHandler = new lambda.Function(this, 'SubmitPredictionHandler', {
            runtime: lambda.Runtime.PYTHON_3_8,
            handler: 'submit_prediction.handler',
            code: lambda.Code.fromAsset('api'),
            tracing: lambda.Tracing.ACTIVE,
            environment: {
                "USER_TABLE_NAME": userTable.tableName
            }
        });
        userTable.grantReadWriteData(submitPredictionHandler);

        // -----------------------------
        // ------------ API ------------
        // -----------------------------
        const api = new apigatewayv2.HttpApi(this, 'Api');

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
    }
}
