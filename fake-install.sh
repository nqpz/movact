#!/bin/bash
# You are free to run, copy, share and modify this script. ~Public domain.

if [ $UID != 0 ]; then
	echo "You need to run this as root. Try putting 'sudo' in front of the program name."
	exit
fi

echo -n \
"This script does *not* install movact. It merely creates a symbolic link to
'movact-terminal.py' in '/usr/local/bin/movact-terminal', one to 'movact-gtk.py'
in '/usr/local/bin/movact-gtk' and one to 'movact-convert.py' in
'/usr/local/bin/movact-convert'. This will allow you to run movact like this:

    $ movact-terminal
or:
    $ movact-gtk
and:
    $ movact-convert

This fancy way of \"installing\" movact requires you to place the movact files in
a directory that you do not rename or move, as the symbolic link will fail to
work in such cases.
Note that if you choose to \"install\" movact now using this method, but later
chooses to move the directory that movact resides in, you just have to rerun
this script.


Do you want to continue? (Y/n) "

read inp
inp=`echo "$inp" | tr [:upper:] [:lower:]` # To lowercase

if [ "$inp" != "n" ]; then
	echo -n "Creating symbolic links..."
	ln -fs "`pwd`/movact-terminal.py" /usr/local/bin/movact-terminal && \
	ln -fs "`pwd`/movact-gtk.py" /usr/local/bin/movact-gtk && \
	ln -fs "`pwd`/movact-convert.py" /usr/local/bin/movact-convert && \
	echo \ Done! || echo -e \\nFailure.
	
	echo -n \
"Choose default frontend (what you will get when you run the alias 'movact'):
0. With text only (for use in terminals/consoles)
1. With a graphical user interface (using GTK) (default)
Your choice: "
	read inp
	if [ "$inp" == "0" ]; then
		echo Choosing text interface..
		echo -n Creating symbolic link..
		ln -fs /usr/local/bin/movact-terminal /usr/local/bin/movact && \
		echo \ Done! || echo -e \\nFailure.
	else
		echo Choosing GTK interface..
		echo -n Creating symbolic link..
		ln -fs /usr/local/bin/movact-gtk /usr/local/bin/movact && \
		echo \ Done! || echo -e \\nFailure.
	fi
else
	echo Aborting.
fi
