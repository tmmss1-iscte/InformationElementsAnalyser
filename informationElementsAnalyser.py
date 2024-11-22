import sqlite3
import datetime as dt
from simple_colors import *

from env_variables import input_db_filepath, show_variation, write_to_file, output_txt_filepath, DEFINITELY_NUMBER_MESSAGES, REASONABLE_NUMBER_MESSAGES, DEFINITELY_PERCENTAGE_MIN, DEFINITELY_PERCENTAGE_MAX, REASONABLE_PERCENTAGE_MIN, REASONABLE_PERCENTAGE_MAX


show_bytes_bits_vari = show_variation

if(show_bytes_bits_vari == "show-bits-variation"):
    show_bytes_variation = 1
    show_bits_variation = 1
elif (show_bytes_bits_vari == "show-bytes-variation"):
    show_bytes_variation = 1
    show_bits_variation = 0
elif (show_bytes_bits_vari == "no-variation"):
    show_bytes_variation = 0
else:
    print("Argumento 1 invalido! Escolher entre: 'no-variation' ou 'show-bytes-variation' ou 'show-bits-variation' se pretender ou nao visualizar variacao, e a que nivel (bytes ou dos bits) para cada Information Element.")
    exit(0)

if write_to_file == True:
    write_file = 1
elif write_to_file == False:
    write_file = 0
else:
    print("Argumento 2 invalido! Escolher entre: 'write' ou 'no-write'.")
    exit(0)


# Conectar com base de dados
connwifi = sqlite3.connect(input_db_filepath, timeout=30)
cwifi = connwifi.cursor()

if write_file: 
    file = open(output_txt_filepath, 'a')

# Data e hora atual 
dataAtual=dt.datetime.now().replace(second=0, microsecond=0)
if write_file: file.write("#################################### [" + str(dataAtual) + "] ######################################\n\n")


# Informacoes Gerais
print("\n--------------------------------------- Informacoes Gerais --------------------------------------------")
if write_file: file.write("\n--------------------------------------- Informacoes Gerais --------------------------------------\n")


#Numero total de Probe Requests (com enderecos MAC aleatorios) capturados
cwifi.execute('select count(*) from Information_Elements')
total_probe_req = cwifi.fetchall()
print("[Numero total de Probe Requests (enderecos MAC aleatorios)]: " + str(total_probe_req[0][0]) + "\n")
if write_file: file.write("[Numero total de Probe Requests (enderecos MAC aleatorios)]: " + str(total_probe_req[0][0]) + "\n\n")

#Numero de enderecos MAC diferentes na base de dados
cwifi.execute('select count(DISTINCT MAC_Address) from Information_Elements')
total_mac_addresses = cwifi.fetchall()
print("[Numero de enderecos MAC diferentes: " +  str(total_mac_addresses[0][0]) + "]")
if write_file: file.write("[Numero de enderecos MAC diferentes: " +  str(total_mac_addresses[0][0]) + "]\n")

#Numero de Footprints diferentes na base de dados
cwifi.execute('select count(DISTINCT Footprint) from Information_Elements')
total_footprints = cwifi.fetchall()
print("[Numero de Footprints diferentes: " +  str(total_footprints[0][0]) + "]")
if write_file: file.write("[Numero de Footprints diferentes: " +  str(total_footprints[0][0]) + "]\n")

#Racio #Enderecos MAC/#Footprints
if total_footprints[0][0] != 0:
    print("[#Enderecos MAC/#Footprints: " + str(round((total_mac_addresses[0][0]/total_footprints[0][0]),2)) + "]\n")
    if write_file: file.write("[#Enderecos MAC/#Footprints: " + str(round((total_mac_addresses[0][0]/total_footprints[0][0]),2)) + "]\n\n")
else:
    print("[#Enderecos MAC/#Footprints: 0]\n")
    if write_file: file.write("[#Enderecos MAC/#Footprints: 0]\n\n")

#Numero de enderecos MAC com apenas uma Footprint
cwifi.execute('select MAC_Address from ( select * from Information_Elements group by MAC_Address,Footprint) group by MAC_Address having count(MAC_Address)=1')
mac_adresses_one_footprint = cwifi.fetchall()
print("[Enderecos MAC com apenas uma Footprint: " +  str(len(mac_adresses_one_footprint)) + "]")
if write_file: file.write("[Enderecos MAC com apenas uma Footprint: " +  str(len(mac_adresses_one_footprint)) + "]\n")

#Numero de enderecos MAC com multiplas Footprints
cwifi.execute('select DISTINCT MAC_Address from ( select * from Information_Elements group by MAC_Address,Footprint) group by MAC_Address having count(MAC_Address)>1')
mac_adresses_multiple_footprints = cwifi.fetchall()
print("[Enderecos MAC com multiplas Footprints: " +  str(len(mac_adresses_multiple_footprints)) + "]")
if write_file: file.write("[Enderecos MAC com multiplas Footprints: " +  str(len(mac_adresses_multiple_footprints)) + "]\n")

print("------------------------------------------------------------------------------------------------------")
if write_file: file.write("-------------------------------------------------------------------------------------------------\n")


# Quais os enderecos MAC com mais do que uma footprint e as diferentes footprints geradas para cada um

cwifi.execute('select MAC_Address from ( select * from Information_Elements group by MAC_Address,Footprint) group by MAC_Address having count(MAC_Address)>1')
mac_adresses = cwifi.fetchall()
number_footprints = []

print("------------------------------------- Enderecos MAC diferentes ---------------------------------------")
if write_file: file.write("---------------------------------- Enderecos MAC diferentes -------------------------------------\n\n")

#Numero de enderecos MAC com diferentes footprints
print("[Enderecos MAC com multiplas Footprints: " + str(len(mac_adresses)) + "]\n")
if write_file: file.write("[Enderecos MAC com multiplas Footprints: " + str(len(mac_adresses)) + "]\n\n")

