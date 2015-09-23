#!/bin/bash
if [[ $# -ne 2 ]] ; then 
   echo "Usage: $(basename $0) [attach|detach] [instanceid]"
   exit
fi

REGION=us-west-2
InstanceId=$2

TMPFILE=/tmp/tmpfile
#aws ec2 describe-volumes --region us-west-2 --filters Name=attachment.instance-id,Values=$InstanceId | jq -r '.Volumes[].Attachments[]|.VolumeId+","+.Device+","+.InstanceId' > $TMPFILE

case $1 in 
  detach) 
  for i in $(cat $TMPFILE); do 
    VolID=$(echo $i | awk -F, '{print $1}')
    Device=$(echo $i | awk -F, '{print $2}')
    SInstID=$(echo $i | awk -F, '{print $3}')
    echo -e  "$VolID\t$Device\t$SInstID"
    aws ec2 detach-volume --region $REGION --instance-id $InstanceId --volume-id $VolID  --force
  done
esac

