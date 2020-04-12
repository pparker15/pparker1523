#!/bin/bash

apt install -y mongodb
systemctl enable mongodb

mongo < mongotest.js
sed -i 's/#auth = true/auth = true/g' /etc/mongodb.conf 
ipv4=$(hostname -I)
sed -i "s/bind_ip = 127.0.0.1/bind_ip = 127.0.0.1,$ipv4/g" /etc/mongodb.conf
