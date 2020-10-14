import util_func
import const_values
import internal_history_file

import math
import numpy
import functools

# 根据代码获取基金历史净值序列
def get_nav(fund_code):
    fund_history_filename = const_values.history_path() + fund_code + ".txt"
    fund_nav = internal_history_file.get_nav_from_file(fund_history_filename)
    return fund_nav

# 获取日增长率均值和方差
def analysis_fund(fund_nav, max_nav):
    fund_nav_increase = []
    fund_nav_increase_logarithm = []
    fund_nav_increase_logarithm_mean = 0.0
    fund_nav_increase_logarithm_var = 0.0

    # 如果有限制长度（合法值是大于10的整数）则截取靠后长度个数的净值
    if (max_nav > 10 and max_nav < len(fund_nav)):
        fund_nav = fund_nav[-max_nav:]

    # 净值数据超过10个方才予以统计
    if len(fund_nav) > 10:
        i = 0
        # 根据净值，获取日增长率对数
        while i < len(fund_nav) - 1:
            fund_nav_increase.append(fund_nav[i + 1] / fund_nav[i])
            fund_nav_increase_logarithm.append(math.log(fund_nav_increase[i]))
            i += 1
        # 计算均值和方差
        fund_nav_increase_logarithm_mean = numpy.mean(fund_nav_increase_logarithm)
        fund_nav_increase_logarithm_var = numpy.var(fund_nav_increase_logarithm)
    
    return fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var

# 转为其他周期的均值或者方差
def mean_var_trans(fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var, days):
    expected_year_rate = 0.0
    expect_year_std_var = 0.0
    try:
        expected_year_rate = math.exp(fund_nav_increase_logarithm_mean * days)
        expect_year_std_var = math.sqrt(fund_nav_increase_logarithm_var * days)
    except:
        print("错误信息：日均值和方差有误！")

    return expected_year_rate, expect_year_std_var

# 获取Risk Adjusted Return
def get_rar(fund_code, risk_free_return):
    fund_nav = get_nav(fund_code)
    fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var = analysis_fund(fund_nav, 0)
    if (util_func.is_float_zero(fund_nav_increase_logarithm_var)):
        return const_values.get_non_sense_float()
    else:
        return (fund_nav_increase_logarithm_mean - risk_free_return) / fund_nav_increase_logarithm_var

# 获取未排序基金列表
def fund_list():
    return internal_history_file.fund_list(const_values.history_path())

# 获取按Risk Adjusted Return排序的基金列表
def rar_sorted_list(risk_free_return):
    if util_func.is_float_non_sense(risk_free_return):
        risk_free_return, var_d = analysis_fund(get_nav(const_values.special_code("ANNUAL")), 0)
        
    # 排序逻辑
    def cmp_fund(fund0, fund1):
        if get_rar(fund0, risk_free_return) < get_rar(fund1, risk_free_return):
            return 1
        if get_rar(fund0, risk_free_return) > get_rar(fund1, risk_free_return):
            return -1
        return 0

    # 根据外部预设的无风险利率，对候选基金进行RAR排名
    def rar_sorted_list():
        raw_list = fund_list()
        sorted_list = sorted(raw_list, key=functools.cmp_to_key(cmp_fund))
        return sorted_list
    
    return rar_sorted_list()