for mac_address in mac_adresses:
    #Numero de footprints diferentes para cada endereco MAC
    cwifi.execute('select DISTINCT Footprint from Information_Elements where MAC_Address=?', (mac_address[0],))
    footprints = cwifi.fetchall()
    number_footprints.append(len(footprints))

    #Footprints diferentes de cada endereco MAC
    footprints_string = ""
    for footprint in footprints:
        footprints_string += footprint[0] + " "

    print(cyan(str(mac_address[0])) + "| " + str(len(footprints)) + " footprints diferentes | " + str(footprints_string))
    if write_file: file.write(str(mac_address[0]) + "| " + str(len(footprints)) + " footprints diferentes | " + str(footprints_string) + "\n")
print("------------------------------------------------------------------------------------------------------")
if write_file: file.write("-------------------------------------------------------------------------------------------------\n")


# Quais os Information Elements utilizados em cada Footprint para cada endereco MAC
print("----------------------------------- Information Elements Utilizados ----------------------------------")
if write_file: file.write("--------------------------------- Information Elements Utilizados -------------------------------\n")
for mac_address in mac_adresses:
    #Numero de footprints diferentes e a sua contagem para cada endereco MAC
    cwifi.execute('select Footprint,IE_array,count(*) from Information_Elements where MAC_Address=? group by Footprint order by (count(*)) DESC', (mac_address[0],))
    footprints_and_IEs = cwifi.fetchall()

    print(cyan(str("[" + mac_address[0] + "]: ")))
    if write_file: file.write(str("[" + mac_address[0] + "]: ") + "\n")
    for footprint_and_IE in footprints_and_IEs:
        print("\t" + str(footprint_and_IE[0]) + ": " + str(footprint_and_IE[1]) + "| Contagem: " + str(footprint_and_IE[2]))
        if write_file: file.write("\t" + str(footprint_and_IE[0]) + ": " + str(footprint_and_IE[1]) + "| Contagem: " + str(footprint_and_IE[2]) + "\n")

    print("")
    if write_file: file.write("\n")
        

print("------------------------------------------------------------------------------------------------------")
if write_file: file.write("-------------------------------------------------------------------------------------------------\n")


GREEN_THREHSOLD = 10        #Ate este valor o output sera com a cor verde (percentagem nao justifica remocao desse bit)
YELLOW_THRESHOLD = 40       #Ate este valor o output sera com a cor amarela (percentagem pode justificar a remocao desse bit)
RED_THRESHOLD = 50          #Ate este valor o output sera com a cor vermelha (percentagem justifica certamente a remocao desse bit)


# Quais os Information Elements e os bits/bytes que variaram para cada endereco MAC

info_elements = ["Footprint","IE array", "Supported Rates", "Extended Supported Rates", "DS Parameter Set", "HT Capabilities", "Extended Capabilities", "VHT Capabilities", "RM Enabled Capabilities", "Interworking", "Supported Operating Classes"]

definitely_variable_bits = []
reasonable_variable_bits = []

vendor_specific_OUI_manuf = [('00:50:F2', 'Microsoft Corp.'), ('00:10:18','Broadcom'), ('00:90:4C', 'Epigram Inc.'), ('50:6F:9A', 'Wi-Fi Alliance'), ('00:17:F2', 'Apple'), ('8C:FD:F0', 'Qualcomm')]

Dict = {}


