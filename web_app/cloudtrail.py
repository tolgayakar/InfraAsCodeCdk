from aws_cdk import aws_cloudtrail as cloudtrail
from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_cloudwatch_actions as actions
from aws_cdk import aws_logs as logs

def createTrail(self,client,alarm_topic):

    log_cloud = logs.LogGroup(
        self,
        "LogsForCloudtrail",
        log_group_name = "Log-Group1",
        retention = logs.RetentionDays.INFINITE
    )

    bucket = s3.Bucket(
        self,
        "Privates",
        bucket_name = f"private-{client}-cloudtraillogs",
        versioned = False,
        public_read_access = False,
        encryption = s3.BucketEncryption.S3_MANAGED,
        removal_policy = core.RemovalPolicy.DESTROY                                                                    
    )

    trail = cloudtrail.Trail(
        self,
        "CloudTrail",
        send_to_cloud_watch_logs = True,
        trail_name = "LogTrail",
        bucket = bucket,
        cloud_watch_log_group = log_cloud,
        sns_topic = alarm_topic,                        
    )

    metricFilters = [
    {
        "metric_name": 'ConsoleLogin',
        "pattern": '$.eventName = "ConsoleLogin"'
    },
    {
        "metric_name": 'FailedConsoleLogin',
        "pattern": '$.eventName = "ConsoleLogin" && $.errorMessage = "Failed authentication"'
    },
    {
        "metric_name": 'EC2Created',
        "pattern": '$.eventName = "RunInstances"'
    },
    {
        "metric_name": 'EC2Resized',
        "pattern": '$.eventName = "ModifyInstanceAttribute" && $.requestParameters.instanceType.value = *'
    },
    {
        "metric_name": 'EC2Terminated',
        "pattern": '$.eventName = "TerminateInstances"'
    },
    {
        "metric_name": 'DefaultVPCChanges',
        "pattern": '$.eventName = "ModifyVpcAttribute"'
    },
    {
        "metric_name": 'VPCCreated',
        "pattern" : '$.eventName = "CreateVpc"'
    },
    {
        "metric_name": 'NewUserCreated',
        "pattern": '$.eventName = "CreateUser"'
    },
    {
        "metric_name": 'NewPolicyCreated',
        "pattern": '$.eventName = "CreatePolicy"'
    },
    {
        "metric_name": 'PolicyChanged',
        "pattern": '$.eventName = "CreatePolicyVersion"'
    },
    {
        "metric_name": 'BucketCreated',
        "pattern": '$.eventName = "CreateBucket"'
    },
    {
        "metric_name": "PublicBucket",
        "pattern": '$.eventName = "PutBucketPublicAccessBlock" && $.requestParameters.PublicAccessBlockConfiguration.RestrictPublicBuckets IS FALSE && $.requestParameters.PublicAccessBlockConfiguration.BlockPublicPolicy IS FALSE && $.requestParameters.PublicAccessBlockConfiguration.BlockPublicAcls IS FALSE &&  $.requestParameters.PublicAccessBlockConfiguration.IgnorePublicAcls IS FALSE'
    },
    {
        "metric_name": "PasswordResets",
        "pattern": '$.eventName = "ResetUserPassword"'
    },
    {
        "metric_name": "APIKeyGenerated",
        "pattern": '$.eventName = "CreateApiKey"'
    },
    {
        "metric_name": "DeleteAPIKey",
        "pattern": '$.eventName = "DeleteApiKey"'
    },
    ]

    for metricFilter in metricFilters:
        metric_filter_logs = logs.MetricFilter(
            self,
            metricFilter["metric_name"],
            log_group = log_cloud,
            metric_namespace = "SecurityMetrics",
            metric_name = metricFilter["metric_name"],
            filter_pattern = logs.JsonPattern(metricFilter["pattern"])
        )

        logs_metric_alarm = cloudwatch.Alarm(
            self,
            metricFilter["metric_name"] + "Alarm",
            metric = metric_filter_logs.metric(),
            actions_enabled = True,
            evaluation_periods = 1,
            threshold = 1
        )
        logs_metric_alarm.add_alarm_action(actions.SnsAction(alarm_topic))




