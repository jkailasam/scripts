#!/bin/bash

source ../env/core.sh
COMMANDS_DIR="../commands"
## define the Help message fuction
Help(){
    cat << EOF
${0##*/} v${VERSION}

Syntax:
`basename ${0}` [ options ] | <command> [ options ] zpool/filesystem ...


COMMANDS:
`for C in $COMMANDS_DIR/*.sh; do [ -f "$C" ] && C_NAME="${C##*/}" && printf '  %s\n' "${C_NAME%.*}"; done`

OPTIONS:
  -h, --help        = Print this help and exit
  -V, --version     = Print the version number and exit

MORE HELP:
  All commands accept the -h option; use it for command-specific help.
  Example: ${0##*/} snapshot -h
           ${0##*/} destroy -h

           
EOF
}


case "$1" in
    '-h'|'--help'|'')
        Help;;
    '-v'|'-V'|'--version')
        printf '%s v%s\n' "${0##*/}" "${VERSION}";;
    *)
        CMD="$1"
        if [ -f "${COMMANDS_DIR}/${CMD}.sh" ]; then
            shift
           . "${COMMANDS_DIR}/${CMD}.sh"
        else
            Fatal "'$CMD' is not a valid ${0##*/} command."
        fi
        ;;
esac
