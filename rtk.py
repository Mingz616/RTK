import os
# import sys
import datetime
import argparse

def get_version():
    return '4.0'

def check_file_path(filepath):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # print('Good')
        return 1
    else:
        raise RuntimeError('File is not exist or empty')

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

    if os.path.exists(float_path) and os.path.getsize(float_path) > 0:
        os.remove(float_path)
    if os.path.exists(fixed_path) and os.path.getsize(fixed_path) > 0:
        os.remove(fixed_path)

    with open(RTK_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if keyword_1 in line:
            float_count += 1
            time = (line[-16:-2])
            float_time += str_to_seconds(time)
            with open(float_path, 'a', encoding='utf-8') as file_a:
                i += 1
                file_a.write(str(i) +'\t' + str(str_to_seconds(time)) + '\n')
        elif keyword_2 in line:
            fixed_count += 1
            time = (line[-16:-2])
            fixed_time += str_to_seconds(time)
            with open(fixed_path, 'a', encoding='utf-8') as file_b:
                j += 1
                file_b.write(str(i) +'\t' + str(str_to_seconds(time)) + '\n')

    if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
        os.remove(log_path)
    with open(log_path, 'w', encoding='utf-8') as file:
        print('\n')

    # print("Float Time: ", float_count)
    # print("Float: ", format(float_time, '.2f'), "s")
    print("Float Average: ", format(float_time/float_count, '.2f'), "s")
    # print("Fixed Time: ", fixed_count)
    # print("Fixed: ", format(fixed_time, '.2f'), "s")
    print("Fixed Average: ", format(fixed_time/fixed_count, '.2f'), "s")

    return float_count, fixed_count

# Calculate average time: removed the largest and 
def calcAvg(type, count_time):
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
        # print(line[1])
        sum += float(line[1])
        if(min > float(line[1])):
            min = float(line[1])
        if(max < float(line[1])):
            max = float(line[1])

    avg = (sum-min-max)/(count_time-2)

    with open(log_path, 'a', encoding='utf-8') as file:
        file.write(type             +   " Statistcs: \t"    +   file_name   +   "\n")
        file.write('\tConverged: \t'  +   str(count_time)     +   "times\n")
        file.write("\tMin: "          +   format(min, '.2f')  +   "s\n")
        file.write("\tMax: "          +   format(max, '.2f')  +   "s\n")
        file.write("\tAverage: "      +   format(avg, '.2f')  +   "s\n")
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

    print("Float Stastistic: ")
    calcAvg('Float', float_count)

    print("Fixed Stastistic: ")
    calcAvg('Fixed', float_count)
