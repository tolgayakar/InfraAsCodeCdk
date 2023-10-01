from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_iam as iam
from aws_cdk import core


def createLBASG(self,vpc,security_group):
    #DOES NOT WORK ALL FOR TEMPLATE ISSUES
    userdata = ec2.UserData.for_linux(shebang="#!/bin/bash -xe")
    userdata.add_commands(
        "yum update -y",
        "yum install httpd -y",
        "service httpd start",
        "chkconfig httpd on",
        "cd /var/www/html",
        'echo "<html><h1>This is WebServer 01</h1></html>" > index.html'
    )

    amazon_linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
        edition=ec2.AmazonLinuxEdition.STANDARD,
        virtualization=ec2.AmazonLinuxVirt.HVM,
        storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
    )

    test_ami = ec2.LookupMachineImage(name="testami") ###DOES NOT WORK

    lb = elbv2.ApplicationLoadBalancer(
        self,
        "ALBID",
        vpc=vpc,
        internet_facing=True,
        load_balancer_name="ALB",       
    )
    lb.connections.allow_from_any_ipv4(
        ec2.Port.tcp(80)
       
    )
    lb.connections.allow_from_any_ipv4(
        ec2.Port.tcp(22)
    )
    
    listener = lb.add_listener(
        "Listener",
        port=80,
        open=True
    )
    
    #Webserver role
    web_server_role = iam.Role(
        self,
        "WebServiceRoleId",
        assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
        managed_policies=[
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
            ),
            ]
    )
    
    asg =   autoscaling.AutoScalingGroup(
        self,
        "ASG",
        instance_type= ec2.InstanceType(instance_type_identifier="t2.micro"),
        machine_image=amazon_linux_ami,
        vpc=vpc,
        role = web_server_role,
        security_group=security_group,
        user_data=userdata,
        min_capacity=2,
        desired_capacity=2,
        max_capacity=3,
    )
    #allow asg security group receive traffic from ALB
    asg.connections.allow_from(lb,ec2.Port.tcp(80))

    listener.add_targets(
        "ApplicationFleet",
        port=80,
        targets=[asg]
    )