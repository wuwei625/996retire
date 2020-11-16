import numpy
import numpy.matlib
import math

def get_geometric_mean(raw_list):
    log_list = []
    result = -1

    for item in raw_list:
        log_list.append(math.log(item))
    if len(log_list) > 0:
        log_mean = numpy.average(log_list)
        result = math.exp(log_mean)

    return result
