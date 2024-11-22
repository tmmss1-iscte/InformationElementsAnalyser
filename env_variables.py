# env_variables.py


# Input database
input_db_filepath = "/home/kali/Desktop/InformationElementsAnalyser/example/PublicDataset.db"               # input database filepath

# Varying Bytes/Bits analysis level
show_variation = 'show-bits-variation'                                                                      # ['show-bits-variation' or 'show-bytes-variation' or 'no-variation']

# Definitely and Reasonable Varying Bytes/Bits Thresholds
DEFINITELY_NUMBER_MESSAGES = 20
REASONABLE_NUMBER_MESSAGES = 10

DEFINITELY_PERCENTAGE_MIN = 25
DEFINITELY_PERCENTAGE_MAX = 50

REASONABLE_PERCENTAGE_MIN = 10
REASONABLE_PERCENTAGE_MAX = 25

# Write output to text file
write_to_file = False                                                                                   # write ouput to text file ['True' or 'False']
output_txt_filepath = "/home/kali/Desktop/InformationElementsAnalyser/InformationElementsReport.txt"    # output .txt file filepath