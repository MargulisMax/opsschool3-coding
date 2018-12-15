import boto3
import click

@click.command()
@click.option('--cidr', help='Define network address range in a format of x.x.x.x/x')
@click.option('--region', help='Enter the region where VPC will be created')
@click.option('--tenancy', help='choose Default for shared host or dedicated for a dedicated host')

def create_vpc(cidr, tenancy, region):
    """ Return VPC description after creation """
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.create_vpc(CidrBlock=cidr, InstanceTenancy=tenancy)
    return response

if __name__ == '__main__':
    create_vpc()
