#!/bin/env bash

FORMAT="${format:-%H:%M:%S}"

handle_buttons(){
	case "$1" in
	    1) ( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null 2>&1 && setsid ./mouse-left-click ) > /dev/null ;;
	    3) ( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null 2>&1 && setsid ./mouse-right-click ) > /dev/null ;;
	esac
}

case "$interval" in
	-3|persist )
		while printf "%($FORMAT)T\n"; sleep 1; do continue; done &
		while read button; do handle_buttons $button; done
		;;
	* )
		printf '%($FORMAT)T\n'
		handle_buttons $BLOCK_BUTTON
esac