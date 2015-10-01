echo "AMI started 13:30"
while true; do  
	aws ec2 describe-images --region us-west-2 --image-ids ami-49c6df79 | grep State  | grep pending > /dev/null 2>/dev/null
	if [[ $? -ne 0 ]] ; then  echo "ami creation finished"; date;  exit 
	else  
	sleep 30
	fi 
done
