from aws_cdk import core
from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as codepipeline_actions
from aws_cdk import aws_cloudformation as cloudformation
from aws_cdk import aws_codebuild as codebuild
import json
def pipeline(self):
    
    pipeline = codepipeline.Pipeline(
        self,
        "Pipeline",
        pipeline_name = "ELBPipeline" 
    )
    source_output = codepipeline.Artifact(artifact_name="Artficat")
    
    source_action = codepipeline_actions.GitHubSourceAction(
        action_name="Github_Source",
        output=source_output,
        owner="my-owner",
        repo="my-repo", 
        
        variables_namespace="MyNamespace"
    )
