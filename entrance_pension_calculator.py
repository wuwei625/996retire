import internal_family_data
import internal_questionnaire
import algorithm_tvm
import ai_finance_plan
import const_values
import util_func
import output_fund

# 调试入口：退休计算器
if __name__ == "__main__":
    # 用户输入数据
    income_active, income_passive, basic_expense, optional_expense, loan, loan_left, kid_expense, kid_left, insurance, insurance_left, retire_year, retire_income, inflation, current_liquidity, current_non_liquidity, income_growth = internal_questionnaire.family_raw_data()
    # 数据标准化处理
    income_year, expense_year, net_cash_flow = internal_family_data.data_source(income_active, income_passive, basic_expense, optional_expense, loan, loan_left, kid_expense, kid_left, insurance, insurance_left, retire_year, retire_income, inflation, income_growth)
    # 给出当前资产的分配建议
    ideal_liquidity, suggested_liquidity, suggested_non_liquidity = ai_finance_plan.current_asset_reallocation(income_year, expense_year, current_liquidity, current_non_liquidity)
    if ideal_liquidity > suggested_liquidity:
        print("你目前的财务状况不太健康，建议你至少保留%i元流动资产，但是你即使变现投资资产之后，也最多只有%i元，建议你慎重规划家庭财务。"%(ideal_liquidity, suggested_liquidity))
    else:
        print("建议你保留%i元流动资产，把投资性金融资产调整为%i元。"%(suggested_liquidity, suggested_non_liquidity))
    # 拆分退休前后现金流
    cf_before_retire, cf_after_retire = internal_family_data.split_cash_flow(net_cash_flow, retire_year)
    # 修正投资资产现金流
    cf_investable = internal_family_data.get_investable_cf(suggested_non_liquidity, cf_before_retire)
    # 计算退休目标
    default_annual_return_rate = const_values.default_annual_return_rate()
    retire_fund_target = 0.0 - algorithm_tvm.get_npv(cf_after_retire, default_annual_return_rate)
    if (retire_fund_target > 1.0):
        irr_need = algorithm_tvm.get_irr(cf_investable, retire_fund_target)
        print("如果你想在退休后维持当前生活品质，你需要在退休时候攒出%.2f万元"%(retire_fund_target / 10000.0))
        if util_func.is_float_non_sense(irr_need):
            print("但是我算不出来你需要怎么投资才行，不排除你填是数据是错的。")
        else:
            print("你需要将现有投资性金融资产和每年结余以%.2f%%的收益率进行运用，才能达到目标。"%(irr_need * 100))
            print("以这个收益率进行运用并达到退休目标的前提是，没有任何低于预期的波动，因此通常你可能需要配置预期收益更高的风险性投资资产。")
            print("以下基金可供参考（已根据你的目标进行优先排序）：")
            output_fund.show_list((1 + irr_need) ** (1 / const_values.period_times("DAY")) - 1.0)