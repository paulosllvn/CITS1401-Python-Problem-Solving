# Author: Paul O'Sullivan
# Student ID: 21492318
# Date Created:26/08/2019
# This program takes a file World Happiness Index and will, depending on a metric((min,median,mean,harmonic mean)
# return a correlation number OR a list of countries that correspond with this metric. 



# Module required for checking the existance of inputted filename
import os


# Processes the inputs from the user
def userinput():
    filename = input("Enter the name of the file you wish to read ").strip()
    if not os.path.isfile(filename):
        print("ERROR : This filename does not exist")
        exit(1)

    if os.stat(filename).st_size == 0:
        print("ERROR : This is an empty file")
        exit(1)

    metric = input("Please choose a metric from min, mean, median, harmonic mean ").lower().strip()
    if metric not in {"min", "mean", "median", "harmonic mean"}:
        print("ERROR: This metric is invalid")
        exit(1)

    action = input(
        "Chose action to be performed on the data using the specified metric. Options are list, correlation ").lower().strip()
    if action not in {"list", "correlation"}:
        print("ERROR: This action is invalid")
        exit(1)

    return filename, metric, action


# Reads file and converts appropriate values to None or Float
def readConvert(filename):
    with open(filename, "r") as f:
        data = [line.split(",")[1:] for line in f.read().splitlines()[1:]]

    with open(filename, "r") as g:
        countries = [line[:line.find(",")] for line in g.read().splitlines()[1:]]

    
    floatData = []
    for i, list in enumerate(data):
        row = [countries[i]]
        for val in list:
            if val:
                row.append(float(val))
            else:
                row.append(None)
        floatData.append(row)

    return floatData


# Normalises data for each country for all categories except "country"
def normalise(data):

    for i in range(len(data[0])):
        max = float('-inf')
        min = float('inf')

        for j in range(len(data)):
            value = data[j][i]

            if value != None and not isinstance(value, str):
                if value < min:
                    min = value
                elif value > max:
                    max = value

        for k in range(len(data)):
            value = data[k][i]
            if value != None and not isinstance(value, str):
                data[k][i] = ((value - min) / (max - min))

    for mylist in data:
        while (None in mylist):
            mylist.remove(None)
    return data


# Function for calculating and returning the average of a list
def average(lst):
    return sum(lst) / len(lst)


# Function for calculating and returning the median of a list.
# Calculates the average of both middle values if there are an even number of entries within the list
def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:

        return (sortedLst[index] + sortedLst[index + 1]) / 2.0


# Function for calculating and returning the harmonic mean of a list
# Ignores any zero values while also ignoring zero values when determining the length of the list.
def harmonicmean(lst):
    tempList = []
    length = 0

    for i, vals in enumerate(lst):
        if vals == 0 or None:
            continue
        else:
            tempList.append(1 / lst[i])
            length += 1

    totalOfTemp = sum(tempList)

    return length / totalOfTemp


# Function for containing calculations based on the given combination of user inputs
# I chose to check the metric first instead of the action due to the fact that both actions use the data calculated from
# the metric. For example, the "mean_list" is used for both "list" and "correlation"
def calculation(metric, action, data):
   
    if metric == "min":
        min_list = []
        for list in data:
            min1 = min([x for x in list][2:])
            tuple1 = (list[0])
            tuple2 = (tuple1, min1)
            min_list.append(tuple2)

        # Sorts list in descending order by each countries minimum values
        min_list.sort(key=lambda x: x[1], reverse=True)

        if action == 'list':
            for entry in min_list:
                print(f'{entry[0]} {entry[1]:.4f}')

        elif action == 'correlation':
            # Calculate Spearman Correlation value and print the value to 4 decimal places
            spearmanMean = spearman(data, min_list)
            print("The correlation coefficient between the study ranking and the ranking using the"
                  " min metric is", "{:.4f}".format(spearmanMean))

   
    elif metric == "mean":
        mean_list = []
        for list in data:
            mean = average([x for x in list][2:])
            tuple1 = (list[0])
            tuple2 = (tuple1, mean)
            mean_list.append(tuple2)

        mean_list.sort(key=lambda x: x[1], reverse=True)
        if action == 'list':
            for entry in mean_list:
                print(f'{entry[0]} {entry[1]:.4f}')

        elif action == 'correlation':
            spearmanMean = spearman(data, mean_list)
            print("The correlation coefficient between the study ranking and the ranking using the"
                  " mean metric is", "{:.4f}".format(spearmanMean))


    elif metric == "median":
        
        median_list = []
        for list in data:
            median1 = median([x for x in list][2:])
            tuple1 = (list[0])
            tuple2 = (tuple1, median1)
            median_list.append(tuple2)

        median_list.sort(key=lambda x: x[1], reverse=True)

        if action == 'list':
            for entry in median_list:
                print(f'{entry[0]} {entry[1]:.4f}')

        elif action == 'correlation':
            spearmanMean = spearman(data, median_list)
            print("The correlation coefficient between the study ranking and the ranking using the"
                  " median metric is", "{:.4f}".format(spearmanMean))



    elif metric == "harmonic mean":
        
        harmonic_list = []
        for list in data:
            
            harmonicmeancalc = harmonicmean([x for x in list][2:])
            tuple1 = (list[0])
            tuple2 = (tuple1, harmonicmeancalc)
            harmonic_list.append(tuple2)  

        harmonic_list.sort(key=lambda x: x[1], reverse=True)

        if action == 'list':
            for entry in harmonic_list:
                print(f'{entry[0]} {entry[1]:.4f}')

        elif action == 'correlation':
            spearmanHarmonic = spearman(data, harmonic_list)
            print("The correlation coefficient between the study ranking and the ranking using the "
                  "harmonic mean metric is", "{:.4f}".format(spearmanHarmonic))


# Function for calculating the correlation between the rankings of a country's life ladder score vs a calculated metric
# Metric can be min,mean,median or harmonic mean
def spearman(data, list):
    lifeladder = [data[i][:2] for i in range(len(data))]

    lifeladder.sort(key=lambda x: x[1], reverse=True)
    list.sort(key=lambda x: x[1], reverse=True)

    ranking = [i for i, j in enumerate(lifeladder, start=1)]


    ranking2 = []
    for ladderList in lifeladder:
        for j, metricList in enumerate(list, start=1):
            if ladderList[0] == metricList[0]:
                ranking2.append(j)

    # List of differences between "Metric Ranking" and "Life Ladder Ranking"
    differences = [ranking[i] - ranking2[i] for i, j in enumerate(ranking)]

    # Sum of the square of each difference.
    differencesquared = sum([i * i for i in differences])

    # Spearman correlation coefficient calculation
    spearman = 1 - ((6 * differencesquared) / (len(lifeladder) * (len(lifeladder) ** 2 - 1)))

    return spearman


def main():
    filename, metic, action = userinput()
    countryValues = readConvert(filename)
    normaliseVales = normalise(countryValues)
    calculation(metic, action, normaliseVales)

