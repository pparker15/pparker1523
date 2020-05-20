#!/bin/bash

DIR="/home/user/Desktop/scripts/data/"
for FILE in "$DIR"*
do
	echo $FILE
  	nfpcapd -l /home/user/Desktop/scripts/data/processed -r $FILE
	nfpcapd
done

cd '/home/user/Desktop/scripts/'

echo 'running nfdump'

nfdump -R /home/user/Desktop/scripts/data/processed/ > nfDump.txt

sort -k 2 nfDump.txt > nfDumpOutput.txt

#create file for python to put text into
echo > ipAddressesPython.txt

echo 'Extracting IP addresses'
python extractIPAddresses.py

echo 'Sorting IP addresses'
sort ipAddressesPython.txt | uniq > sortOutput.txt

echo 'Starting nslookup'
nslookup < sortOutput.txt > nsOutput.txt

echo 'Getting name from AS'
netcat whois.cymru.com 43 < sortOutput.txt | sort -n > asnOutput.txt

echo 'Adding data to name_table'
python addNames.py

echo 'replacing IP addresses'
python replaceIPaddresses.py

echo "Associating CDN flows with known applications"
python IdentificationByAssociation.py

echo "Completed"
