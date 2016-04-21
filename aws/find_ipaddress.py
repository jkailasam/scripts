from flask import Flask, jsonify, Response
from netaddr import IPNetwork, IPAddress
import boto3
from boto3.session import Session

app = Flask(__name__)
accounts = ['prod','dev','legacy']
regions = ['us-west-2','us-west-1','us-east-1']
file = '/tmp/vpc'


def account_region(file,addr):
    with open (file,'r') as vpcs:
        for line in vpcs:
            line = line.strip().split(',')
            if IPAddress(addr) in IPNetwork(line[3]):
                return [line[0], line[1], line[2]]
                break

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


def lip_details(region, account, addr):
    filter = [{'Name':'addresses.private-ip-address', 'Values':[addr]}]
    ec2c = Session(profile_name=account).client('ec2', region)
    lip = ec2c.describe_network_interfaces(Filters = filter)['NetworkInterfaces']
    if not lip:
        lip = {'Result': 'Local IP address not found'}
    elif len(lip[0].keys()) >= 1:
        lip = lip[0]
        lip['Account_Info'] = [account,region]
    return lip

def eip_details(addr):
    filter = [{'Name': 'addresses.association.public-ip', 'Values': [addr]}]
    for account in accounts:
        for region in regions:
            ec2c = Session(profile_name=account).client('ec2', region)
            eip = ec2c.describe_network_interfaces(Filters = filter)['NetworkInterfaces']
            if not eip:
                eip = {'Result': 'EIP address Not found'}
            elif len(eip[0].keys())>= 1:
                eip = eip[0]
                eip['Account_Info'] = [account,region]
                break
        if len(eip.keys()) >1:
            break
    return eip

def find_info(addr):
    if addr.startswith('10.200.') or addr.startswith('10.201.') or addr.startswith('100.127.'):
        account_info = account_region(file,addr)
        region = account_info[1]
        account = account_info[0]
        return lip_details(region, account, addr)
    else:
        eip = eip_details(addr)
        return eip

@app.route('/ip/<addr>')
def find_details(addr):
    output = find_info(addr)
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)
