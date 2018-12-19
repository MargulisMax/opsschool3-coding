import boto3
import click

REGION = 'us-east-1'
AVAIL_ZONE = 'us-east-1c'
DEFAULT_ROUTES = {
    'Private_1c':'0.0.0.0/0',
    'Public_1c':'0.0.0.0/0'
}
SUBNETS = {
    'Private_1c':'10.21.0.0/24',
    'Public_1c':'10.21.2.0/24'
}

def get_subnet_id_by_tag(ec2, tag_name):
    subnet = ec2.describe_subnets(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    tag_name,
                ],
            }
        ]
    )
    return subnet['Subnets'][0]['SubnetId']

def associate_route_table_to_subnet(ec2, route_table_id, subnet_id):
    ec2.associate_route_table(
        RouteTableId=route_table_id,
        SubnetId=subnet_id,
    )

def create_new_route(ec2, cidr_block, gateway_id, route_table_id):
    ec2.create_route(
        DestinationCidrBlock=cidr_block,
        GatewayId=gateway_id,
        RouteTableId=route_table_id,
    )

def create_route_table(ec2, vpc_id, igw, natgw):
    for route_name in DEFAULT_ROUTES:
        new_route_table = ec2.create_route_table(
            VpcId=vpc_id,
        )
        create_tags(ec2, new_route_table['RouteTable']['RouteTableId'], route_name)
        if route_name == 'Private_1c':
            create_new_route(ec2, DEFAULT_ROUTES[route_name], natgw, new_route_table['RouteTable']['RouteTableId'])
            subnet_id = get_subnet_id_by_tag(ec2, route_name)
            associate_route_table_to_subnet(ec2, new_route_table['RouteTable']['RouteTableId'], subnet_id)
        else:
            create_new_route(ec2, DEFAULT_ROUTES[route_name], igw, new_route_table['RouteTable']['RouteTableId'])
            subnet_id = get_subnet_id_by_tag(ec2, route_name)
            associate_route_table_to_subnet(ec2, new_route_table['RouteTable']['RouteTableId'], subnet_id)


def allocate_eip(ec2):
    new_eip = ec2.allocate_address(
        Domain='vpc',
    )
    return new_eip

def create_nat_gateway(ec2, public_subnet):
    nat_gw_eip = allocate_eip(ec2)
    new_nat_gw = ec2.create_nat_gateway(
        AllocationId=nat_gw_eip['AllocationId'],
        SubnetId=public_subnet,
    )
    return new_nat_gw['NatGateway']['NatGatewayId']

def create_tags(ec2, resource, resource_name):
    new_tag = ec2.create_tags(
       Resources=[
           resource,
       ],
       Tags=[
           {
               'key': 'Name',
               'value': resource_name
           },
       ]
    )


def create_subnets(ec2, vpc_id):
    for net_name in SUBNETS:
        new_subnet = ec2.create_subnet(
            AvailabilityZone=AVAIL_ZONE,
            CidrBlock=SUBNETS[net_name],
            VpcId=vpc_id,
        )
        create_tags(ec2, new_subnet['Subnet']['SubnetId'], net_name)

@click.command()
@click.option('--vpc', help='Enter the Vpc ID')
@click.option('--igw', help='Enter the Internet Gateway ID')

def create_aws_network(vpc, igw):
    ec2 = boto3.client('ec2', region_name=REGION)
    """ :type : pyboto3.ec2 """
    new_subnets = create_subnets(ec2, vpc)
    new_nat_gw = create_nat_gateway(ec2, get_subnet_id_by_tag(ec2, 'Public_1c'))
    create_route_table(ec2, vpc, igw, new_nat_gw)



if __name__ == '__main__':
    create_aws_network()
