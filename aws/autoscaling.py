import boto3
import time
from six.moves import urllib

autoscaling = boto3.client('autoscaling', 'us-west-2')
ssm = boto3.client('ssm', 'us-west-2')
ASGS=autoscaling.describe_auto_scaling_groups()['AutoScalingGroups']
s3bucket = 'nflx-itp-assets-internal'
s3directory = 'ec2runlogs'
s3prefix = 'https://s3-us-west-2.amazonaws.com'
s3suffix = 'awsrunShellScript/0.aws%3ArunShellScript/'
master_script_url = 'https://stash.netflix.com/projects/ET/repos/visine/browse/visine-master-script.sh?raw'
script_option = 'mailbox_add'
logfile = '/var/log/visine-add-mailbox.log'
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
    print('\nmailbox will be added in the {0} instances'.format(instanceids))
    response = sendcommand(instanceids)
    CommandId = response['Command']['CommandId']
    print("\nCommand Submitted. Command response is: {0}".format(response))
    print('\nCommandId is: {0}'.format(CommandId))

    time.sleep(5)
    for instanceid in instanceids:
    	print('\n\nProcessing Logs for instance: {0}'.format(instanceid))
        print('Detaild output and errlog for this instance can be found from the following URL:')
        print("https://console.aws.amazon.com/s3/home?region=us-west-2#&bucket={0}&prefix={1}/{2}/{3}/{4}".format(s3bucket,s3directory,CommandId,instanceid,s3suffix))
        print('\n*** CMD Output Log for instance {0}: '.format(instanceid))
        url = s3prefix+'/'+s3bucket+'/'+s3directory+'/'+CommandId+'/'+instanceid+'/'+s3suffix+'stdout'
        stdout = urllib.request.urlopen(url)
        print(stdout.read())
        print('*** End of Output Log for Instance {0}\n\n'.format(instanceid))
