# InformationElementsAnalyser

This repository contains a software tool to analyse Information Elements (IEs) from probe request messages.
This tool analyzes the Information Elements of probe requests that are contained in a database, generating data analyses at various levels. 
It can also write/generate a report for each analysis (i.e., each time the tool is run) into a text file.

This tool was used to determine what information should be considered or ignored from the Information Elements of probe request messages, in order to develop a fingerprinting algorithm to uniquely identify mobile devices. More details about this tool and this work are available [here](https://repositorio.iscte-iul.pt/handle/10071/29505).

Besides the software tool, this repository also contains the software for collecting and storing the data in the apropriated format for subsequent analysis by the tool.

***IMPORTANT NOTES:***
* The software will only run under certain conditions (my excuses in advance for the inconvenience):
  * The software is meant to be spefically run on a device with Kali Linux OS installed.
  * Please clone this repository at the '/home/kali/Desktop' folder of your device and not move any file from its original path, otherwise you may compromisse the executability of the software.
 

## informationElementsAnalyser.py

(Falar do objetivo principal deste script, descrever muito sucintamente o que ele faz)

(Dizer que tipo de análise faz/mostra, com bullet points a explicar cada ponto da análise o melhor possível)

(Falar das variaveis de ambiente, explicar quais são e para que servem)

### example

(Dizer que são ficherios de exemplo com dados do Public Dataset dos italianos e que foram usados para fazer a validação da informação a considerar/ignorar para cada Information Element para a footprint e que pode ser usado como exemplo do output gerado pela ferramenta, para se ter uma noção do que ela faz).
    
## aircrack-ng

 This software does not make part of the analysis tool itself. Instead, this software is only available to collect the data and inserting it in the correct format in the local database.
 
The 'aircrack-ng' directory contains the software for the data collection. In particular, the 'airodump-ng' tool was purposefully customized in order to collect the necessary data and insert it into a local database.

The 'airodump-ng' suite does the following:
* Only probe request messages with a random source MAC address are captured. (Probe requests with a real MAC address can be uniquely identified from its MAC address, and so, there is no relevance in collecting those messages);
* For each probe request, the source MAC address, a footprint, the Information Elements, the RSSID, and the SEQ number are analysed, and stored in the 'InformationElements.db' database.
* Each Information Element (IE) is represented by three fields (IE_ID, IE_length, and IE_value). As some of this IEs are substantly varying by nature, the entire information of each IE is not stored in the database. The information stored from each IE of each probe request in the database is presented in the 'ies_data_stored.csv" file. The data of each IE is stored in hexadecimal format.
* The information considered from each Information Element of each probe request used to generate the 'footprint' field is presented in the 'footprint_ies_considered.csv' file.

### Instalation

To install this specific custom-made 'aircrack-ng' version, do the following steps:
1. Uninstall the original aircrack-ng suite from the apt repository (if exists):
```
sudo apt-get remove aircrack-ng
```
3. Install all requirements. You can check the requirements in the official documentation page of aircrack-ng available [here](https://www.aircrack-ng.org/doku.php?id=install_aircrack#installing_aircrack-ng_from_source).
4. Install this specific version of the 'aircrack-ng' suite:
```
cd aircrack-ng-1.7
 autoreconf -i
 ./configure
 make
 sudo make install
 sudo ldconfig
```

***NOTES:***
* This specific aircrack-ng version requires a prior SQLite3 version instead of the latest version of the SQLite3. As so, you may also need to uninstall the original sqlite3 packages from the apt repository and install a prior version of SQLite3. In this case, the version 3.39.0 was installed and used for this specific version of aircrack-ng. You can also install this SQLite3 version by doing following the steps:
  1. Uninstall the latest version of SQLite3 from the apt repository:
  ```
  sudo apt-get remove sqlite3
  ```
  2. Do the following steps:
  ```
  cd sqlite-autoconf-3390000
  ./configure
  make
  sudo make install
  ```
  3. Once this commands suceed, you can check your SQLite3 version:
  ```
  sqlite3 --version
  ```

### Collected data

Having installed this specific version of the 'aircrack-ng' suite, you can collect the probe requests messages by doing the following steps:
1. Check what wireless interfaces you have available on your device (```sudo airmon-ng```). A list of the wireless interfaces is returned.
2. Set the wireless interface in monitor mode (```sudo airmon-ng start <wlan>```).
3. Start sniffing probe request messages(```sudo airodump-ng --background 1 <wlan>```). The 'airodump-ng' will start collecting data and insert it on the 'Information_Elements.db' database.

## DB

This directory contains the database where the collected data is written by the 'airodump-ng' suite. The 'airodump-ng' is has hardcoded the database filepath '/home/kali/Desktop/InformationElementsAnalyser/DB/InformationElements.db' to write the collected data, so please do not change the location of this file in any circunstance.

This database is empty and contains only one table (Information_Elements). The information of each probe request message is stored in a row of this table.

The schema of the Information_Elements table is the following:

CREATE TABLE `Information_Elements` ( \
 `MAC_Address`  text , \
 `Footprint` text, \
 `IE_array` text, \
 `Supp_Rates` text, \
 `Extended_Supp_Rates` text, \
 `DS_Parameter` text, \
 `HT_Capabilities` text, \
 `Extended_Capabilities` text, \
 `VHT_Capabilities` text, \
 `RM_enabled_Capabilities` text, \
 `Interworking` text, \
 `Supp_Operating_Classes` text, \
 `Vendor_1` text, \
 `Vendor_2` text, \
 `Vendor_3` text, \
 `Vendor_4` text, \
 `Timestamp` datetime, \
 `Power` text, \
 `Manufacturer` text, \
 `SEQ` INTEGER \
);








