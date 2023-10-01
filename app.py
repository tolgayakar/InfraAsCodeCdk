#!/usr/bin/env python3
import os

from aws_cdk import core

from web_app.web_app_stack import WebAppStack
import os

app = core.App()
#account_id = ""
account_id = os.environ["ACCOUNT_ID"]
region = os.environ["REGION"]
env = core.Environment(account = account_id,region = region)
WebAppStack(app, "WebAppStack", env = env)

app.synth()
