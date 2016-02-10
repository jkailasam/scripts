import boto3

autoscaling = boto3.client('autoscaling', 'us-west-2')
ssm = boto3.client('ssm', 'us-west-2')
ASGS=autoscaling.describe_auto_scaling_groups()['AutoScalingGroups']
s3bucket = 'itcloudeng'
s3directory = 'ec2runlogs'
master_script_url = 'https://stash.netflix.com/projects/ET/repos/visine/browse/visine-master-script.sh?raw'
script_option = 'mailbox_add'
logfile = '/var/log/dailyrotate.log'
command = 'curl -s {} | /bin/bash /dev/stdin {} 2>&1 | tee {}'.format(master_script_url,script_option,logfile )

def sendcommand(instanceids):
    response = ssm.send_command(
        InstanceIds = instanceids,
        DocumentName = 'AWS-RunShellScript',
        TimeoutSeconds = 300,
        Parameters = {'commands':[command]},
        OutputS3KeyPrefix = s3directory,
        OutputS3BucketName = s3bucket)
    return response

def find_instances():
    instanceids = []
    for ASG in ASGS:
        asgname = ASG['AutoScalingGroupName']
        if ('visine-imap' in asgname)  or ('visine-smtp' in asgname):
            Instances = ASG['Instances']
            for Instance in Instances:
                instanceids.append(Instance['InstanceId'])
    return instanceids


if __name__ == '__main__':
    instanceids = find_instances()
    print instanceids
    response = sendcommand(instanceids)
    print response


# ssm.list_commands(CommandId='095aacf5-c2f2-492e-82eb-ff1423e3e707')['Commands'][0]['Status']