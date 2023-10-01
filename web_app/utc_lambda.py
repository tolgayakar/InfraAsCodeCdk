from aws_cdk import core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigateway

def createLambdaToFindUTC(self):

    serverless = _lambda.Function(
        self,
        "functionId2",
        function_name = "UTCFunctionPython",
        runtime = _lambda.Runtime.PYTHON_3_8,
        handler = "utc.lambda_handler",
        code = _lambda.Code.asset("utc_py"),
        timeout = core.Duration.minutes(15),        
        memory_size = 1024,  
    )
    
    version = serverless.add_version("v1")
    version1_alias = _lambda.Alias(
        self,
        "alias1",
        alias_name = "prod",
        version = version
    )

    api_py = apigateway.LambdaRestApi(
        self,
        id = "RestApiForUTC",
        handler = serverless,
        rest_api_name = "UTC",
        proxy=False
                                                              
    )
    items = api_py.root.add_resource("v1")
    items.add_method("GET",apigateway.LambdaIntegration(serverless))
    
    