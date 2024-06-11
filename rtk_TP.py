"""
    > File Name:     RTK Performance Analysis Tool
    > Version:       V7.0
    > Author:        Ming
    > Mail:          
    > Created Time:  June 6th, 2024
"""

import os
import datetime
import argparse

def get_version():
    """Version Display"""
    return '7.0'

def check_file_path(filepath):
    """
    Description: Check the file is existed or not
    Parameter:   File path and name
    Return:    
    """
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # print('Good')
        return 1
    else:
        raise RuntimeError('File is not exist or empty')

# Conver string to seconds
def str_to_seconds(time_str):
    """
    Description:Convert time string to double second
    Parameter:  str(time)
    Return:     double(time) in seconds  
    """
    try:
        dt = datetime.datetime.strptime(time_str, "%H:%M:%S.%f")
        second = (dt-datetime.datetime(1900,1,1)).total_seconds()
        return second
    except ValueError:
        return None
    
def conv_12to24(time_str):
    pd = time_str.split(' ')
    if(pd[1] == "PM,"):
        hr = int(pd[0][0:1])
        min = int(pd[0][2:4])
        sec = int(pd[0][6:8])
        # print("Test: ", hr, min, sec)
        return hr+12, min, sec
    else:
        hr = int(pd[0][0:2])
        min = int(pd[0][3:5])
        sec = int(pd[0][6:8])
        # print("Test: ", hr, min, sec)
        return hr, min, sec

def calc_period(start_time_str, end_time_str):
    """
    Description:Convert time string to double hours
    Parameter:  str(start_time), str(end_time)
    Return:     period in hours  
    """
    try:
        # start_time = datetime.datetime.strptime(start_time_str, "%H:%M:%S %p, %b %d")
        # start_time = start_time - datetime.datetime(1900,1,1)
        # end_time = datetime.datetime.strptime(end_time_str, "%H:%M:%S %p, %b %d")
        # end_time = end_time - datetime.datetime(1900,1,1)

        # # Separte morning or afternoon
        # start_hr, start_min, start_sec = conv_12to24(start_time_str)
        # end_hr, end_min, end_sec = conv_12to24(end_time_str)

        # # Calc period
        # hr = end_hr - start_hr
        # min = end_min - start_min
        # sec = end_sec - start_sec

        # Organize time frame
        # period = datetime.time(hour=hr, minute=min, second=sec)
        # print("\nTest start time: ", period,  '\n')

        start_time = datetime.datetime.strptime(start_time_str, "%H:%M:%S")
        end_time = datetime.datetime.strptime(end_time_str, "%H:%M:%S")
        # print("Test: ", start_time, end_time)
        period = end_time - start_time

        return period
    except ValueError:
        return None

