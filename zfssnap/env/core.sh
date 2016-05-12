#!/bin/bash
#All the environment variables are functions are defined here
readonly VERSION='1.0.0.beta1'
ZFS='/sbin/zfs'
ZPOOL='/sbin/zpool'


## HELPER FUNCTIONS
Err() {
    printf '%s\n' "ERROR: $*" >&2
}

Fatal() {
    printf '%s\n' "FATAL: $*" >&2
    exit 1
}

Info() {
    printf '%s\n' "INFO: $*" >&2
}

Warn() {
    printf '%s\n' "WARNING: $*" >&2
}

ValidTTL() {
    TTL=$1
    #Find the last character
    TTL_TYPE=$(echo -n $TTL | tail -c 1)
    #get all characters but last and remove all the leading 0 if any
    #TTL_VALUE=$(echo -n $TTL | head -c -1|sed 's/^0*//')
    TTL_VALUE=$(echo -n $TTL | sed -e '$s/\(.\{1\}\)$//' -e 's/^0*//')
    if ! [[ $TTL_TYPE = m || $TTL_TYPE = h || $TTL_TYPE = d || $TTL_TYPE = w || $TTL_TYPE = M || $TTL_TYPE = y ]] ; then
        return 10
    fi
    # confirm TTL_VALUE is an integer
    re='^[0-9]+$'
    if ! [[ $TTL_VALUE =~ $re ]]; then
        return 10
    fi

}
