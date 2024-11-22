# DB

This folder contains the database where the collected data is written by the 'airodump-ng' suite. 

The 'airodump-ng' is has hardcoded the database filepath '/home/kali/Desktop/InformationElementsAnalyser/DB/InformationElements.db' to write the collected data, so please do not change the location of this file in any circunstance.

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
