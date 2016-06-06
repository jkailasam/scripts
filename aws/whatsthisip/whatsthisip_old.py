__author__ = 'Jeeva'

import boto3
import json
import datetime
from boto3.session import Session
from flask import Flask,jsonify,request
from netaddr import IPNetwork, IPAddress
from urllib.request import urlopen

app = Flask(__name__)
accounts = ['prod','dev','legacy']
accounts = ['prod']
regions = ['us-west-2','us-west-1','us-east-1']
file = '/tmp/vpc'

# Fix for the error while serializing the datetime format
json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)

## Find the account and region info for Private IPs
def find_account_region(file,addr):
    with open (file,'r') as vpcs:
        for line in vpcs:
            line = line.strip().split(',')
            if IPAddress(addr) in IPNetwork(line[3]):
                return [line[0], line[1], line[2]]
                break

## Get Security tokens for prod, dev and legacy accounts:
def get_creds(account):
    sts = boto3.client('sts')
    if account == 'dev':
        creds = sts.assume_role(RoleArn='arn:aws:iam::020769165682:role/whatsthisip',
        RoleSessionName="AssumeRoleSession1")['Credentials']
    elif account == 'legacy':
        creds = sts.assume_role(RoleArn='arn:aws:iam::020661041473:role/whatsthisip',
        RoleSessionName="AssumeRoleSession1")['Credentials']
    if account == 'prod':
        aws = Session()
    elif account == 'dev' or account == 'legacy':
        aws = Session(aws_access_key_id = creds['AccessKeyId'],
        aws_secret_access_key = creds['SecretAccessKey'],
        aws_session_token = creds['SessionToken'])
    else:
        print('Invalid Account')
    return aws

## Find private IP address details for etech accoutns
def lip_details(region, account, addr):
    filter = [{'Name':'addresses.private-ip-address', 'Values':[addr]}]
    aws_creds = get_creds(account)
    ec2c = aws_creds.client('ec2', region)
    lip = ec2c.describe_network_interfaces(Filters = filter)['NetworkInterfaces']
    if not lip:
        lip = {'Result': 'Could not find Private IP address'}
    elif len(lip[0].keys()) >= 1:
        lip = lip[0]
        lip['Account_Info'] = [account,region]
    return lip

# Find out eip details for etech accounts
def eip_details(addr):
    filter = [{'Name': 'addresses.association.public-ip', 'Values': [addr]}]
    for account in accounts:
        for region in regions:
            aws_creds = get_creds(account)
            ec2c = aws_creds.client('ec2', region)
            eip = ec2c.describe_network_interfaces(Filters = filter)['NetworkInterfaces']
            if eip:
                eip = eip[0]
                eip['Account_Info'] = [account,region]
                break
        if eip:
            break
    return eip

# get the Private IP / EIP from aws accounts
def get_data_from_aws(addr):
    if addr.startswith('10.200.') or addr.startswith('10.201.') or addr.startswith('100.127.'):
        account_info = find_account_region(file,addr)
        region = account_info[1]
        account = account_info[0]
        return lip_details(region, account, addr)
    else:
        eip = eip_details(addr)
        return eip

# get the IP from go/locate
def get_Data_from_Locate(addr):
    InstanceData = json.loads(urlopen('http://locate.test.netflix.net/api/v1/locate/'+addr).read().decode('utf-8'))
    return InstanceData

# Get the instance details for hte ip address range
def get_bulk_data_from_aws(addr):
    AllInstances = []
    for account in accounts:
        for region in regions:
            aws_creds = get_creds(account)
            ec2c = aws_creds.client('ec2', region)
            filter=[{'Name': 'private-ip-address', 'Values': [addr]}]
            responses = ec2c.describe_instances(Filters = filter, MaxResults=200)
            AllInstances.extend(responses['Reservations'])
            while responses.get('NextToken', None) is not None:
                responses = ec2c.describe_instances(Filters = filter, MaxResults=200, NextToken=responses['NextToken'])
                AllInstances.extend(responses['Reservations'])
            print('Found {} instances in {} region'.format(len(AllInstances),region))
    return AllInstances

def format_InstantData(InstanceData):
    if request.args.get('pretty') == 'no':
        return json.dumps(InstanceData)
    else:
        return jsonify(InstanceData)


@app.route('/<addr>' , methods=['GET'])
def Return_ADDR_Info(addr, pretty='yes'):
    InstanceData = get_Data_from_Locate(addr)
    if InstanceData:
        return format_InstantData(InstanceData[0])
    else:
        InstanceData = get_data_from_aws(addr)
        if InstanceData:
            return format_InstantData(InstanceData)
        else:
            return 'Could not find matching EIP address'

@app.route('/bulk/<addr>' , methods=['GET'])
def Return_Bulk_ADDR_Info(addr, pretty = 'yes'):
    InstanceData = get_bulk_data_from_aws(addr)
    if InstanceData:
        InstanceData_dict = {'Instances': InstanceData}
        return format_InstantData(InstanceData_dict)
    else:
        return 'Could not find matching IP address range'

@app.errorhandler(404)
def usage(error):
    return """Usage: GET https://whatsthisip.itp.netflix.net/[ip]?[pretty=no] <br>
    Usage: GET https://whatsthisip.itp.netflix.net/bulk/[ip]?[pretty=no]\n"""


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080)
