import get_fund_nav_from_file
import get_mean_and_var_from_history_nav
import monte_carlo
import timing_invest_simulate
import const_values
import numpy
import time

# 调试入口：单个基金的定投模拟结果输出
if __name__ == "__main__":
    tips = "AI吴小蔚梦游中为你服务，请勿当真。请确保要模拟的基金净值数据已经导入到./history/文件夹。"
    tips_code = "输入要定投基金代码，输入0退出。（特殊代码：1：保险年金；2：沪深300；3：中证500；4：上证50；5：创业板）"
    tips_month_amount = "你每月想定投多少钱（按周定投没写，要的话自己改程序）？比如1000块就输入1000："
    tips_years = "你想定投几年？"
    tips_fee_rate = "交易手续费是百分几？输入0.5表示0.5%："
    tips_target_amount = "你觉得有多少钱算养老自由？比如想100万就输入1000000："
    tips_stupid = "你他妈输入的啥玩意儿"

    print(tips)
    month_amount = int(input(tips_month_amount))
    years = int(input(tips_years))
    target_amount = int(input(tips_target_amount))

    fund_code = input(tips_code)
    while fund_code != "0":
        # 先查询历史净值
        fund_history_filename = "./history/" + fund_code + ".txt"
        fund_nav = get_fund_nav_from_file.do_get(fund_history_filename)
        # 至少需要10个值才有意义执行下一步
        nav_amount = len(fund_nav)
        final_values = []
        success_case_amount = 0
        if nav_amount > 10:
            fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var = get_mean_and_var_from_history_nav.analysis_fund(fund_nav, 0)
            if (abs(fund_nav_increase_logarithm_mean) > const_values.zero_float() or abs(fund_nav_increase_logarithm_var) > const_values.zero_float()):
                
                fee_rate = float(input(tips_fee_rate)) / 100.0
                
                if (target_amount < month_amount or years < 1 or month_amount < 1 or fee_rate < const_values.zero_float("NEG") or fee_rate > const_values.max_fee_rate()):
                    print(tips_stupid)
                else:
                    # 修正费率
                    if fee_rate < const_values.zero_float():
                        fee_rate = 0.0
                    # 获取test_times组模拟净值
                    fund_nav_simulate = monte_carlo.get_nav_matrix(fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var, const_values.test_times(), years * const_values.days("YEAR"))
                    # 获取对应的账户价值
                    account_values_simulate = timing_invest_simulate.get_simulated_asset_values(const_values.days("MONTH"), month_amount, fee_rate, fund_nav_simulate)
                    for single_account_values in account_values_simulate:
                        # 记录账户终值
                        final_values.append(single_account_values[-1])
                        # 如果账户到达过目标值，记录一个成功
                        #print(max(single_account_values))
                        if max(single_account_values) >= target_amount:
                            success_case_amount += 1
                    # 计算均值
                    expected_final_value = int(numpy.average(final_values))
                    # 计算成功率
                    success_rate_bp = 10000 * success_case_amount / len(account_values_simulate)
                    success_rate_float = success_rate_bp / 100.00
                    # 打印结果
                    print("如果闭眼按计划定投，你的账户终值的预期值是" + str(expected_final_value) + "元。")
                    print("如果决定见好就收的话，你有" + str(success_rate_float) + "%的概率在投资周期结束时或者之前，实现养老自由。")
            else:
                print("错误信息：基金历史未获得正确结果！")
        else:
            print ("错误信息：没有获取到净值历史，或者数据太少，无法完成操作。")
        fund_code = input(tips_code)