#!/bin/bash

DIR="/home/user/Desktop/categoryTest/data/"
for FILE in "$DIR"*
do
	echo $FILE
   	nfpcapd -l /home/user/Desktop/categoryTest/data/processed -r $FILE
	nfpcapd
done

cd '/home/user/Desktop/categoryTest/'

echo 'running nfdump'

nfdump -R /home/user/Desktop/categoryTest/data/processed/ > nfDumpToSort.txt

echo "Sorting nfdump output"
sort -k 2 nfDumpToSort.txt > nfDumpOutput.txt


#create file for python to put text into
echo > ipAddressesPython.txt

echo 'Extracting IP addresses'
python extractIPs.py

echo 'Sorting IP addresses'
sort ipAddressesPython.txt | uniq > sortOutput.txt

echo 'Starting nslookup'
nslookup < sortOutput.txt > nsOutput.txt

echo 'Getting name from AS'
netcat whois.cymru.com 43 < sortOutput.txt | sort -n > asnOutput.txt

echo 'replacing IP addresses'
python mergeFilesV8.py
