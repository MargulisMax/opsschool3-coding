import boto3
import click


#def create_igw():
    #response = ec2.create_internet_gateway()
    #return response

@click.command()
@click.option('--region', help='Define network address range in a format of x.x.x.x/x')

def select_active_vpc(region):
    ec2 = boto3.client('ec2', region_name=region)
    get_vpcs = ec2.describe_vpcs()
    for vpcid in get_vpcs['Vpcs']:
        print(vpcid['VpcId'])
    selected_id = input("Select VPC ID: ")


if __name__ == '__main__':
    select_active_vpc()
