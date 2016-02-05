import boto3

autoscaling = boto3.client('autoscaling', 'us-west-2')
ASGS=autoscaling.describe_auto_scaling_groups()['AutoScalingGroups']

def ssm(instanceid):



for ASG in ASGS:
    asgname = ASG['AutoScalingGroupName']
    if ('visine-imap' in asgname)  or ('visine-smtp' in asgname) :
        Instances = ASG['Instances']
        for Instance in Instances:
            instanceid=Instance['InstanceId']
            print instanceid
