__author__ = 'Jeeva Kailasam'
import datetime
import boto3
import boto.ec2
import sys

regions = ['us-west-1', 'us-west-2', 'us-east-1']
region = 'us-west-2'
ec2 = boto3.resource('ec2',region)
conn = boto.ec2.connect_to_region(region)
client=boto3.client('ec2',region)


filters = [{'Values': ['instance-stop', 'instance-reboot', 'system-reboot', 'system-maintenance', 'instance-retirement'], 'Name': 'event.code'}]

InstanceStatuses = client.describe_instance_status(Filters=filters)['InstanceStatuses']

for InstanceStatus in InstanceStatuses:
    instance_id = InstanceStatus['InstanceId']
    Events = InstanceStatus['Events']
    for Event in Events:
        Event_Code = Event['Code']
        Event_Descrition = Event['Description']
        Event_Time = Event['NotBefore'].strftime('%a %Y-%m-%d %H:%M UTC')
        print "Instance {0} is Scheduled to {1}.".format(instance_id,Event_Code)
        print "Reason: {0}".format(Event_Descrition)
        print "Scheduled Time: {0}".format(Event_Time)








