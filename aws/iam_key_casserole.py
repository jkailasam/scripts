import os
import argparse
import boto3
from boto3.session import Session

#secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
#access_key = os.environ['AWS_ACCESS_KEY_ID']
#access_token = os.environ['AWS_SESSION_TOKEN']

#iam = boto3.resource('iam')
#iamc = boto3.client('iam')


# Metadata = iamc.list_access_keys(UserName=user.user_name)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARYELLO = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#parser = argparse.ArgumentParser(description='Lists all the iAM acoounts and Accesskeys')
#parser.add_argument('--account', default='prod', choices=['prod','dev','legacy'],help='Account Name')
#args = parser.parse_args()
#profile = args.account



#aws = Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=access_token)
#aws = Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=access_token)

iam = boto3.resource('iam')
iamc = boto3.client('iam')
string = 'LastUsedDate'
users = iam.users.all()


## MAIN FUNCTION
for user in users:
    for key in user.access_keys.all():
        username = user.user_name
        accessid = key.id
        status = key.status
        lastused = iamc.get_access_key_last_used(AccessKeyId=accessid)
        if status == "Active":
            if string in lastused['AccessKeyLastUsed']:
                date = lastused['AccessKeyLastUsed'][string].strftime('%Y-%m-%d %H:%M UTC')
                print("User: {:<35}  Key: {}     Last_Used: {}".format(username,accessid,date))
            else:
                print(bcolors.FAIL + "User: {:<35}  Key: {}     Key_Active_but_Never_Used".format(username,accessid) + bcolors.ENDC)
        else:
            print(bcolors.WARYELLO + "User: {:<35}  Key: {}     Key Not Active".format(username,accessid) + bcolors.ENDC)
