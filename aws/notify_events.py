__author__ = 'Jeeva Kailasam'

import boto3
import boto.ec2
import sys

regions = ['us-west-1', 'us-west-2', 'us-east-1']
for region in regions:
    ec2 = boto3.resource('ec2',region)
    conn = boto.ec2.connect_to_region(region)
    client=boto3.client('ec2',region)




