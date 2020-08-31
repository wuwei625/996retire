import math
import numpy

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
