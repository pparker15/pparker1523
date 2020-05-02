cd /home/user/Desktop/TestBBC

grep 2020-04-08 nfDump.txt > newOutput.txt
sed -i 's/192.168.1.3/192.168.1.50/g' newOutput.txt 

grep 2020-04-09 nfDump.txt >> newOutput.txt
sed -i 's/192.168.1.3/192.168.1.51/g' newOutput.txt 
sed -i 's/2020-04-09/2020-04-08/g' newOutput.txt 

grep 2020-04-10 nfDump.txt >> newOutput.txt
sed -i 's/192.168.1.3/192.168.1.52/g' newOutput.txt 
sed -i 's/2020-04-10/2020-04-08/g' newOutput.txt 

grep 2020-04-11 nfDump.txt >> newOutput.txt
sed -i 's/192.168.1.3/192.168.1.53/g' newOutput.txt 
sed -i 's/2020-04-11/2020-04-08/g' newOutput.txt 

grep 2020-04-12 nfDump.txt >> newOutput.txt
sed -i 's/192.168.1.3/192.168.1.54/g' newOutput.txt 
sed -i 's/2020-04-12/2020-04-08/g' newOutput.txt 

grep 2020-04-13 nfDump.txt >> newOutput.txt
sed -i 's/192.168.1.3/192.168.1.55/g' newOutput.txt 
sed -i 's/2020-04-13/2020-04-08/g' newOutput.txt 

grep 2020-04-14 nfDump.txt >> newOutput.txt
sed -i 's/192.168.1.3/192.168.1.56/g' newOutput.txt 
sed -i 's/2020-04-14/2020-04-08/g' newOutput.txt 

grep 2020-04-15 nfDump.txt >> newOutput.txt
sed -i 's/192.168.1.3/192.168.1.57/g' newOutput.txt 
sed -i 's/2020-04-15/2020-04-08/g' newOutput.txt


sort -k 2 newOutput.txt > nfDumpOutput5.txt
