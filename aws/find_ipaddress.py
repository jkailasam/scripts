from flask import Flask
from netaddr import IPNetwork, IPAddress
import boto3
import json
import datetime

app = Flask(__name__)
regions = ['us-west-2','us-west-1','us-east-1']
#addr = '10.201.96.50'
#addr = '54.191.126.200'
file = '/tmp/vpc'

def account_region(file,addr):
    with open (file,'r') as vpcs:
        for line in vpcs:
            line = line.strip().split(',')
            subnet = line[3]
            if IPAddress(addr) in IPNetwork(line[3]):
                return [line[0], line[1], line[2]]
                break


def lip_details(ec2c,region,addr):
    filter = [{'Name':'addresses.private-ip-address', 'Values':[addr]}]
    lip = ec2c.describe_network_interfaces(Filters = filter)['NetworkInterfaces']
    json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)
    return json.dumps(lip)


def eip_details(addr):
    filter = [{'Name':'public-ip', 'Values':[addr]}]
    for region in regions:
        ec2c = boto3.client('ec2', region)
        eip = ec2c.describe_addresses(Filters = filter)['Addresses']
        #print('eip is: {}'.format(eip))
        if len(eip)>=1:
            eip.append({'region':region})
            return json.dumps(eip)
            break
    if not eip:
        return '[]'
        #return json.dumps('[]')
        #return json.dumps(eip)

def find_info(addr):
    if addr.startswith('10.200.') or addr.startswith('10.201.') or addr.startswith('100.127.'):
        account_info = account_region(file,addr)
        profile = account_info[0]
        region = account_info[1]
        ec2c = boto3.client('ec2',region)
        return lip_details(ec2c, region, addr)
    else:
        eip = eip_details(addr)
        return eip


@app.route('/ip/<addr>')
def find_details(addr):
    output = find_info(addr)
    if len(output) > 2:
        return output
    else:
        return 'IP Address not found'

if __name__ == '__main__':
    app.run(debug=True)
