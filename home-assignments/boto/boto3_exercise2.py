import boto3
import click

def create_and_attach_dhcpopts(ec2, vpc_id):
    new_dhcp_options = ec2.create_dhcp_options(
        dhcpconfigurations=[
            {
                'Key': 'domain-name-servers',
                'Values': [
                    '10.21.0.10',
                    '10.21.2.10',
                ],
            },
        ],
    )
    ec2.associate_dhcp_options(new_dhcp_options['DhcpOptions']['DhcpOptionsId'], vpc_id)

def create_and_attach_igw(ec2, vpc_id):
    new_igw = ec2.create_internet_gateway()
    ec2.attach_internet_gateway(new_igw['InternetGateway']['InternetGatewayId'], vpc_id)

def select_vpc_id(ec2):
    get_vpcs = ec2.describe_vpcs()
    for vpc in get_vpcs['Vpcs']:
        print(vpc['VpcId'])
    selected_id = input("Select VPC ID: ")
    return selected_id

@click.command()
@click.option('--region', help='Enter the region where VPC will be created')

def attach_igw_and_dhcpopts_to_vpc(region):
    ec2 = boto3.client('ec2', region_name=region)
    vpc_id = select_vpc_id(ec2)
    create_and_attach_igw(ec2, vpc_id)
    create_and_attach_dhcpopts(ec2, vpc_id)

if __name__ == '__main__':
    attach_igw_and_dhcpopts_to_vpc()

