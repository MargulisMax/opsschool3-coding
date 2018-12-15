import boto3
import click

def add_tags(vpc):
    new_tags = vpc.create_tags(
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Boto3-Exercise1'
            }
        ]
    )
    print(new_tags)

@click.command()
@click.option('--cidr', help='Define network address range in a format of x.x.x.x/x')
@click.option('--region', help='Enter the region where VPC will be created')
@click.option('--tenancy', help='choose Default for shared host or dedicated for a dedicated host')

def create_vpc(cidr, tenancy, region):
    ec2 = boto3.client('ec2', region_name=region)
    ec2_resource = boto3.resource('ec2', region_name=region)
    vpc_response = ec2.create_vpc(CidrBlock=cidr, InstanceTenancy=tenancy)
    vpc_id = vpc_response['Vpc']['VpcId']
    vpc = ec2_resource.Vpc(vpc_id)
    vpc.wait_until_exists()
    add_tags(vpc)

if __name__ == '__main__':
    create_vpc()
