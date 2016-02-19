__author__ = 'Jeeva Kailasam'
import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr
from boto3.session import Session
import sys
import pprint
import json

regions = ['us-west-1', 'us-west-2', 'us-east-1']
#region = 'us-west-2'
table_name = 'Event-Notify'
dynamodb=boto3.resource('dynamodb','us-west-2')
ddbclient = boto3.client('dynamodb','us-west-2')
table = dynamodb.Table(table_name)

legacy = Session(profile_name='legacy')
dev = Session(profile_name='dev')
prod = Session(profile_name='prod')
account = 'prod'

filters = [{'Values': ['instance-stop', 'instance-reboot', 'system-reboot', 'system-maintenance', 'instance-retirement'], 'Name': 'event.code'}]

def find_existing_events():
    current_events = table.scan()['Items']
    events = {}
    for current_event in current_events:
        events[current_event['InstanceId']] = current_event['EventTime']
    return events

def sendEmail(dictEvent):
    msg = MIMEText(json.dumps(dictEvent, sort_keys=True, indent=4, separators=(',', ': ')))
    msg['Subject'] = 'AWS Maintenance for %s' % dictEvent['Instance ID']
    msg['From'] = 'itcloudeng@netflix.com'
    msg['To'] = 'itcloudeng@netflix.com'
    s = smtplib.SMTP('mailrelay.itp.netflix.net')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()


def addtoddb(Instance_Id,account,Event_Code,Event_Description,Event_Time,app,Owner,email):
    table_item = {'InstanceId':Instance_Id,'Region':region,'EventCode':Event_Code, 'EventDescription':Event_Description,\
                         'EventTime':Event_Time,'App':app,'Owner':Owner,'Email':email,'Account':account}
    table.put_item(Item = table_item)
    return table_item

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


def check_events(aws,region):
    #ec2 = boto3.resource('ec2',region)
    #ec2client=boto3.client('ec2',region)
    ec2 = aws.resource('ec2',region)
    ec2client = aws.client('ec2',region)
    InstanceStatuses = ec2client.describe_instance_status(Filters=filters)['InstanceStatuses']
    existing_events = find_existing_events()

    for InstanceStatus in InstanceStatuses:
        Instance_Id = InstanceStatus['InstanceId']
        TAGS = process_tags(ec2,Instance_Id)
        Events = InstanceStatus['Events']
        for Event in Events:
            Event_Code = Event['Code']
            Event_Description = Event['Description']
            Event_Time = Event['NotBefore'].strftime('%Y-%m-%d')
            print('Checking if this event for {0} is already recorded...'.format(Instance_Id))
            if (existing_events.has_key(Instance_Id) and existing_events[Instance_Id] == Event_Time):
                print("This event is already recorded... Skipping.... \n".format(Instance_Id))
            else:
                #print('Instance ID: {}'.format(Instance_Id))
                #print('Event Code: {}'.format(Event_Code))
                #print('Event Reason: {0}'.format(Event_Description))
                #print('Scheduled Date: {}'.format(Event_Time))
                #print('Account: {0} \nRegion: {1}\n\n'.format(account,region))
                print('Record not found.. adding')
                table_item  = addtoddb(Instance_Id,account,Event_Code,Event_Description,Event_Time,TAGS['app'],TAGS['Owner'],TAGS['email'])
                #pprint.pprint(table_item, width = 1)
                print(json.dumps(table_item, sort_keys=True, indent=5, separators=(',', ':')))
                print('\n\n')



if __name__ == '__main__':
    for account in 'prod','dev','legacy':
        aws = Session(profile_name=account)
        for region in regions:
            check_events(aws,region)











### work on it further###
