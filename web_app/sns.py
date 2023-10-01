from aws_cdk import core
from aws_cdk import aws_sns as sns
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_cloudwatch_actions as actions
from aws_cdk import aws_sns_subscriptions as subs
import os

def createSNS(self):

    my_topic = sns.Topic(self, 
        "Topic1",
        display_name = "Customer subscription topic",
        topic_name = "TopicforLogs"
    )
    email = os.environ["EMAIL"]
    my_topic.add_subscription(subs.EmailSubscription(email))

    return my_topic