import questionnaire
import get_mean_and_var_from_history_nav
import monte_carlo
import timing_invest_simulate
import const_values
import numpy
import time

from matplotlib import pyplot as plt
from matplotlib import font_manager


def show(fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var, years, month_amount, fee_rate, fund_code):
    final_values = []
    half_way_success_case_amount = 0
    final_success_case_amount = 0
    t = time.time()
    # 获取test_times组模拟净值
    fund_nav_simulate = monte_carlo.get_nav_matrix(fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var, const_values.test_times(), years * const_values.days("YEAR"))
    # 获取对应的账户价值
    account_values_simulate = timing_invest_simulate.get_simulated_asset_values(const_values.days("MONTH"), month_amount, fee_rate, fund_nav_simulate)
    for single_account_values in account_values_simulate:
        # 记录账户终值
        final_values.append(single_account_values[-1])
        # 如果账户到达过目标值，记录一个成功
        #print(max(single_account_values))
        if single_account_values[-1] >= target_amount:
            final_success_case_amount += 1
        if max(single_account_values) >= target_amount:
            half_way_success_case_amount += 1
    # 计算均值
    expected_final_value = int(numpy.average(final_values))
    # 计算成功率
    total_cases = len(account_values_simulate)
    half_way_success_rate = 10000 * half_way_success_case_amount / total_cases / 100.00
    final_success_rate = 10000 * final_success_case_amount / total_cases / 100.00
    # 打印结果
    t = time.time() - t
    # print("计算耗时：" , t, "s")
    print("如果闭眼按计划定投，你的账户终值的预期值是" + str(expected_final_value) + "元，并有" + str(final_success_rate) + "%的概率在投资周期结束时实现养老自由。")
    print("如果决定见好就收的话，你有" + str(half_way_success_rate) + "%的概率在投资周期结束时或者之前，实现养老自由。")
    if (fund_code != "1"):
        showchart(final_values, fund_code)
    else:
        print("年金没有不确定性，不产生图表。")

def showchart(final_values, fund_code):
    expected_final_value = int(numpy.average(final_values))
    final_value_std = int(numpy.std(final_values))
    total_cases = len(final_values)

    d = max(min(expected_final_value // 5, final_value_std // 2), expected_final_value // 20 + 1)
    num_bin = range(int(min(final_values)), min(final_value_std * 4, int(max(final_values))), d)
    plt.figure(figsize=(20,8),dpi=80)
    plt.hist(final_values, num_bin)
    plt.xticks(num_bin)
    plt.xlabel("Final value")
    plt.ylabel("Occurance in " + str(total_cases) + "cases")
    plt.title("Final value distribution under your plan, fund code:" + fund_code,size=25)
    plt.grid(alpha=2.0)
    plt.show()

# 调试入口：单个基金的定投模拟结果输出
if __name__ == "__main__":
    tips = "AI吴小蔚梦游中为你服务，请勿当真。请确保要模拟的基金净值数据已经导入到./history/文件夹。"
    print(tips)
    fund_code, fund_nav, month_amount, years, fee_rate, target_amount = questionnaire.fund_invest()
    while fund_code != "0":
        nav_amount = len(fund_nav)
        if nav_amount > 10:
            fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var = get_mean_and_var_from_history_nav.analysis_fund(fund_nav, 0)
            if (abs(fund_nav_increase_logarithm_mean) > const_values.zero_float() or abs(fund_nav_increase_logarithm_var) > const_values.zero_float()):
                show(fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var, years, month_amount, fee_rate, fund_code)
            else:
                print("错误信息：基金历史未获得正确结果！")
        else:
            print ("错误信息：没有获取到净值历史，或者数据太少，无法完成操作。")
        fund_code, fund_nav, month_amount, years, fee_rate, target_amount = questionnaire.fund_invest()
    exit()