for mac_address in mac_adresses:
    cwifi.execute('select Footprint,IE_array,Supp_Rates,Extended_Supp_Rates,DS_Parameter,HT_Capabilities,Extended_Capabilities,VHT_Capabilities,RM_enabled_Capabilities,Interworking,Supp_Operating_Classes,Vendor_1,Vendor_2,Vendor_3,Vendor_4 from Information_Elements where MAC_Address=? group by Footprint order by length(IE_array),IE_array', (mac_address[0],) )
    different_footprints = cwifi.fetchall()
    footprints_info_elements_utilized = []              #Lista com Information Elements utilizados em cada Footprint diferente para cada endereco MAC
    #print(mac_address[0])        

    Dict[mac_address[0]] = {}                           #Dicionario que ira conter informacao sobre cada endereco MAC

    variable_info_elements = []                         #Lista com Information Elements que variaram para cada endereco MAC
    dictionary_list = []                                #Lista de dicionarios com bytes e bits diferentes de cada Information Element diferente para cada endereco MAC

    variable_OUIs = []

    content_variation_elements = [[],[],[],[],[],[],[],[],[],[],[]]


    #Numero total de mensagens para esse endereco MAC
    cwifi.execute('select count(*) from Information_Elements where MAC_Address=? group by Footprint', (mac_address[0],))
    footprints_count = cwifi.fetchall()

    footprints_total_count = 0

    for count in footprints_count:
        footprints_total_count += count[0]

    #Apanhar variacoes de conteudo para cada Information Element de cada Footprint do endereco MAC (ate aos Vendor Specific)
    for different_footprint in different_footprints:

        for a in range(2, 11):
            
            if different_footprint[a] not in content_variation_elements[a] and different_footprint[a] != '' and different_footprint[a] != ' ':
                content_variation_elements[a].append(different_footprint[a])

    #Apanhar Information Elements que variaram (ate aos Vendor Specific)
    for r in range(len(content_variation_elements)):

        if len(content_variation_elements[r]) > 1:
            variable_info_elements.append(info_elements[r])   
       
    i = 0
    # Iterar os conteudos diferentes de cada Information Element (ate aos Vendor Specific)
    for different_info_contents_list in content_variation_elements:

        info_element_index = content_variation_elements.index(different_info_contents_list)

        if len(different_info_contents_list) > 1:

            min_length = 0

            #Ver menor tamanho entre todos os conteudos desse Information Element, para saber ate onde se comparar
            for different_info_element_content in different_info_contents_list:
                if min_length == 0:
                    min_length = len(different_info_element_content)
                elif len(different_info_element_content) < min_length:
                    min_length = len(different_info_element_content)

            #print(min_length)
            #print(different_info_contents_list)

            different_info_elem_content_truncated_list = []

            #Truncar todos os conteudos ao tamanho de bytes minimo entre todos os conteudos desse Information Element
            for different_info_element_content in different_info_contents_list:
                if len(different_info_element_content) > min_length:
                    truncated_bytes = different_info_element_content[:-(len(different_info_element_content)-min_length)]
                else:
                    truncated_bytes = different_info_element_content
                different_info_elem_content_truncated_list.append(truncated_bytes)

            #print(different_info_elem_content_truncated_list)

            if len(set(different_info_elem_content_truncated_list)) > 1:

                bits_number = "0" + str(int(min_length/2)*8) + "b"

                xor_list = []       #Lista de todos os XORs feitos entre todos os conteudos desse Information Element

                #Comparar os conteudos (diferentes) de cada Information Element e fazer o XOR entre cada um adjacentemente
                for different_info_element_content_x,different_info_element_content_y in zip(different_info_elem_content_truncated_list,different_info_elem_content_truncated_list[1:]):

                    #XOR entre todos os conteudos desses Information Elements
                    convert_string_x = int(different_info_element_content_x, base=16)
                    convert_string_y = int(different_info_element_content_y, base=16)
                    xor = convert_string_x ^ convert_string_y

                    binary_xor = format(xor, bits_number)

                    xor_list.append(binary_xor)


                final_xor = format(0, bits_number)
                final_xor_l = list(final_xor)

                #print(xor_list)

                #"Soma" de todos os XORs
                for xor_element in xor_list:
                    for xor_bit in range(len(xor_element)):
                        if str(xor_element[xor_bit]) == "1":
                            final_xor_l[xor_bit] = '1'

                final_xor = "".join(final_xor_l)

                #print(final_xor)

                bit_position = 1
                variable_bytes = []             #Bytes diferentes no conteudo
                variable_bits = []              #Bits e bytes diferentes no conteudo
                variable_bits_count = []        #Contagem de '0's e '1's de cada bit de cada byte diferente no conteudo

                temp_definitely_variable_bits = []
                temp_reasonable_variable_bits = []

                #Obtencao dos bits/bytes diferentes de entre todas as Footprints
                for bit in range(len(final_xor)):
                    
                    if(int(final_xor[bit]) == 1):

                        if( bit_position%8 != 0 ):
                            position_bit = bit_position%8
                            position_byte = bit_position//8 + 1
                        else:
                            position_bit = 8
                            position_byte = bit_position//8
                        
                        if position_byte not in variable_bytes:
                            variable_bytes.append(position_byte)
                            #print("[" + str(position_byte) + "º byte]")
                            
                        variable_bits.append(str(position_byte) + "|" + str(position_bit))
                        #print("[" + str(position_byte) + "º byte | " + str(position_bit) + "º bit]")

                        zeros_counter = 0
                        ones_counter = 0
                        
                        #Contagem de 0's e 1's desse bit
                        for different_footprint in different_footprints:
                                
                                cwifi.execute('select count(*) from Information_Elements where MAC_Address=? and Footprint=?', (mac_address[0],different_footprint[0],))
                                footprint_count = cwifi.fetchall()

                                if different_footprint[i] != '' and different_footprint[i] != ' ':

                                    if len(different_footprint[i]) > min_length:
                                        truncated_bytes_temp = different_footprint[i][:-(len(different_footprint[i])-min_length)]
                                    else:
                                        truncated_bytes_temp = different_footprint[i]

                                    convert_string_temp = int(truncated_bytes_temp, base=16)

                                    binary_temp = format(convert_string_temp, bits_number)

                                    #print(binary_temp)

                                    if binary_temp[bit_position-1] != None:

                                        if str(binary_temp[bit_position-1]) == "0":
                                            zeros_counter += footprint_count[0][0]
                                        elif str(binary_temp[bit_position-1]) == "1":
                                            ones_counter += footprint_count[0][0]

                        bit0_calc = str(zeros_counter) + "/" + str(footprints_total_count)
                        bit0_percentage = round((zeros_counter/footprints_total_count)*100)

                        bit1_calc = str(ones_counter) + "/" + str(footprints_total_count)
                        bit1_percentage = round((ones_counter/footprints_total_count)*100)

                        variable_bits_count.append(str(position_byte) + "|" + str(position_bit) + "|" + str(bit0_calc) + "|" + str(bit0_percentage) + "|" + str(bit1_calc) + "|" + str(bit1_percentage))

                        if ((int(bit0_percentage) >= DEFINITELY_PERCENTAGE_MIN and int(bit0_percentage) <= DEFINITELY_PERCENTAGE_MAX) or (int(bit1_percentage) >= DEFINITELY_PERCENTAGE_MIN and int(bit1_percentage) <= DEFINITELY_PERCENTAGE_MAX)) and (int(footprints_total_count) > DEFINITELY_NUMBER_MESSAGES):
                            if str(position_byte) + "|" + str(position_bit) not in temp_definitely_variable_bits:
                                temp_definitely_variable_bits.append(str(position_byte) + "|" + str(position_bit))

                        elif ((int(bit0_percentage) >= REASONABLE_PERCENTAGE_MIN and int(bit0_percentage) <= REASONABLE_PERCENTAGE_MAX) or (int(bit1_percentage) >= REASONABLE_PERCENTAGE_MIN and int(bit1_percentage) <= REASONABLE_PERCENTAGE_MAX)) and (int(footprints_total_count) > REASONABLE_NUMBER_MESSAGES):
                            if str(position_byte) + "|" + str(position_bit) not in temp_reasonable_variable_bits and str(position_byte) + "|" + str(position_bit) not in temp_definitely_variable_bits:
                                temp_reasonable_variable_bits.append(str(position_byte) + "|" + str(position_bit))

                    bit_position += 1

                #print(temp_definitely_variable_bits)


                # Acrescentar bits definitivamente variaveis desse Information Element
                elemnt_already_exists = 0
                for info_elemnt_variable_bits_list in definitely_variable_bits:

                    if info_elemnt_variable_bits_list[0] == info_elements[i]:
                        elemnt_already_exists = 1

                if elemnt_already_exists == 0:
                    temp_list = []
                    temp_list.append(info_elements[i])
                    temp_list.append(temp_definitely_variable_bits)
                    definitely_variable_bits.append(temp_list)
                else:
                    for info_elemnt_variable_bits_list in definitely_variable_bits:

                        if info_elemnt_variable_bits_list[0] == info_elements[i]:

                            for variable_byte_bit in temp_definitely_variable_bits:

                                if variable_byte_bit not in info_elemnt_variable_bits_list[1]:
                                    info_elemnt_variable_bits_list[1].append(variable_byte_bit)


                # Acrescentar bits possivelmente variaveis desse Information Elements
                elemnt_already_exists = 0
                for info_elemnt_variable_bits_list in reasonable_variable_bits:
                    if str(info_elemnt_variable_bits_list[0]) == info_elements[i]:
                        elemnt_already_exists = 1
                        
                if elemnt_already_exists == 0:
                    temp_list = []
                    temp_list.append(info_elements[i])
                    temp_list.append(temp_reasonable_variable_bits)
                    reasonable_variable_bits.append(temp_list)
                else:
                    for info_elemnt_variable_bits_list in reasonable_variable_bits:

                        if info_elemnt_variable_bits_list[0] == info_elements[i]:

                            for variable_byte_bit in temp_reasonable_variable_bits:

                                if variable_byte_bit not in info_elemnt_variable_bits_list[1]:
                                    info_elemnt_variable_bits_list[1].append(variable_byte_bit)


                #Construcao de um dicionario para cada byte de cada Information Element com bits diferentes e sua contagem
                Info_Element_Byte_Dict = {}
                for t in range(len(variable_bytes)):
                    bits_list = []
                    for b in range(len(variable_bits)):
                        byte_n = variable_bits[b].split('|')[0]
                        bit_n = variable_bits[b].split('|')[1]
                        if(str(variable_bytes[t]) == str(byte_n)):

                            for g in range(len(variable_bits_count)):
                                byte_n_n = variable_bits_count[g].split('|')[0]
                                bit_n_n = variable_bits_count[g].split('|')[1]

                                if (str(byte_n_n) == str(byte_n) and str(bit_n_n) == str(bit_n)):
                                    bits_list.append(variable_bits_count[g])

                    Info_Element_Byte_Dict["[" + str(variable_bytes[t]) + "º byte]"] = bits_list
                dictionary_list.append(Info_Element_Byte_Dict)



        i += 1


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * VENDOR SPECIFIC * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

    different_OUIs = []

    #Apanhar Vendor Specific OUIs diferentes para o endereco MAC
    for different_footprint in different_footprints:

        for a in range(11, len(different_footprint)):

            #print(different_footprint[a])

            if different_footprint[a] != '' and different_footprint[a] != ' ' and len(different_footprint[a]) > 6:

                OUI_vend = str(different_footprint[a][0]+different_footprint[a][1] + ":" + different_footprint[a][2]+different_footprint[a][3] + ":" + different_footprint[a][4]+different_footprint[a][5])
            
                if OUI_vend not in different_OUIs:
                    different_OUIs.append(OUI_vend)

    different_OUIs_content = [[] for i in range(len(different_OUIs))]

    #Apanhar variacoes de conteudo para cada Vendor Specific OUI de cada Footprint do endereco MAC
    for different_footprint in different_footprints:

        for a in range(11, len(different_footprint)):

            if different_footprint[a] != '' and different_footprint[a] != ' ' and len(different_footprint[a]) > 6:

                OUI_temp = str(different_footprint[a][0]+different_footprint[a][1] + ":" + different_footprint[a][2]+different_footprint[a][3] + ":" + different_footprint[a][4]+different_footprint[a][5])

                if OUI_temp in different_OUIs:

                    if different_OUIs_content[different_OUIs.index(OUI_temp)].count(different_footprint[a]) < 1:
                        different_OUIs_content[different_OUIs.index(OUI_temp)].append(different_footprint[a])
                            
    # Iterar os conteudos diferentes de cada Vendor Specific OUI
    for different_vendor_list in different_OUIs_content:

        OUI_vendor = different_OUIs[different_OUIs_content.index(different_vendor_list)]

        if len(different_vendor_list) > 1:

            #print("OUI " + str(OUI_vendor) + " variou.")
            #print(different_vendor_list)
            variable_info_elements.append(OUI_vendor)

            min_length = 0

            #Ver menor tamanho entre todos os conteudos desse Information Element, para saber ate onde se comparar
            for different_vendor_content in different_vendor_list:
                if min_length == 0:
                    min_length = len(different_vendor_content)
                elif len(different_vendor_content) < min_length:
                    min_length = len(different_vendor_content)

            
            different_vendor_content_truncated_list = []

            #Truncar todos os conteudos ao tamanho de bytes minimo entre todos os conteudos desse Vendor Specific
            for different_vendor_content in different_vendor_list:
                if len(different_vendor_content) > min_length:
                    truncated_bytes = different_vendor_content[:-(len(different_vendor_content)-min_length)]
                else:
                    truncated_bytes = different_vendor_content
                different_vendor_content_truncated_list.append(truncated_bytes)

            
            if len(set(different_vendor_content_truncated_list)) > 1:

                bits_number = "0" + str(int(min_length/2)*8) + "b"

                xor_list = []       #Lista de todos os XORs feitos entre todos os conteudos desse Vendor Specific

                #Comparar os conteudos (diferentes) de cada Information Element e fazer o XOR entre cada um adjacentemente
                for different_vendor_content_x,different_vendor_content_y in zip(different_vendor_content_truncated_list,different_vendor_content_truncated_list[1:]):

                    #XOR entre todos os conteudos desses Information Elements
                    convert_string_x = int(different_vendor_content_x, base=16)
                    convert_string_y = int(different_vendor_content_y, base=16)
                    xor = convert_string_x ^ convert_string_y

                    binary_xor = format(xor, bits_number)

                    xor_list.append(binary_xor)


                final_xor = format(0, bits_number)
                final_xor_l = list(final_xor)

                #print(xor_list)

                #"Soma" de todos os XORs
                for xor_element in xor_list:
                    for xor_bit in range(len(xor_element)):
                        if str(xor_element[xor_bit]) == "1":
                            final_xor_l[xor_bit] = '1'

                final_xor = "".join(final_xor_l)

                #print(final_xor)

                bit_position = 1
                variable_bytes = []             #Bytes diferentes no conteudo
                variable_bits = []              #Bits e bytes diferentes no conteudo
                variable_bits_count = []        #Contagem de '0's e '1's de cada bit de cada byte diferente no conteudo

                temp_definitely_variable_bits_vendor = []
                temp_reasonable_variable_bits_vendor = []

                #Obtencao dos bits/bytes diferentes de entre todas as Footprints
                for bit in range(len(final_xor)):
                    
                    if(int(final_xor[bit]) == 1):

                        if( bit_position%8 != 0 ):
                            position_bit = bit_position%8
                            position_byte = bit_position//8 + 1
                        else:
                            position_bit = 8
                            position_byte = bit_position//8
                        
                        if position_byte not in variable_bytes:
                            variable_bytes.append(position_byte)
                            #print("[" + str(position_byte) + "º byte]")
                            
                        variable_bits.append(str(position_byte) + "|" + str(position_bit))
                        #print("[" + str(position_byte) + "º byte | " + str(position_bit) + "º bit]")


                        zeros_counter = 0
                        ones_counter = 0
                        
                        #Contagem de 0's e 1's desse bit
                        for different_footprint in different_footprints:
                                
                                cwifi.execute('select count(*) from Information_Elements where MAC_Address=? and Footprint=?', (mac_address[0],different_footprint[0],))
                                footprint_count = cwifi.fetchall()

                                for a in range(11, len(different_footprint)):

                                    if different_footprint[a] != '' and different_footprint[a] != ' ' and len(different_footprint[a]) > 6:

                                        OUI_vend = str(different_footprint[a][0]+different_footprint[a][1] + ":" + different_footprint[a][2]+different_footprint[a][3] + ":" + different_footprint[a][4]+different_footprint[a][5])
                                    
                                        if OUI_vend == OUI_vendor:

                                            if len(different_footprint[a]) > min_length:
                                                truncated_bytes_temp = different_footprint[a][:-(len(different_footprint[i])-min_length)]
                                            else:
                                                truncated_bytes_temp = different_footprint[a]

                                            convert_string_temp = int(truncated_bytes_temp, base=16)

                                            binary_temp = format(convert_string_temp, bits_number)

                                            #print(binary_temp)

                                            if binary_temp[bit_position-1] != None:

                                                if str(binary_temp[bit_position-1]) == "0":
                                                    zeros_counter += footprint_count[0][0]
                                                elif str(binary_temp[bit_position-1]) == "1":
                                                    ones_counter += footprint_count[0][0]

                        bit0_calc = str(zeros_counter) + "/" + str(footprints_total_count)
                        bit0_percentage = round((zeros_counter/footprints_total_count)*100)

                        bit1_calc = str(ones_counter) + "/" + str(footprints_total_count)
                        bit1_percentage = round((ones_counter/footprints_total_count)*100)

                        variable_bits_count.append(str(position_byte) + "|" + str(position_bit) + "|" + str(bit0_calc) + "|" + str(bit0_percentage) + "|" + str(bit1_calc) + "|" + str(bit1_percentage))

                        if ((int(bit0_percentage) >= DEFINITELY_PERCENTAGE_MIN and int(bit0_percentage) <= DEFINITELY_PERCENTAGE_MAX) or (int(bit1_percentage) >= DEFINITELY_PERCENTAGE_MIN and int(bit1_percentage) <= DEFINITELY_PERCENTAGE_MAX)) and (int(footprints_total_count) > DEFINITELY_NUMBER_MESSAGES):
                            if str(position_byte) + "|" + str(position_bit) not in temp_definitely_variable_bits_vendor:
                                temp_definitely_variable_bits_vendor.append(str(position_byte) + "|" + str(position_bit))

                        elif ((int(bit0_percentage) >= REASONABLE_PERCENTAGE_MIN and int(bit0_percentage) <= REASONABLE_PERCENTAGE_MAX) or (int(bit1_percentage) >= REASONABLE_PERCENTAGE_MIN and int(bit1_percentage) <= REASONABLE_PERCENTAGE_MAX)) and (int(footprints_total_count) > REASONABLE_NUMBER_MESSAGES):
                            if str(position_byte) + "|" + str(position_bit) not in temp_reasonable_variable_bits_vendor and str(position_byte) + "|" + str(position_bit) not in temp_definitely_variable_bits_vendor:
                                temp_reasonable_variable_bits_vendor.append(str(position_byte) + "|" + str(position_bit))

                    bit_position += 1


                # Acrescentar bits definitivamente variaveis desse Vendor Specific OUI
                elemnt_already_exists = 0
                for info_elemnt_variable_bits_list in definitely_variable_bits:
                    if str(info_elemnt_variable_bits_list[0]) == str(OUI_vendor):
                        elemnt_already_exists = 1
                        
                if elemnt_already_exists == 0:
                    temp_list = []
                    temp_list.append(OUI_vendor)
                    temp_list.append(temp_definitely_variable_bits_vendor)
                    definitely_variable_bits.append(temp_list)
                else:
                    for info_elemnt_variable_bits_list in definitely_variable_bits:

                        if info_elemnt_variable_bits_list[0] == OUI_vendor:

                            for variable_byte_bit in temp_definitely_variable_bits_vendor:

                                if variable_byte_bit not in info_elemnt_variable_bits_list[1]:
                                    info_elemnt_variable_bits_list[1].append(variable_byte_bit)


                # Acrescentar bits possivelmente variaveis desse Vendor Specific OUI
                elemnt_already_exists = 0
                for info_elemnt_variable_bits_list in reasonable_variable_bits:
                    if str(info_elemnt_variable_bits_list[0]) == str(OUI_vendor):
                        elemnt_already_exists = 1
                        
                if elemnt_already_exists == 0:
                    temp_list = []
                    temp_list.append(OUI_vendor)
                    temp_list.append(temp_reasonable_variable_bits_vendor)
                    reasonable_variable_bits.append(temp_list)
                else:
                    for info_elemnt_variable_bits_list in reasonable_variable_bits:

                        if info_elemnt_variable_bits_list[0] == OUI_vendor:

                            for variable_byte_bit in temp_reasonable_variable_bits_vendor:

                                if variable_byte_bit not in info_elemnt_variable_bits_list[1]:
                                    info_elemnt_variable_bits_list[1].append(variable_byte_bit)
                                


                #Construcao de um dicionario para cada byte de cada Information Element com bits diferentes e sua contagem
                Info_Element_Byte_Dict = {}
                for t in range(len(variable_bytes)):
                    bits_list = []
                    for b in range(len(variable_bits)):
                        byte_n = variable_bits[b].split('|')[0]
                        bit_n = variable_bits[b].split('|')[1]
                        if(str(variable_bytes[t]) == str(byte_n)):

                            for g in range(len(variable_bits_count)):
                                byte_n_n = variable_bits_count[g].split('|')[0]
                                bit_n_n = variable_bits_count[g].split('|')[1]

                                if (str(byte_n_n) == str(byte_n) and str(bit_n_n) == str(bit_n)):
                                    bits_list.append(variable_bits_count[g])

                    Info_Element_Byte_Dict["[" + str(variable_bytes[t]) + "º byte]"] = bits_list
                dictionary_list.append(Info_Element_Byte_Dict)



    #Insercao no dicionario de cada Information Element que variou e bits/bytes que variaram
    for e in range(len(variable_info_elements)):  
            Dict[mac_address[0]][variable_info_elements[e]] = dictionary_list[e]

