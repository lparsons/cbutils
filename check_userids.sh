#!/usr/bin/env sh

file=$1

while read line; do
        out=$(ldapsearch -h ldap.princeton.edu -p 389 -x -b "o=Princeton University,c=US" "(uid=$line)")


        if grep -q "numEntries: 1" <<<$out; then
                echo "$line\tFOUND"
                #echo $out
        else
                echo "$line\tNOT FOUND"
                #echo $out
        fi

done < $file

