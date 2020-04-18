#!/bin/bash

DIR="/home/user/Desktop/TestBBC/data/"
for FILE in "$DIR"*
do
	echo $FILE
   	nfpcapd -l /home/user/Desktop/TestBBC/data/processed -r $FILE
	nfpcapd
done

cd '/home/user/Desktop/TestBBC/'

echo 'running nfdump'

nfdump -R /home/user/Desktop/TestBBC/data/processed/ > nfDumpOutput.txt

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
python mergeFilesV8.py > mergedFiles.txt

echo "Sorting nfdump output and removing LAN data"
sed -i '/dsldevice.lan./d' ./mergedFiles.txt
sed -i '/ICMP/d' ./mergedFiles.txt
sort -k 3 mergedFiles.txt > nfDumpFinalOutput.txt

echo "Associating unknown/CDN flows with known applications"
python identificationByAssociation.py

echo "Removing files no longer needed"
rm AfterFacebook.txt AfterSpotify.txt AfterTwitter.txt asnOutput.txt ipAddressesPython.txt mergedFiles.txt nfDumpOutput.txt nsOutput.txt sortOutput.txt 