#print(Dict)


# Construcao de um dicionario com os bits definitivamente variaveis

Definitely_InfoElem_Dict = {}

for definitely_info_element_byte_bit_list in definitely_variable_bits:

    Definitely_InfoElem_Dict[definitely_info_element_byte_bit_list[0]] = {}

    def_bytes = []

    for definitely_byte_bit in definitely_info_element_byte_bit_list[1]:

        byte = definitely_byte_bit.split('|')[0]
        if byte not in def_bytes:
            def_bytes.append(byte)

    for def_byte in def_bytes:

        definitely_byte_bits_list = []

        for definitely_byte_bit in definitely_info_element_byte_bit_list[1]:

            byte = definitely_byte_bit.split('|')[0]

            if byte == def_byte:
                definitely_byte_bits_list.append(definitely_byte_bit.split('|')[1])

        Definitely_InfoElem_Dict[definitely_info_element_byte_bit_list[0]][def_byte] = definitely_byte_bits_list


# Construcao de um dicionario com os bits provavelmente variaveis

Reasonable_InfoElem_Dict = {}

for reasonable_info_element_byte_bit_list in reasonable_variable_bits:

    Reasonable_InfoElem_Dict[reasonable_info_element_byte_bit_list[0]] = {}

    res_bytes = []

    for reasonable_byte_bit in reasonable_info_element_byte_bit_list[1]:

        byte = reasonable_byte_bit.split('|')[0]
        if byte not in res_bytes:
            res_bytes.append(byte)

    for res_byte in res_bytes:

        reasonable_byte_bits_list = []

        for reasonable_byte_bit in reasonable_info_element_byte_bit_list[1]:

            byte = reasonable_byte_bit.split('|')[0]

            if byte == res_byte:

                if Definitely_InfoElem_Dict.get(reasonable_info_element_byte_bit_list[0]).get(res_byte) != None:
                    if reasonable_byte_bit.split('|')[1] not in Definitely_InfoElem_Dict.get(reasonable_info_element_byte_bit_list[0]).get(res_byte):
                        reasonable_byte_bits_list.append(reasonable_byte_bit.split('|')[1])
                else:
                    reasonable_byte_bits_list.append(reasonable_byte_bit.split('|')[1])

        if len(reasonable_byte_bits_list):
            Reasonable_InfoElem_Dict[reasonable_info_element_byte_bit_list[0]][res_byte] = reasonable_byte_bits_list    
        



