import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import * as apprunner from '@aws-cdk/aws-apprunner-alpha';
import * as ecr_assets from 'aws-cdk-lib/aws-ecr-assets';
import * as iam from 'aws-cdk-lib/aws-iam';

export class InfrastructureStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // 1. Storage
    const table = new dynamodb.Table(this, 'AnnaSetuStateTable', {
      tableName: 'AnnaSetuStateTable',
      partitionKey: { name: 'PK', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'SK', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY, 
    });

    const archiveBucket = new s3.Bucket(this, 'AnnaSetuEventArchive', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      encryption: s3.BucketEncryption.S3_MANAGED,
    });

    // 2. Queueing & EventBridge
    const dlq = new sqs.Queue(this, 'WorkflowDLQ', {
      retentionPeriod: cdk.Duration.days(14),
    });
    const workflowQueue = new sqs.Queue(this, 'WorkflowQueue', {
      visibilityTimeout: cdk.Duration.seconds(300),
      deadLetterQueue: { queue: dlq, maxReceiveCount: 3 }
    });

    const eventBus = new events.EventBus(this, 'AnnaSetuBus', {
      eventBusName: 'AnnaSetuOperationsBus'
    });
    
    // Route domain events to workflow queue
    new events.Rule(this, 'WorkflowRule', {
      eventBus,
      eventPattern: { source: ['annasetu.operations'] },
      targets: [new targets.SqsQueue(workflowQueue)]
    });

    // 3. Auth
    const userPool = new cognito.UserPool(this, 'AnnaSetuUsers', {
      selfSignUpEnabled: false,
      signInAliases: { email: true },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
    
    // 4. API Compute (App Runner)
    // Note: To successfully deploy, Docker daemon must be running or we use asset path.
    // For this submission package, we define the AppRunner service using a local asset.
    const imageAsset = new ecr_assets.DockerImageAsset(this, 'BackendImage', {
      directory: '../backend', 
    });

    const appRunnerRole = new iam.Role(this, 'AppRunnerInstanceRole', {
      assumedBy: new iam.ServicePrincipal('tasks.apprunner.amazonaws.com')
    });

    const apiService = new apprunner.Service(this, 'AnnaSetuAPI', {
      source: apprunner.Source.fromAsset({
        imageConfiguration: { port: 8000 },
        asset: imageAsset
      }),
      instanceRole: appRunnerRole,
    });

    table.grantReadWriteData(appRunnerRole);
    archiveBucket.grantReadWrite(appRunnerRole);
    workflowQueue.grantConsumeMessages(appRunnerRole);
    eventBus.grantPutEventsTo(appRunnerRole);

    // Bedrock Access
    appRunnerRole.addToPrincipalPolicy(new iam.PolicyStatement({
      actions: ['bedrock:InvokeModel'],
      resources: ['*']
    }));

    // 5. Frontend Hosting
    const frontendBucket = new s3.Bucket(this, 'AnnaSetuFrontend', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
    });

    /*
    const distribution = new cloudfront.Distribution(this, 'FrontendDistribution', {
      defaultBehavior: {
        origin: new origins.S3Origin(frontendBucket),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
      },
      defaultRootObject: 'index.html',
      errorResponses: [{ httpStatus: 404, responsePagePath: '/index.html' }]
    });

    // We deploy the local dist output to the S3 bucket
    new s3deploy.BucketDeployment(this, 'DeployFrontend', {
      sources: [s3deploy.Source.asset('../frontend/dist')],
      destinationBucket: frontendBucket,
      distribution,
    });
    */

    // 6. Outputs
    new cdk.CfnOutput(this, 'DynamoDBTableName', { value: table.tableName });
    new cdk.CfnOutput(this, 'S3BucketName', { value: archiveBucket.bucketName });
    new cdk.CfnOutput(this, 'ApiUrl', { value: apiService.serviceUrl });
    // new cdk.CfnOutput(this, 'FrontendUrl', { value: distribution.domainName });
    new cdk.CfnOutput(this, 'UserPoolId', { value: userPool.userPoolId });
  }
}
