#---------------------------------------------------------------------------------------
# This beta heat meshtal python code tested with python 3.8.5 and python 3.9.4 [Marconi]
# require 2 addon packages "numpy" and "natsort"
# if not pre-installed use following command for install
# "pip install numpy natsort"
#---------------------------------------------------------------------------------------

import numpy as np
import os
import re
import itertools
import time
from natsort import natsort_keygen, ns

#---------------------------------------------------------------------------------------
# folder location of inventory_output_folder
inventory_output_foler = "./inventory_out"
# folder location of r2smesh input folder
r2s_input_folder = "./input"
# which time interval for extract beta heat
time_interval = 4
# if during MCNP run using FC card, option = 1, default is 0
option = 1
#---------------------------------------------------------------------------------------


# define beta heat output file
meshtal_file = "meshtal."
output_file_name = meshtal_file + str(time_interval)
#print (output_file_name)
#beta_heat = open (output_file_name,'a')


# fine string funtion
def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
        along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results



# open meshtal.fine
fine = os.path.join(r2s_input_folder, "meshtal.fine")
fine_meshtal = open (fine, 'r')
fine_meshtal_results = fine_meshtal.readlines()

# pick up header of meshtal.fine
for index, line in enumerate(fine_meshtal_results):
# search tally particle information for replacement
    meshtally_search = " mesh tally."
    matched_lines = search_string_in_file (fine, meshtally_search)

    matched_line_num1 = str(matched_lines[0]).split(",")
    matched_line_num2 = matched_line_num1[0].split("(")


    if index < option+10:
        beta_heat = open (output_file_name,'a')
#        print()
        if index == 0:
            print (" Mesh Tally Number       999", file = beta_heat)
        elif index == option+9:
            print ("        X         Y         Z     Result", file = beta_heat)
        elif index == int(matched_line_num2[1])-1:
            print (" beta heat  mesh tally.", file = beta_heat)
        else :
            print (line, end ="", file = beta_heat)
    else :
        break
beta_heat.close()


# extract X Y Z values
X_content = fine_meshtal_results[option+4]
Y_content = fine_meshtal_results[option+5]
Z_content = fine_meshtal_results[option+6]

# remove two times element 0, "XYZ" and "direction:"
X_values = X_content.split()
del X_values[0]
del X_values[0]
Y_values = Y_content.split()
del Y_values[0]
del Y_values[0]
Z_values = Z_content.split()
del Z_values[0]
del Z_values[0]

#print (X_values)

# read inventory folder
output_files = os.listdir(inventory_output_foler)
output_solted = sorted( output_files, key=lambda X: (int(X.split(".")[1]), int(X.split(".")[2]), int(X.split(".")[3])))

# output_files.sort(key=int)

# print (output_solted)

# play with fispact output files (inventory_out.X.Y.Z)
for index in output_solted:
# get X Y Z position
    #    print (index)
    split_name=index.split(".")
    
    X_index = split_name[1]
    X_index1 = X_values[int(X_index) -1]
    X_index2 = X_values[int(X_index)]
    X_position = round ((float(X_index1) + float(X_index2)) / 2 ,3)
#    print ("X ", split_name[1], "is ", X_position)
    Y_index = split_name[2]
    Y_index1 = Y_values[int(Y_index) -1]
    Y_index2 = Y_values[int(Y_index)]
    Y_position = round ((float(Y_index1) + float(Y_index2)) / 2, 3)
#    print ("Y ", split_name[2], "is ", Y_position)
    Z_index = split_name[3]
    Z_index1 = Z_values[int(Z_index) -1]
    Z_index2 = Z_values[int(Z_index)]
    Z_position = round ((float(Z_index1) + float(Z_index2)) / 2, 3)
#    print ("Z ",split_name[3], "is ", Z_position)

#    print (X_position, Y_position, Z_position)

# read fispact output files (inventory_out)
    work_file = os.path.join(inventory_output_foler, index)
    inventory_out = open (work_file, "r")
    inventory_out_results = inventory_out.readlines()

    time_interval_search = "1* * * * * TIME INTERVAL"
    matched_lines = search_string_in_file (work_file, time_interval_search)
    
    print_output = []
    
    for elem in matched_lines:
        time_interval_output = elem[1].split()
#        print (time_interval_output[7])
        if (int(time_interval_output[7]) == time_interval):
#            print('Line Number = ', elem[0], elem[1])

# search beta heat output line number
            matched_beta_lines = search_string_in_file (work_file, "   TOTAL BETA  HEAT PRODUCTION")
            
            beta_results = []
            
            for elem_b in matched_beta_lines:
                if (elem_b[0] > elem[0]):
                    #print (elem[0])
                    #print (elem_b[0])
                    beta_heat_values = elem_b[1].split()
                    beta_results_float = "{:.5e}".format(float(beta_heat_values[4]))
                    beta_heat_results = open (output_file_name,'a')
                    print (" ", X_position,"", Y_position,"", Z_position,"", beta_results_float, sep = "  ", file = beta_heat_results)
                    beta_heat_results.close()
#                    beta_results.append(beta_results_float)
                    break
            
#            beta_results = "{:.5e}".format(float(beta_heat[4]))
#            beta_output.append(beta_results)

#            print (float(X_position), float(Y_position), float(Z_position), beta_results, file = beta_heat)

#            print_output_lines = "   " + str(X_position) + "  " + str(Y_position) + "  " + str(Z_position) + "  " + str(beta_results)
#            print (print_output_lines)
#            print_output.append(print_output_lines)

#    print (*print_output, sep = "  ", file = beta_heat_results)
#    print (*print_output, sep = "  ")
#    beta_heat_results.close()
