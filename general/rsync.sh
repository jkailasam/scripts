#!/bin/bash
LOGSDIR=/root/logs

cd /nfs/www
for i in $(cat /root/kj); do
nohup rsync -avh --exclude='no-sync' --exclude='.snapshot' --numeric-ids $i /nfsnew/www/ >${LOGSDIR}/${i}.out 2>${LOGSDIR}/${i}.error &
# nohup rsync -ave “ssh -i keyfile”  --numeric-ids $i system1:/targetdir >${LOGSDIR}/${i}.out 2>${LOGSDIR}/${i}.erro

        while true; do
        sleep 30
        COUNT=$(ps -ef | grep rsync | wc -l)
        [[ $COUNT -le 20 ]] && break
        done
done

### end of script to test the pull request ###
