# aircrack-ng

 This software does not make part of the analysis tool itself. Instead, this software is only available to collect the data and inserting it in the correct format in the local database.
 
The 'aircrack-ng' folder contains the software for the data collection. In particular, the 'airodump-ng' tool was purposefully customized in order to collect the necessary data and insert it into a local database.

The 'airodump-ng' suite does the following:
* Only probe request messages with a random source MAC address are captured. (Probe requests with a real MAC address can be uniquely identified from its MAC address, and so, there is no relevance in collecting those messages);
* For each probe request, the source MAC address, a footprint, the Information Elements, the RSSID, and the SEQ number are analysed, and stored in the 'InformationElements.db' database.
* Each Information Element (IE) is represented by three fields (IE_ID, IE_length, and IE_value). As some of this IEs are substantly varying by nature (e.g., SSID or DS_Parameter_Set), the entire information of somes IEs is not analyser nor stored in the database. The information considered from each Information Element of each probe request is presented in the 'footprint_ies_considered.csv' file. This is also the information used to generate the device footprints. The data of each IE is stored in hexadecimal format.

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

### Collect data

Having installed this specific version of the 'aircrack-ng' suite, you can collect the probe requests messages by doing the following steps:
1. Check what wireless interfaces you have available on your device (```sudo airmon-ng```). A list of the wireless interfaces is returned.
2. Set the wireless interface in monitor mode (```sudo airmon-ng start <wlan>```).
3. Start sniffing probe request messages(```sudo airodump-ng --background 1 <wlan>```). The 'airodump-ng' will start collecting data and insert it on the 'Information_Elements.db' database.








