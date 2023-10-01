from aws_cdk import core as cdk
from constructs import Construct
from web_app.vpc import createVPC
from web_app.sns import createSNS
from web_app.cloudtrail import createTrail
from web_app.az_lambda import createLambdaToFindAZ
from web_app.utc_lambda import createLambdaToFindUTC
from web_app.lbasg import createLBASG
from web_app.ecr import createRepositoryForImage
from web_app.ecs import createCluster

class WebAppStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        client = "makeunique"#this is for bucket
        vpc,security_group = createVPC(self)
        #createLambdaToFindAZ(self) "called in the java"
        createLambdaToFindUTC(self)
        createLBASG(self,vpc,security_group)
        alarm_topic = createSNS(self)
        createTrail(self,client,alarm_topic)
        #uri = createRepositoryForImage(self)
        createCluster(self,vpc)
