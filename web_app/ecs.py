from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns

def createCluster(self,vpc):
    cluster = ecs.Cluster(
        self,
        "ECSCluster",
        vpc = vpc,
        cluster_name = "App"
    )

    cluster.add_capacity(
        "AustoScalingGroup",
        instance_type = ec2.InstanceType("t2.micro"),
        desired_capacity = 2,
        max_capacity = 3
    )

    load_balancer = ecs_patterns.ApplicationLoadBalancedEc2Service(
        self,
        "Ecsservice",
        cluster = cluster,
        memory_reservation_mib = 512,#soft limit
        task_image_options = {
            "image":ecs.ContainerImage.from_registry("tolgayakar/test")
        },
        service_name = "App"          
    )