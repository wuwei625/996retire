import numpy
import numpy.matlib
import math

def get_matrix_by_mean_and_var(target_mean, target_var, array_amount, array_length):
    # 获取指定均值、方差、样本量的二阶数组
    return (numpy.sqrt(target_var)) * numpy.matlib.randn(array_amount, array_length) + target_mean

def get_nav_matrix(target_mean, target_var, array_amount, array_length):
    # 根据指定日净值变化对数的均值、方差、样本量，模拟基金净值序列
    result = []
    start_nav = 1.0

    logarithm_matrix = get_matrix_by_mean_and_var(target_mean, target_var, array_amount, array_length).tolist()
    
    for logarithm_sequence in logarithm_matrix:
        single_nav_sequence = []
        single_nav_sequence.append(start_nav)
        for single_logarithm_increase in logarithm_sequence:
            # 日净值测算
            new_nav = single_nav_sequence[-1] * math.exp(single_logarithm_increase)
            single_nav_sequence.append(new_nav)
        # 把模拟的每组净值序列写回结果
        result.append(single_nav_sequence)

    return result
    