print("----------------------------------- Information Elements Diferentes ----------------------------------\n")
if write_file: file.write("-------------------------------- Information Elements Diferentes --------------------------------\n\n")
for mac_address,info_element in Dict.items():

    if isinstance(info_element, str):
        print( cyan("[" + mac_address + "]: ") + red(str(info_element)) + "\n")
        if write_file: file.write("[" + mac_address + "]: " + str(info_element) + "\n")
    else:
        print( cyan("[" + mac_address + "]: ") + red(str(sorted(list(info_element.keys()), reverse=True))) )
        if write_file: file.write("[" + mac_address + "]: " + str(sorted(list(info_element.keys()))) + "\n")

        for key in sorted(info_element, reverse=True):

            if isinstance(info_element[key], str):
                print("\t" + red(key + ": " + str(info_element[key])))
                if write_file: file.write("\t" + key + ": " + str(info_element[key]) + "\n")
            else:

                print("\t" + red(key + ":") + magenta(" [Bytes diferentes: " + str(len(info_element[key])) + "] ") + "[Bits diferentes: " + str(sum(len(v) for v in info_element[key].values())) + "]")
                if write_file: file.write("\t" + key + ":" + " [Bytes diferentes: " + str(len(info_element[key])) + "] " + "[Bits diferentes: " + str(sum(len(v) for v in info_element[key].values())) + "]\n")


                if show_bytes_variation:
                    for byte_bit in info_element[key]:
                        print("\t   " + magenta(byte_bit))
                        if write_file: file.write("\t   " + byte_bit + "\n")

                        if show_bits_variation:
                            for bit_and_0s_1s in info_element[key][byte_bit]:
                                bit_n = bit_and_0s_1s.split('|')[1]

                                bit0_calc_n = bit_and_0s_1s.split('|')[2]
                                bit0_percentage_n = int(bit_and_0s_1s.split('|')[3])


                                bit1_calc_n = bit_and_0s_1s.split('|')[4]
                                bit1_percentage_n = int(bit_and_0s_1s.split('|')[5])


                                if (bit0_percentage_n >= YELLOW_THRESHOLD and bit0_percentage_n <= RED_THRESHOLD) or (bit1_percentage_n >= YELLOW_THRESHOLD and bit1_percentage_n <= RED_THRESHOLD):
                                    print("\t        [" + str(bit_n) + "º bit]: " + red("0: " + str(bit0_percentage_n) + "% (" + str(bit0_calc_n) + ") | 1: " + str(bit1_percentage_n) + "% (" + str(bit1_calc_n) + ")"))
                                elif (bit0_percentage_n >= GREEN_THREHSOLD and bit0_percentage_n < YELLOW_THRESHOLD) or (bit1_percentage_n >= GREEN_THREHSOLD and bit1_percentage_n < YELLOW_THRESHOLD):
                                    print("\t        [" + str(bit_n) + "º bit]: " + yellow("0: " + str(bit0_percentage_n) + "% (" + str(bit0_calc_n) + ") | 1: " + str(bit1_percentage_n) + "% (" + str(bit1_calc_n) + ")"))
                                elif (bit0_percentage_n > 0 and bit0_percentage_n < GREEN_THREHSOLD ) or (bit1_percentage_n > 0 and bit1_percentage_n < GREEN_THREHSOLD):
                                    print("\t        [" + str(bit_n) + "º bit]: " + "0: " + str(bit0_percentage_n) + "% (" + str(bit0_calc_n) + ") | 1: " + str(bit1_percentage_n) + "% (" + str(bit1_calc_n) + ")")
                                else:
                                    print("\t        [" + str(bit_n) + "º bit]: 0: " + str(bit0_percentage_n) + "% (" + str(bit0_calc_n) + ") | 1: " + str(bit1_percentage_n) + "% (" + str(bit1_calc_n) + ")")

                                if write_file: file.write("\t        [" + str(bit_n) + "º bit]: 0: " + str(bit0_percentage_n) + "% (" + str(bit0_calc_n) + ") | 1: " + str(bit1_percentage_n) + "% (" + str(bit1_calc_n) + ")" + "\n")
                

            print("")
            if write_file: file.write("\n")
    

