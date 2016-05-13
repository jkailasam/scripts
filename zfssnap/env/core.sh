#!/bin/bash
#All the environment variables are functions are defined here
readonly VERSION='1.0.0.beta1'
ZFS='/sbin/zfs'
ZPOOL='/sbin/zpool'
TIME_FORMAT='%Y-%m-%d_%H.%M.%S'
readonly DATE_PATTERN='[2][0][0-9][0-9]-[01][0-9]-[0-3][0-9]_[0-2][0-9].[0-5][0-9].[0-5][0-9]'

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


## Check TTL if it is valid
ValidTTL() {
    TTL=$1
    TTL_TYPE=$(echo -n $TTL | tail -c 1) ## get the last character
    TTL_VALUE=$(echo -n $TTL | sed -e '$s/\(.\{1\}\)$//' -e 's/^0*//')  ## get all but last and remove leading 0
    if ! [[ $TTL_TYPE = m || $TTL_TYPE = h || $TTL_TYPE = d || $TTL_TYPE = w || $TTL_TYPE = M || $TTL_TYPE = y ]] ; then
        return 10
    fi
    # confirm TTL_VALUE is an integer
    re='^[0-9]+$'
    if ! [[ $TTL_VALUE =~ $re ]]; then
        return 10
    fi
}

# Returns 0 if filesystem exists
#FSExists() {
#    FS_LIST=${FS_LIST:-`$ZFS list -H -o name`}#

#    #local i
#    for i in $FS_LIST; do
#        [ "$1" = "$i" ] && return 0
#    done
#    return 1
#}

TrimToPrefix() {
    local snapshot_name="$1"
    # make sure it contains a date
    [ -z "${SnapShotName##*$DATE_PATTERN*}" ] || { RETVAL=''; return 1; }
    local snapshot_prefix="${snapshot_name%$DATE_PATTERN*}"
    if ValidPrefix "$snapshot_prefix"; then
        RETVAL=$snapshot_prefix && return 0
    else
        RETVAL='' && return 1
    fi
}
