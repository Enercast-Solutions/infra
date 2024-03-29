import * as cdk from '@aws-cdk/core';
import * as ecs from '@aws-cdk/aws-ecs';
import * as ecsPatterns from '@aws-cdk/aws-ecs-patterns';

export interface EnergyConsumptionPredStackOutput {
    serviceUrl: string;
}

export class EnergyConsumptionPredStack extends cdk.Stack {
  output: EnergyConsumptionPredStackOutput;

  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const service = new ecsPatterns.ApplicationLoadBalancedFargateService(this, 'EnergyConsumptionPredictionService', {
        memoryLimitMiB: 512,
        cpu: 256,
        taskImageOptions: {
            image: ecs.ContainerImage.fromAsset('prediction-service'),
            containerPort: 5000
        },
        desiredCount: 1,
    });

    this.output = {
        serviceUrl: service.loadBalancer.loadBalancerDnsName
    };
  }
}
