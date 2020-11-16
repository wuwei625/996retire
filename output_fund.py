# 输出基金信息的函数集合
import const_values
import util_func
import internal_fund_data_process
import internal_timing_invest_simulate
import algorithm_monte_carlo

import time
import numpy
from matplotlib import pyplot as plt
from matplotlib import font_manager

# 单一基金分析结果
def show_single_fund_mean_and_var(fund_code, fund_nav):
    tips_warning = "警告信息：基金的增长率和波动率均为0，可能历史业绩均为固定值，也可能未获得正确结果。"
    tips_error = "错误信息：没有获取到净值历史，或者数据太少，无法完成操作。"
    nav_amount = len(fund_nav)
    if nav_amount > 10:
        print("共导入" + str(nav_amount) + "个历史净值参与分析")
        fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var = internal_fund_data_process.analysis_fund(fund_nav, 0)
        if util_func.is_float_zero(fund_nav_increase_logarithm_mean) and util_func.is_float_zero(fund_nav_increase_logarithm_var):
            print(tips_warning)
        else:
            expected_year_rate, expect_year_std_var = internal_fund_data_process.mean_var_trans(fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var, const_values.days("YEAR"))
            if util_func.is_float_zero(fund_nav_increase_logarithm_var):
                print("基金日增长率对数的均值是%.4f%%"%(fund_nav_increase_logarithm_mean * 100))
                print("这个基金的历史年化收益率是%.2f%%"%((expected_year_rate - 1.0) * 100) + "，基本没有波动。")
            else:
                print("基金日增长率对数的均值是%.4f%%，方差是%.4f%%"%(fund_nav_increase_logarithm_mean * 100, fund_nav_increase_logarithm_var * 100))
                print("这个基金的历史年化收益率是%.2f%%，历史年化波动率是%.2f%%"%((expected_year_rate - 1.0) * 100, expect_year_std_var * 100))
    else:
        print (tips_error)

# 显示基金池全部基金的核心分析并排序
def show_list(risk_free_return = const_values.get_non_sense_float()):
    fund_list = internal_fund_data_process.rar_sorted_list(risk_free_return)
    print("基金代码\t历史年化收益\t历史年化波动")
    for fund_code in fund_list:
        if not util_func.isAnnualCode(fund_code):
            fund_nav = internal_fund_data_process.get_nav(fund_code)
            fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var = internal_fund_data_process.analysis_fund(fund_nav, 0)
            expected_year_rate, expect_year_std_var = internal_fund_data_process.mean_var_trans(fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var, const_values.days("YEAR"))
            print("%s\t\t%.2f%%\t\t%.2f%%"%(fund_code, (expected_year_rate - 1.0) * 100, expect_year_std_var * 100))

# 定投结果显示
def show_timing(fund_nav, invest_years, terminate_years, month_amount, fee_rate, fund_code, target_amount):
    final_values = []
    final_values_2 = [] # 见好就收模式的终值
    half_way_success_case_amount = 0
    final_success_case_amount = 0

    nav_amount = len(fund_nav)
    t = time.time()
    if nav_amount > 10:
        fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var = internal_fund_data_process.analysis_fund(fund_nav, 0)
        if util_func.is_float_zero(fund_nav_increase_logarithm_mean) and util_func.is_float_zero(fund_nav_increase_logarithm_var):
            print("错误信息：基金历史未获得正确结果！")
        else:
            # 获取test_times组模拟净值
            fund_nav_simulate = algorithm_monte_carlo.get_nav_matrix(fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var, const_values.test_times(), terminate_years * const_values.days("YEAR"))
            # 获取对应的账户价值
            if invest_years > 0:
                # 定投模式
                invest_times = invest_years * const_values.period_times("MONTH")
            else:
                # 一次性模式
                invest_times = 1
            account_values_simulate = internal_timing_invest_simulate.get_simulated_asset_values(const_values.days("MONTH"), invest_times, month_amount, fee_rate, fund_nav_simulate)
            for single_account_values in account_values_simulate:
                # 记录账户终值
                final_values.append(single_account_values[-1])
                # 如果账户到达过目标值，记录一个成功
                #print(max(single_account_values))
                if single_account_values[-1] >= target_amount:
                    final_success_case_amount += 1
                if max(single_account_values) >= target_amount:
                    half_way_success_case_amount += 1
                    final_values_2.append(target_amount)
                else:
                    final_values_2.append(single_account_values[-1])
            # 计算均值
            expected_final_value = int(numpy.average(final_values))
            expected_final_value_2 = int(numpy.average(final_values_2))
            # 计算成功率
            total_cases = len(account_values_simulate)
            half_way_success_rate = 10000 * half_way_success_case_amount / total_cases / 100.00
            final_success_rate = 10000 * final_success_case_amount / total_cases / 100.00
            # 打印结果
            t = time.time() - t
            # print("计算耗时：" , t, "s")
            print("如果闭眼按计划投资，你的账户终值的预期值是%.2f万元，并有%.2f%%的概率在投资周期结束时实现目标。"%(expected_final_value/10000.0, final_success_rate))
            print("如果决定见好就收的话，你的账户终值的预期值是%.2f万元，你有%.2f%%的概率在投资周期结束时或者之前，实现投资目标。"%(expected_final_value_2/10000.0, half_way_success_rate))
            if (fund_code != const_values.special_code("ANUAL")):
                default_max_value = showchart(final_values, fund_code)
                showchart(final_values_2, fund_code, default_max_value)
            else:
                print("年金没有不确定性，不产生图表。")
    else:
        print ("错误信息：没有获取到净值历史，或者数据太少，无法完成操作。")

# 一次性投资结果显示
def show_single(fund_nav, terminate_years, init_amount, fee_rate, fund_code, target_amount):
    show_timing(fund_nav, 0, terminate_years, init_amount, fee_rate, fund_code, target_amount)

# 投资结果图表展示
def showchart(final_values, fund_code, default_max_value=0):
    expected_final_value = int(numpy.average(final_values))
    final_value_std = int(numpy.std(final_values))
    total_cases = len(final_values)

    d = max(min(expected_final_value // 5, final_value_std // 2), expected_final_value // 20 + 1, default_max_value // 20)
    num_bin = range(int(min(final_values)), max(default_max_value, min(expected_final_value + final_value_std * 6, int(max(final_values)))), d)
    plt.figure(figsize=(20,8),dpi=80)
    plt.hist(final_values, num_bin)
    plt.xticks(num_bin)
    plt.xlabel("Final value")
    plt.ylabel("Occurance in " + str(total_cases) + "cases")
    plt.title("Final value distribution under your plan, fund code:" + fund_code,size=25)
    plt.grid(alpha=2.0)
    plt.show()

    # 返回图表域最大值给下一次展示使用
    return min(expected_final_value + final_value_std * 6, int(max(final_values)))
