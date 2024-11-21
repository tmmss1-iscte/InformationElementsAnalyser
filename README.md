# InformationElementsAnalyser

This repository contains a software tool to analyse Information Elements (IEs) from probe request messages.
This tool analyzes the Information Elements of probe requests that are contained in a database, generating data analyses at various levels. 
It can also write/generate a report for each analysis (i.e., each time the tool is run) into a text file.

This tool was used for determing a fingerprinting algorithm for a master's dissertation regarding this scope, and is
available at 'https://repositorio.iscte-iul.pt/handle/10071/29505'.

This repository also contains software for the data collection (aircrack-ng) and a database (InformationElements.db) to store it in the correct format 
for subsequent analysis by the tool.

***IMPORTANT NOTES:***
* The software will only run under certain conditions (my excuses in advance for the inconvenience):
  * The software is meant to be spefically run on a device with Kali Linux OS (version indenpendent) installed.
  * Please clone this repository in the /home/kali/Desktop folder of your device. Despite having a 'env_variables.py' file where you can specify the location of the database for the input data, the 'airodump-ng' suite has the path '/home/kali/Desktop/InformationElementsAnalyser/DB/InformationElements.db' hardcoded as the input database where the data will be written. Therefore, do not move any file from its original path, otherwise you may compromisse the executability of the software.
    
## aircrack-ng

The 'aircrack-ng' directory contains the software for the data collection. In particular, the 'airodump-ng' tool was purposefully customized in order to collect the necessary data and insert it into a local database.
Therefore, the 'airodump-ng' suite does the following:
* Only probe request messages with a random source MAC address are captured. (Probe requests with a real MAC address can be uniquely identified from its MAC address, and so, there is no relevance in collecting those messages);
* For each probe request, the source MAC address, a footprint, all its Information Elements, the RSSID, and the SEQ number are analysed, and stored in the '/DB/InformationElements.db' database.
* (Falar da informação utilizada/considerada para a geração das footprints)
* (Falar da informação que é considerada/armazenada em hexadecimal para cada InformationElement na base de dados)

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
* This specific aircrack-ng version requires a prior SQLite3 version instead of the latest version of the SQLite3. As so, you may also need to uninstall the original sqlite3 packages from the apt repository just like in step 1) and install a prior version of SQLite3. In this case, the version 3.39.0 was installed and used for this specific version of aircrack-ng. You can also install this SQLite3 version by doing following the steps:
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

## DB

This directory contains the database where the collected data is written by the 'airodump-ng' suite. The 'airodump-ng' is has hardcoded the database filepath '/home/kali/Desktop/InformationElementsAnalyser/DB/InformationElements.db' to write the collected data. 

This database is empty and contains only one table (Information_Elements), which its schema is presented in the 'InformationElements_schema.txt' file.


## informationElementsAnalyser.py

(Falar do objetivo principal deste script, descrever muito sucintamente o que ele faz)

(Dizer que tipo de análise faz/mostra, com bullet points a explicar cada ponto da análise o melhor possível)

(Falar das variaveis de ambiente, explicar quais são e para que servem)

### example.py

(Dizer que são ficherios de exemplo com dados do Public Dataset dos italianos e que foram usados para fazer a validação da informação a considerar/ignorar para cada Information Element para a footprint e que pode ser usado como exemplo do output gerado pela ferramenta, para se ter uma noção do que ela faz).




