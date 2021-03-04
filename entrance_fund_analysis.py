# -*- coding: utf-8 -*-
# 基金分析的调试入口

import internal_questionnaire
import internal_fund_data_process
import const_values
import util_func
import output_fund

# 调试入口：单个基金的历史分析输出
if __name__ == "__main__":
    tips = "AI吴小蔚为你服务。请确保要分析的基金净值数据已经导入到./history/文件夹。"
    
    print(tips)
    fund_code, fund_nav = internal_questionnaire.fund_analysis()
    while not util_func.isExitCode(fund_code):
        if fund_code == "list":
            # 此处括号中可以加入参数，参数是收益基准值（日），用(年利率+1)^(1/244)-1获取
            output_fund.show_list(0.0004)   
        else:
            output_fund.show_single_fund_mean_and_var(fund_code, fund_nav)
            fund_code, fund_nav = internal_questionnaire.fund_analysis()
    exit()