import boto3

autoscaling = boto3.client('autoscaling', 'us-west-2')
ssm = boto3.client('ssm', 'us-west-2')
ASGS=autoscaling.describe_auto_scaling_groups()['AutoScalingGroups']
s3bucket = 'itcloudeng'
s3directory = 'ec2runlogs'

def sendcommand(instanceid):
    response = ssm.send_command(
        InstanceIds = [instanceid],
        DocumentName = 'AWS-RunShellScript',
        TimeoutSeconds = 300,
        Parameters = {'commands':['date']},
        OutputS3KeyPrefix = s3directory,
        OutputS3BucketName = s3bucket)
    return response

for ASG in ASGS:
    asgname = ASG['AutoScalingGroupName']
    if ('visine-imap' in asgname)  or ('visine-smtp' in asgname):
        Instances = ASG['Instances']
        for Instance in Instances:
            instanceid = Instance['InstanceId']
            print instanceid


if __name__ == '__main__':
    a = sendcommand('i-77983cb0')
    print a


# ssm.list_commands(CommandId='095aacf5-c2f2-492e-82eb-ff1423e3e707')['Commands'][0]['Status']