print("------------------------------------------------------------------------------------------------------")
if write_file: file.write("-------------------------------------------------------------------------------------------------\n")

print("----------------------------------- Definitely Variable Bytes/Bits -----------------------------------\n")
if write_file: file.write("----------------------------------- Definitely Variable Bytes/Bits ------------------------------\n\n")
print("PARAMETERS:")
if write_file: file.write("PARAMETERS: \n")
print(" 1 - Minimum total number of Probe Requests: " + str(DEFINITELY_NUMBER_MESSAGES))
if write_file: file.write(" 1 - Minimum total number of Probe Requests: " + str(DEFINITELY_NUMBER_MESSAGES) + "\n")
print(" 2 - Variation Percentage: " + str(DEFINITELY_PERCENTAGE_MIN) + "%-" + str(DEFINITELY_PERCENTAGE_MAX) + "%")
if write_file: file.write(" 2 - Variation Percentage: " + str(DEFINITELY_PERCENTAGE_MIN) + "%-" + str(DEFINITELY_PERCENTAGE_MAX) + "% \n\n")
print("")


for info_element,bytes_bits in sorted(Definitely_InfoElem_Dict.items(), reverse=True):

    if len(bytes_bits):

        print(red("[" + str(info_element) + "]:"))
        if write_file: file.write("[" + str(info_element) + "]: \n")

        for byte in sorted(bytes_bits):

            print(red("  [" + str(byte) + "º byte]: "), end ="")
            if write_file: file.write("  [" + str(byte) + "º byte]: ")
            
            for count,bit in enumerate(sorted(bytes_bits[byte])):
                if count == len(bytes_bits[byte]) -1:
                    print(str(bit) + "º bit", end ="")
                    if write_file: file.write(str(bit) + "º bit")
                else:
                    print(str(bit) + "º bit, ", end ="")
                    if write_file: file.write(str(bit) + "º bit, ")
                

            print("")
            if write_file: file.write("\n")

        print("")
        if write_file: file.write("\n")