# Sort out the original file and separate two files to store
def sort_RTK_file(RTK_file):

    """
    Description:    Initialization, check all the valid RTK result
                    Save the Float and Fixed time into separate files
                    And Save the RTK period into log file
    Parameter:      File path and File name
    Return:         int(Count RTK times) in Float and Fixed
    """
    keyword_1 = 'Time to RTK Float'
    keyword_2 = 'Time to RTK Fixed'
    float_time = 0
    float_count = 0
    fixed_time = 0
    fixed_count = 0

    i = 0
    j = 0

    # Delete the file if it's existed to ensure refresh the result
    if os.path.exists(float_path) and os.path.getsize(float_path) > 0:
        os.remove(float_path)
    if os.path.exists(fixed_path) and os.path.getsize(fixed_path) > 0:
        os.remove(fixed_path)

    # Read the RTK file's data
    with open(RTK_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Read the start time from the first line
    first_line = lines[5]
    first_line = first_line.split(' ')
    first_time = first_line[0]

    # Read the end time from the end line
    last_line = lines[-1]
    last_line = last_line.split(' ')
    last_time = last_line[0]

    # Calculate the RTK test period
    # print("Test: ", first_time[1:-1], last_time[1:-1])
    diff = calc_period(first_time[1:-1], last_time[1:-1])
    print("RTK Period:\t", diff)

    for line in lines:
        if keyword_1 in line:           # Float statistic
            float_count += 1
            line = line.split(' ')      # Splite the string to list
            time = (line[-1])           # Time is the last one in the list
            float_time += str_to_seconds(time[:-2]) # -2 is to short 1-bit of the milliseconds
            # Save the float time to the file
            with open(float_path, 'a', encoding='utf-8') as file_a:
                i += 1
                file_a.write(str(i) +'\t' + str(str_to_seconds(time[:-2])) + '\n')
        elif keyword_2 in line:
            fixed_count += 1
            line = line.split(' ')
            time = (line[-1])
            fixed_time += str_to_seconds(time[:-2])
            # Save the fixed time to the file
            with open(fixed_path, 'a', encoding='utf-8') as file_b:
                j += 1
                file_b.write(str(i) +'\t' + str(str_to_seconds(time[:-2])) + '\n')

    # Check existance of the log file to ensure refresh the statitical result
    if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
        os.remove(log_path)
    with open(log_path, 'w', encoding='utf-8') as file:         # Add RTK test period into the file
        file.write("Analyzed File: \t" + str(file_path) + "\n")
        file.write("RTK Period: \t\t" + str(diff) + " hours\n\n")

    print("RTK Rough Average")       # This average doesn't rull out the maximum and minimum value
    # print("Float Time: ", float_count)
    # print("Float: ", format(float_time, '.2f'), "s")
    print("Float Average: ", format(float_time/float_count, '.2f'), "s")
    # print("Fixed Time: ", fixed_count)
    # print("Fixed: ", format(fixed_time, '.2f'), "s")
    print("Fixed Average: ", format(fixed_time/fixed_count, '.2f'), "s")

    return float_count, fixed_count

# Calculate average time: removed the largest and 
def calcAvg(type, count_time):
    """
    Description:    Analyze the RTK performance by calculating the average RTK time
                    Save the Float and Fixed average time into log file
    Parameter:      str(Float or Fixed), int(Count RTK times) in Float and Fixed
    Return:         
    """
    min = 100
    max = -1
    sum = 0

    if(type == 'Float'):
        file_name = float_path
    elif(type == "Fixed"):
        file_name = fixed_path
    else:
        assert("Type \"Float\" Or \"Fixed\"")

    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        line = line.split('\t')
        sum += float(line[1])
        if(min > float(line[1])):
            min = float(line[1])
        if(max < float(line[1])):
            max = float(line[1])

    avg = (sum-min-max)/(count_time-2)

    with open(log_path, 'a', encoding='utf-8') as file:
        file.write(type               +   " Statistcs: \t"    +   file_name   +   "\n")
        file.write('\tConverged: \t'  +   str(count_time)     +   "times\n")
        file.write("\tMin: \t\t"      +   format(min, '.2f')  +   "s\n")
        file.write("\tMax: \t\t"      +   format(max, '.2f')  +   "s\n")
        file.write("\tAverage: \t"    +   format(avg, '.2f')  +   "s\n")
        file.write("\n")

    print(type, " Statistcs: \t", file_name, "\n",
        "Converged: ",    count_time, "times\t",
            "Min: ",        format(min, '.2f'), "s\t",
            "Max: ",        format(max, '.2f'), "s\t", 
            "Average: ",    format(avg, '.2f'), "s")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="RTK Performance Analysis and Stastical Tool")
    parser.add_argument('--path', type=str, help='address of the RTK file', default=os.path.abspath(""))
    parser.add_argument('--file', type=str, help='RTK file name', default='TEST_RTK.txt')
    parser.add_argument('--log', type=str, help='Final statistic file name', default='log.txt')
    parser.add_argument('-v', '--version', action='version', version=get_version(), help="Display Version")

    args = parser.parse_args()

    # path_and_file = sys.argv[0]
    # original_path = os.path.abspath("")

    file_path = os.path.join(args.path, args.file)
    # print(file_path)
    float_path = os.path.join(args.path, 'gen_float_stat.txt')
    fixed_path = os.path.join(args.path, 'gen_fixed_stat.txt')
    log_path = os.path.join(args.path, args.log)

    if(check_file_path(file_path)):
        RTK_file = file_path
        # print(RTK_file)

    float_count, fixed_count = sort_RTK_file(RTK_file)

    calcAvg('Float', float_count)

    calcAvg('Fixed', float_count)
