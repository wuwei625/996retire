import numpy
import numpy.matlib
import math
import multiprocessing

def get_matrix_by_mean_and_var(target_mean, target_var, array_amount, array_length):
    # 获取指定均值、方差、样本量的二阶数组
    return (numpy.sqrt(target_var)) * numpy.matlib.randn(array_amount, array_length) + target_mean

def append_nav_list_to_matrix(logarithm_matrix):
    result = []
    start_nav = 1.0
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

def internal_get_nav_matrix(target_mean, target_var, array_amount, array_length):
    # 根据指定日净值变化对数的均值、方差、样本量，模拟基金净值序列
    logarithm_matrix = get_matrix_by_mean_and_var(target_mean, target_var, array_amount, array_length).tolist()
    result = append_nav_list_to_matrix(logarithm_matrix)
    return result

def get_nav_matrix(target_mean, target_var, array_amount, array_length):
    # 根据指定日净值变化对数的均值、方差、样本量，模拟基金净值序列
    result = []
    # 在有条件的情况下采用多进程机制，把总核数-1全部用掉
    processor_number_available = multiprocessing.cpu_count() - 1

    # 可用核大于1时采用多进程
    if processor_number_available > 1:
        sub_amount = array_amount // processor_number_available + 1
        sub_result = []
        pool = multiprocessing.Pool(processes=processor_number_available)
        for i in range(0, processor_number_available):
            # 分配计算量
            tmp = pool.apply_async(
                func=internal_get_nav_matrix, 
                args=(target_mean, target_var, sub_amount, array_length)
            )
            sub_result.append(tmp)
        pool.close()
        pool.join()
        for i in range(0, processor_number_available):
            result.extend(sub_result[i].get())
    else:
        # 单进程
        result = internal_get_nav_matrix(target_mean, target_var, array_amount, array_length).tolist()

    return result