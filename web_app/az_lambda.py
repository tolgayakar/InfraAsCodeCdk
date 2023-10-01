from aws_cdk import core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigateway

def createLambdaToFindAZ(self):

    serverless = _lambda.Function(
        self,
        "functionId",
        function_name = "AZFunctionPython",
        runtime = _lambda.Runtime.PYTHON_3_8,
        handler = "az.lambda_handler",
        code = _lambda.Code.asset("az_py"),
        timeout = core.Duration.minutes(15),
        memory_size = 1024,  
    )
    
    version = serverless.add_version("v1")
    version1_alias = _lambda.Alias(
        self,
        "alias",
        alias_name = "prod",
        version = version
    )

    api_py = apigateway.LambdaRestApi(
        self,
        id = "RestApiForAZ",
        handler = serverless,
        rest_api_name = "AZ",                                                                                                             
    )

    output = core.CfnOutput(
        self,
        "ApiUrl",
        value = f"{api_py.url}",
        description="Link to access rest api"
    )