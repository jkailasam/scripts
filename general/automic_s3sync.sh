#!/bin/bash
cd /apps/uc4/0800
for i in $(find /apps/uc4/0800 -maxdepth 1 -mtime +90  | awk -F/ '{print $5}'); do   
	aws s3 sync ${i}/ s3://nflx-enterprise-platforms-us-east-1/automicprod_backup/0800/${i}/ && rm -rf $i
done



