#!/bin/bash
set -e
# install nfdump

cd /usr/src/
apt-get install libtool -y
apt-get install bison
apt-get install libbz2.dev -y
apt install make gcc flex rrdtool librrd-dev libpcap-dev php librrds-perl libsocket6-perl apache2 -y
wget https://github.com/phaag/nfdump/archive/v1.6.17.tar.gz
tar xzfv v1.6.17.tar.gz
cd nfdump-1.6.17/
sh ./autogen.sh
./configure --enable-nsel --enable-nfprofile --enable-sflow --enable-readpcap --enable-nfpcapd
make
make install
cd /usr/local/lib
ldconfig -v

#install python module
apt install python3-pip -y
pip3 install mysql-connector

#install whois
apt install whois
