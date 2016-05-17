#!/bin/bash
#All the environment variables are functions are defined here
readonly VERSION='0.1.0'
ZFS='/sbin/zfs'
ZPOOL='/sbin/zpool'
TIME_FORMAT='%Y-%m-%d_%H.%M.%S'
readonly DATE_PATTERN='[2][0][0-9][0-9]-[01][0-9]-[0-3][0-9]_[0-2][0-9].[0-5][0-9].[0-5][0-9]'

## HELPER FUNCTIONS
Err() {
    printf '%s\n' "$(date +'%b %d  %X') ERROR:  $*" >&2
}

Fatal() {
    printf '%s\n' "$(date +'%b %d  %X') FATAL:  $*" >&2
    exit 1
}

Info() {
    printf '%s\n' "$(date +'%b %d  %X') INFO:  $*" >&2
}

Warn() {
    printf '%s\n' "$(date +'%b %d  %X') WARNING: $*" >&2
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

## Returns 0 if filesystem exists
FSExists() {
    FS_LIST=${FS_LIST:-`$ZFS list -H -o name`}
    #local i
    for i in $FS_LIST; do
        [ "$1" = "$i" ] && return 0
    done
    return 1
}

IsSnapshot() {
    case "$1" in
        [!@]*@*[!@]) return 0;;
        *) return 1;;
    esac
}

TrimToFileSystem() {
    local snapshot="$1"
    local file_system="${snapshot%%@*}"

    if FSExists "$file_system"; then
        RETVAL=$file_system && return 0
    else
        RETVAL='' && return 1
    fi
}


RM_SNAPSHOTS(){
    if IsSnapshot "$1"; then
        local zfs_destroy="$ZFS destroy $*"

        if ! [[ $DRY_RUN = true ]]; then
            if $zfs_destroy >&2; then
                echo "$(date +'%b %d  %X') $zfs_destroy .... DONE"
                #printf '%s ... DONE\n' "$zfs_destroy"
            else
                echo "$(date +'%b %d  %X') $zfs_destroy .... FAIL"
                #printf '%s ... FAIL\n' "$zfs_destroy"
            fi
        else
            #printf '%s\n' "$zfs_destroy"
            echo "$(date +'%b %d  %X') $zfs_destroy"
        fi
    else
        Fatal 'Trying to delete ZFS pool or filesystem? WTF?' \
              'This is bug, and we definitely do not want that.' \
              'Please report it to https://github.com/zfsnap/zfsnap/issues' \
              'Do not panic, as nothing was deleted. :-)'
    fi
}
