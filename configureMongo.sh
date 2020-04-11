#!/bin/bash

apt install -y mongodb
systemctl enable mongodb

mongo < mongotest.js
sed -i 's/#auth = true/auth = true/g' /etc/mongodb.conf 
read -p "Enter IP address of remote system: " ipv4
sed -i "s/bind_ip = 127.0.0.1/bind_ip = 127.0.0.1,$ipv4/g" /etc/mongodb.conf
