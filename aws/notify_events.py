__author__ = 'Jeeva Kailasam'
import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr
import sys

regions = ['us-west-1', 'us-west-2', 'us-east-1']
#region = 'us-west-2'
table_name = 'Event-Notify'
dynamodb=boto3.resource('dynamodb','us-west-2')
ddbclient = boto3.client('dynamodb','us-west-2')
table = dynamodb.Table(table_name)



filters = [{'Values': ['instance-stop', 'instance-reboot', 'system-reboot', 'system-maintenance', 'instance-retirement'], 'Name': 'event.code'}]



def addtoddb(Instance_Id,Event_Code,Event_Description,Event_Time,app,Owner,email):
    table.put_item(Item={'InstanceId':Instance_Id,'Region':region,'EventCode':Event_Code, 'EventDescription':Event_Description,\
                         'EventTime':Event_Time,'App':app,'Owner':Owner,'email':email})

def process_tags(ec2,Instance_Id):
    tags = ec2.Instance(Instance_Id).tags
    email = 'NA'
    app = 'NA'
    Owner = 'NA'
    for tag in tags:
        if tag['Key']  == 'Name':
            app = tag['Value']
        elif tag['Key'] == 'eboxapp':
            app = tag['Value']
        if tag['Key']  == 'eboxemail':
            email = tag['Value']
        if tag['Key'] == 'eboxuser':
            Owner = tag['Value']
        elif tag['Key'] == 'Owner':
            Owner = tag['Value']
    return {'app':app, 'email':email, 'Owner':Owner}


def check_events(region):
    #for region in regions:
    ec2 = boto3.resource('ec2',region)
    ec2client=boto3.client('ec2',region)
    InstanceStatuses = ec2client.describe_instance_status(Filters=filters)['InstanceStatuses']

    for InstanceStatus in InstanceStatuses:
        Instance_Id = InstanceStatus['InstanceId']
        TAGS = process_tags(ec2,Instance_Id)
        Events = InstanceStatus['Events']
        for Event in Events:
            Event_Code = Event['Code']
            Event_Description = Event['Description']
            Event_Time = Event['NotBefore'].strftime('%Y-%m-%d %H:%M UTC')
            #Event_Time = Event['NotBefore']
            print ("Instance {0} is Scheduled to {1}".format(Instance_Id,Event_Code))
            print ("Reason: {0}".format(Event_Description))
            print ("Scheduled Time: {0}".format(Event_Time))
            addtoddb(Instance_Id,Event_Code,Event_Description,Event_Time,TAGS['app'],TAGS['Owner'],TAGS['email'])

if __name__ == '__main__':
   for region in regions:
       check_events(region)







### work on it further###