print("")
if write_file: file.write("\n")

print("------------------------------------------------------------------------------------------------------")
if write_file: file.write("-------------------------------------------------------------------------------------------------\n")        

print("----------------------------------- Possibly Variable Bytes/Bits -------------------------------------\n")
if write_file: file.write("----------------------------------- Possibly Variable Bytes/Bits --------------------------------\n\n")

print("PARAMETERS:")
if write_file: file.write("PARAMETERS: \n")
print(" 1 - Minimum total number of Probe Requests: " + str(REASONABLE_NUMBER_MESSAGES))
if write_file: file.write(" 1 - Minimum total number of Probe Requests: " + str(REASONABLE_NUMBER_MESSAGES) + "\n")
print(" 2 - Variation Percentage: " + str(REASONABLE_PERCENTAGE_MIN) + "%-" + str(REASONABLE_PERCENTAGE_MAX) + "%")
if write_file: file.write(" 2 - Variation Percentage: " + str(REASONABLE_PERCENTAGE_MIN) + "%-" + str(REASONABLE_PERCENTAGE_MAX) + "% \n\n")
print("")

for info_element,bytes_bits in sorted(Reasonable_InfoElem_Dict.items(), reverse=True):

    if len(bytes_bits):

        print(yellow("[" + str(info_element) + "]:"))
        if write_file: file.write("[" + str(info_element) + "]: \n")

        for byte in sorted(bytes_bits):

            print(yellow("  [" + str(byte) + "º byte]: "), end ="")
            if write_file: file.write("  [" + str(byte) + "º byte]: ")
            
            for count,bit in enumerate(sorted(bytes_bits[byte])):
                if count == len(bytes_bits[byte]) -1:
                    print(str(bit) + "º bit", end ="")
                else:
                    print(str(bit) + "º bit, ", end ="")
                if write_file: file.write(str(bit) + "º bit ")

            print("")
            if write_file: file.write("\n")

        print("")
        if write_file: file.write("\n")

