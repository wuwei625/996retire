import data_source
import questionnaire
import tvm
import const_values

# 调试入口：退休计算器
if __name__ == "__main__":
    # 用户输入数据
    income_active, income_passive, basic_expense, optional_expense, loan, loan_left, kid_expense, kid_left, insurance, insurance_left, retire_year, retire_income, inflation, income_growth = questionnaire.family_raw_data()
    # 数据标准化处理
    income_year, expense_year, net_cash_flow = data_source.init_data_source(income_active, income_passive, basic_expense, optional_expense, loan, loan_left, kid_expense, kid_left, insurance, insurance_left, retire_year, retire_income, inflation, income_growth)
    cf_before_retire,cf_after_retire = data_source.split_cash_flow(net_cash_flow, retire_year)
    retire_fund_target = 0.0 - tvm.get_npv(cf_after_retire, inflation)
    if (retire_fund_target > 1.0):
        irr_need = tvm.get_irr(cf_before_retire, retire_fund_target)
        print("如果你想在退休后维持当前生活品质，你需要在退休时候攒出%.2f万元"%(retire_fund_target / 10000.0))
        if const_values.is_float_error(irr_need):
            print("但是我算不出来你需要怎么投资才行，不排除你填是数据是错的。")
        else:
            print("你需要将现有资产和每年结余以%.2f%%的收益率进行运用，才能达到目标"%(irr_need * 100))