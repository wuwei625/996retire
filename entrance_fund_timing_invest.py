# -*- coding: utf-8 -*-
# 基金定投的调试入口

import internal_questionnaire
import internal_fund_data_process
import algorithm_monte_carlo
import internal_timing_invest_simulate
import const_values
import util_func
import output_fund



# 调试入口：单个基金的定投模拟结果输出
if __name__ == "__main__":
    tips = "AI吴小蔚梦游中为你服务，请勿当真。请确保要模拟的基金净值数据已经导入到./history/文件夹。"
    print(tips)
    fund_code, fund_nav, month_amount, invest_years, terminate_years, fee_rate, target_amount = internal_questionnaire.fund_invest()
    while not util_func.isExitCode(fund_code):
        if util_func.isLs(fund_code):
            output_fund.show_list()
        else:
            output_fund.show_timing(fund_nav, invest_years, terminate_years, month_amount, fee_rate, fund_code, target_amount)
        fund_code, fund_nav, month_amount, invest_years, terminate_years, fee_rate, target_amount = internal_questionnaire.fund_invest()
    exit()