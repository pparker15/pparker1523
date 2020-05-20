# pparker1523
Project Supervisor - Bogdan Ghita

The aim of the project is to identify the applications being used on the network by each user. This is completed using nslookup, an AS mapping tool and by assocation (CDN and unknown flows).

Prerequisites
  A MySQL server
  Apache with PHP
  Ubuntu OS

How to use?
  To recreate the database, use the command 'source > database.sql'. Check that the triggers were created.
  To install dependencies, run ConfigUbuntu.sh, but ensure to run apt get update and apt get upgrade first.
  
  Within the scripts folder, create a folder called 'data' and within the data folder, create a new folder called 'processed'. 
  Put the pcap files in the data folder.
  Check the paths within the 'ProcessData.sh' match where it is installed.
  Update the scripts with MySQL login information.
  
  Put the html folder in the '/var/www' folder.
  
  Execute 'ProcessData.sh' to identify the applications by association.


creative commons license
