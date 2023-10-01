from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_logs as logs

def createVPC(self):

    vpc = ec2.Vpc(
        self,
        "VPCID",
        cidr = "10.0.0.0/16",
        max_azs = 3,
        vpc_name = "CDKVPC",             
    )

    security_group = ec2.SecurityGroup(
        self,
        security_group_name = "CDK-Sec-Group",
        id = "CDK-security-group",
        vpc = vpc,
        allow_all_outbound = True,   
    )

    security_group.add_ingress_rule(ec2.Peer.ipv4("0.0.0.0/0"),ec2.Port.tcp(22))
    security_group.add_ingress_rule(ec2.Peer.ipv4("0.0.0.0/0"),ec2.Port.tcp(443))
    security_group.add_ingress_rule(ec2.Peer.ipv4("0.0.0.0/0"),ec2.Port.tcp(80))

    return vpc,security_group