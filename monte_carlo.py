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

def get_nav_matrix(target_mean, target_var, array_amount, array_length):
    # 根据指定日净值变化对数的均值、方差、样本量，模拟基金净值序列
    result = []

    logarithm_matrix = get_matrix_by_mean_and_var(target_mean, target_var, array_amount, array_length).tolist()
    
    # 此处在有条件的情况下采用多任务机制，把总核数-1全部用掉
    processor_number_available = multiprocessing.cpu_count() - 1
    total_task_amount = len(logarithm_matrix)
    # 可用核大于1且需要分析的场景大于可用核2倍时采用多任务
    if processor_number_available > 1 and total_task_amount > processor_number_available * 2:
        # 根据场景数量和核数量分配任务
        sub_len = total_task_amount // processor_number_available
        sub_result = []
        pool = multiprocessing.Pool(processes=processor_number_available)

        for i in range(0, processor_number_available):
            sub_start_index = i * sub_len
            sub_end_index = (i + 1) * sub_len
            # 如果是最后一组，要把剩余任务都领走
            if i == processor_number_available - 1:
                sub_end_index = total_task_amount
            # 分配完毕，启用多任务
            tmp = pool.apply_async(
                func=append_nav_list_to_matrix, 
                args=logarithm_matrix[sub_start_index: sub_end_index]
            )
            sub_result.append(tmp)
        pool.close()
        pool.join()
        for i in range(0, processor_number_available):
            result.extend(sub_result[i].get())
    else:
        result = append_nav_list_to_matrix(logarithm_matrix)

    return result
    