#!/bin/bash
# You are free to run, copy, share and modify this script. ~Public domain.

if [ $UID != 0 ]; then
	echo "You need to run this as root. Try putting 'sudo' in front of the program name."
	exit
fi

echo -n \
"This script removes movact from '/usr/local/bin/'.

Do you want to continue? (Y/n) "

read inp
inp=`echo "$inp" | tr [:upper:] [:lower:]` # To lowercase

if [ "$inp" != "n" ]; then
	echo -n "Removing symbolic links..."
	rm -f /usr/local/bin/movact-terminal && \
	rm -f /usr/local/bin/movact-gtk && \
	rm -f /usr/local/bin/movact-convert && \
	echo \ Done! || echo -e \\nFailure.
else
	echo Aborting.
fi
