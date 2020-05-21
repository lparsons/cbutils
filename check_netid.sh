#!/usr/bin/env sh

file=$1

while read line; do
	echo -ne "$line - "
	out=$(ldapsearch -h ldap.princeton.edu -p 389 -x -b "o=Princeton University,c=US" "(uid=$line)")


	if grep -q "numEntries: 1" <<<$out; then
		echo "FOUND"
	else
		echo "NOT FOUND"
		echo $out
	fi

done < $file
