import datetime
import time

rtk = 'TEST_RTK.txt'            # Revise the name
# Fixed file name
float_file = 'float.txt'
fixed_file = 'fixed.txt'

# Conver string to seconds
def str_to_seconds(time_str):
    try:
        dt = datetime.datetime.strptime(time_str, "%H:%M:%S.%f")
        second = (dt-datetime.datetime(1900,1,1)).total_seconds()
        # print(second)
        return second
    except ValueError:
        return None

# Sort out the original file and separate two files to store
def sort_RTK_file(RTK_file):
    keyword_1 = 'Time to RTK Float'
    keyword_2 = 'Time to RTK Fixed'
    float_time = 0
    float_count = 0
    fixed_time = 0
    fixed_count = 0

    i = 0
    j = 0
    with open(RTK_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if keyword_1 in line:
            float_count += 1
            time = (line[-16:-2])
            float_time += str_to_seconds(time)
            with open('float.txt', 'a', encoding='utf-8') as file_a:
                i += 1
                file_a.write(str(i) +'\t' + str(str_to_seconds(time)) + '\n')
        elif keyword_2 in line:
            fixed_count += 1
            time = (line[-16:-2])
            fixed_time += str_to_seconds(time)
            with open('fixed.txt', 'a', encoding='utf-8') as file_b:
                j += 1
                file_b.write(str(i) +'\t' + str(str_to_seconds(time)) + '\n')

    # print("Float Time: ", float_count)
    # print("Float: ", format(float_time, '.2f'), "s")
    print("Float Average: ", format(float_time/float_count, '.2f'), "s")
    # print("Fixed Time: ", fixed_count)
    # print("Fixed: ", format(fixed_time, '.2f'), "s")
    print("Fixed Average: ", format(fixed_time/fixed_count, '.2f'), "s")

    return float_count, fixed_count

# Calculate average time: removed the largest and 
def calcAvg(file_name, count_time):
    min = 100
    max = -1
    sum = 0

    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        line = line.split('\t')
        # print(line[1])
        sum += float(line[1])
        if(min > float(line[1])):
            min = float(line[1])
        if(max < float(line[1])):
            max = float(line[1])

    avg = (sum-min-max)/(count_time-2)
    print("Converged: ",    count_time, "times\t",
            "Min: ",        format(min, '.2f'), "s\t",
            "Max: ",        format(max, '.2f'), "s\t", 
            "Average: ",    format(avg, '.2f'), "s")

# Main

float_count, fixed_count = sort_RTK_file(rtk)

print("Float Stastistic: ")
calcAvg(float_file, float_count)

print("Fixed Stastistic: ")
calcAvg(fixed_file, float_count)
