import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class InfrastructureStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The primary single-table design DynamoDB table for AnnaSetu
    const table = new dynamodb.Table(this, 'AnnaSetuStateTable', {
      tableName: 'AnnaSetuStateTable',
      partitionKey: { name: 'PK', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'SK', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY, // For hackathon purposes
    });

    // S3 Bucket for event history / history archiving
    const bucket = new s3.Bucket(this, 'AnnaSetuEventArchive', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    // Output the names so backend knows them
    new cdk.CfnOutput(this, 'DynamoDBTableName', { value: table.tableName });
    new cdk.CfnOutput(this, 'S3BucketName', { value: bucket.bucketName });
  }
}