print("")
if write_file: file.write("\n")

print("------------------------------------------------------------------------------------------------------")
if write_file: file.write("-------------------------------------------------------------------------------------------------\n")


# Qual e o racio de presenca de cada Information Element para todos os Probe Requests (com enderecos MAC aleatorios) capturados

info_elements_IDs = ['1','50','3','45','127','191','70','107','59','221(1)','221(2)','221(3)','221(4)']
info_elements_presence_rate = [0,0,0,0,0,0,0,0,0,0,0,0,0]

print("--------------------------------- Information Elements Presence Rate ---------------------------------\n")
if write_file: file.write("--------------------------------- Information Elements Presence Rate ----------------------------\n\n")

#Numero total de Probe Requests com enderecos MAC aleatorios capturados
print("[Numero total de Probe Requests (enderecos MAC aleatorios)]: " + str(total_probe_req[0][0]) + "\n")

#Obtencao de cada Probe Request capturado
cwifi.execute('select IE_array from Information_Elements')
IE_arrays = cwifi.fetchall()

#Iteracao por cada IE_array que contem os Information Element IDs para cada Probe Request
for IE_array in IE_arrays:
    info_IDs = IE_array[0].split()

    #Iteracao sobre cada Information Element utilizado
    for info_ID in info_IDs:
        if info_ID in info_elements_IDs:
            #Incrementar o contador de cada Information Element
            info_elements_presence_rate[info_elements_IDs.index(info_ID)] += 1

print("PRESENCE RATE: ")
if write_file: file.write("PRESENCE RATE: \n")
if total_probe_req[0][0] != 0:
    for r in range(2, len(info_elements)):
        print("[" + str(info_elements[r]) + "]: " + str(info_elements_presence_rate[r-2]) + " | " + str(round(((info_elements_presence_rate[r-2]/total_probe_req[0][0])*100),2)) + " %")
        if write_file: file.write("[" + str(info_elements[r]) + "]: " + str(info_elements_presence_rate[r-2]) + " | " + str(round(((info_elements_presence_rate[r-2]/total_probe_req[0][0])*100),2)) + " %\n")
else:
    print("No messages captured.")
    if write_file: file.write("No messages captured.\n")

print("")
if write_file: file.write("\n")
            
print("------------------------------------------------------------------------------------------------------")
if write_file: file.write("-------------------------------------------------------------------------------------------------\n")

# Quais sao os Vendor Specific que mais costumam aparecer e os seus tipos nos Probe Requests (com enderecos MAC aleatorios) capturados

OUIs_count_Dict = {}
OUI_Types_count_Dict = {}

for mac_address in mac_adresses:

    cwifi.execute('select count(*),Footprint,Vendor_1,Vendor_2,Vendor_3,Vendor_4 from Information_Elements where MAC_Address=? group by Footprint', (mac_address[0],) )
    different_footprints = cwifi.fetchall()

    for different_footprint in different_footprints:

        footprint_count = int(different_footprint[0])


        for a in range(len(different_footprint)):

            if a > 1 and different_footprint[a] != '' and len(different_footprint[a]) > 6:
                OUI_c = str(different_footprint[a][0])+str(different_footprint[a][1])+":"+str(different_footprint[a][2])+str(different_footprint[a][3])+":"+str(different_footprint[a][4])+str(different_footprint[a][5])
                OUI_Type = str(int(str(different_footprint[a][6])+str(different_footprint[a][7]), base=16))

                OUIs_count_Dict[OUI_c] = OUIs_count_Dict.get(OUI_c, 0) + int(footprint_count)

                if OUI_Types_count_Dict.get(OUI_c) is None:
                    OUI_Types_count_Dict[OUI_c] = {}

                OUI_Types_count_Dict[OUI_c][OUI_Type] = OUI_Types_count_Dict[OUI_c].get(OUI_Type,0) + int(footprint_count)


print("--------------------------------------- Vendor Specific Information ----------------------------------\n")
if write_file: file.write("--------------------------------------- Vendor Specific Information -----------------------------\n\n")


print("Vendor Specific mais comuns: (Probe Requests com enderecos MAC aleatorios para apenas os enderecos MAC com mais do que uma Footprint) \n")
if write_file: file.write("Vendor Specific mais comuns: (Probe Requests com enderecos MAC aleatorios para apenas os enderecos MAC com mais do que uma Footprint) \n\n")


if OUIs_count_Dict.items():
    for oui,oui_total_count in sorted(OUIs_count_Dict.items(), key=lambda x:x[1], reverse=True):

        manuf_name = ""

        for c in range(len(vendor_specific_OUI_manuf)):
            if oui == vendor_specific_OUI_manuf[c][0]:
                manuf_name = vendor_specific_OUI_manuf[c][1]

        if manuf_name == "":
            manuf_name = "Unknown"

        print("[" + str(oui) + "]: Manufacturer: " + str(manuf_name) + " | Contagem: " + str(oui_total_count) + " | " + str(round((oui_total_count/total_probe_req[0][0]*100),1)) + "%")
        if write_file: file.write("[" + str(oui) + "]: Manufacturer: " + str(manuf_name) + " | Contagem: " + str(oui_total_count) + " | " + str(round((oui_total_count/total_probe_req[0][0]*100),1)) + "%\n")

        for oui_c ,oui_type_and_count in OUI_Types_count_Dict.items():

            if oui_c == oui:
                
                for key in oui_type_and_count:
                    print("  [OUI Type: " + str(key) + "]: " + str(oui_type_and_count[key]))
                    if write_file: file.write("  [OUI Type: " + str(key) + "]: " + str(oui_type_and_count[key]) + "\n")
else:
    print("No Vendor Specific Information Elements captured.")
    if write_file: file.write("No Vendor Specific Information Elements captured. \n")


print("\n------------------------------------------------------------------------------------------------------\n")
if write_file: file.write("\n-------------------------------------------------------------------------------------------------\n\n")

if write_file: file.write("#################################################################################################\n\n")


