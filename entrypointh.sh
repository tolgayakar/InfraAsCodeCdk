#!/bin/sh


cdk bootstrap --require-approval never
cdk deploy --all --require-approval never

