# 这个文件是财务数据处理的函数

import const_values

def data_source(income_active, income_passive, basic_expense, optional_expense, loan, loan_left, kid_expense, kid_left, insurance, insurance_left, retire_year, retire_income, inflation, income_growth):
    income_active_year = []      # 逐年主动收入
    income_passive_year = []     # 逐年被动收入
    basic_expense_year = []      # 逐年基本支出
    optional_expense_year = []   # 逐年可选支出
    loan_year = []               # 逐年贷款支出
    kid_expense_year = []        # 逐年子女支出
    insurance_year = []          # 逐年保险费用
    income_year = []             # 逐年总收入
    expense_year = []            # 逐年总支出
    net_cash_flow = []           # 净现金流

    # 退休后，可选消费维持原水平的年份
    year_after_retire_with_optional = const_values.year_after_retire_with_optional()
    # 退休一段是假后，可选消费从原水平逐渐递减为0的年份
    year_after_retire_with_optional_reduce = const_values.year_after_retire_with_optional_reduce()

    # 财务处理原则：分为退休前、退休后第一阶段、退休后第二阶段，一共三个阶段来估算
    # 假设用户已经妥善配置保险，因此不再考虑身故、疾病等风险，而假设用户健健康康，并且活到退休后40年（年数可通过const_values调节返回值来控制）
    # 主动收入受到收入增长系数调节，退休当年按照退休替代率打折
    # 被动收入受到【通胀率】调节
    # 贷款、保险费用不涨
    # 其他开支按照通胀率调节
    # 退休前的财务情况
    for i in range(retire_year):
        if i == 0:
            income_active_year.append(income_active * 1.0)
            income_passive_year.append(income_passive * 1.0)
            basic_expense_year.append(basic_expense * 1.0)
            optional_expense_year.append(optional_expense * 1.0)
            loan_year.append(loan * 1.0)
            kid_expense_year.append(kid_expense * 1.0)
            insurance_year.append(insurance * 1.0)
        else:
            income_active_year.append(income_active_year[-1] * (income_growth + 1.0))
            income_passive_year.append(income_passive_year[-1] * (inflation + 1.0))
            basic_expense_year.append(basic_expense_year[-1] * (inflation + 1.0))
            optional_expense_year.append(optional_expense_year[-1] * (inflation + 1.0))
            if loan_left > i:
                loan_year.append(loan * 1.0)
            else:
                loan_year.append(0.0)
            if kid_left > i:
                kid_expense_year.append(kid_expense_year[-1] * (inflation + 1.0))
            else:
                kid_expense_year.append(0.0)
            if insurance_left > i:
                insurance_year.append(insurance * 1.0)
            else:
                insurance_year.append(0.0)
    # 退休后第一阶段，可选消费维持原有水平
    for i in range(retire_year, retire_year + year_after_retire_with_optional):
        if i == retire_year:
            # 退休当年，用退休替代率处理主动收入
            income_active_year.append(income_active_year[-1] * (income_growth + 1.0) * retire_income)
        else:
            income_active_year.append(income_active_year[-1] * (income_growth + 1.0))
        income_passive_year.append(income_passive_year[-1] * (inflation + 1.0))
        basic_expense_year.append(basic_expense_year[-1] * (inflation + 1.0))
        optional_expense_year.append(optional_expense_year[-1] * (inflation + 1.0))
        if loan_left > i:
            loan_year.append(loan * 1.0)
        else:
            loan_year.append(0.0)
        if kid_left > i:
            kid_expense_year.append(kid_expense_year[-1] * (inflation + 1.0))
        else:
            kid_expense_year.append(0.0)
        if insurance_left > i:
            insurance_year.append(insurance * 1.0)
        else:
            insurance_year.append(0.0)
    
    # 退休后第二阶段，可选消费递减到0
    for i in range(retire_year + year_after_retire_with_optional, retire_year + year_after_retire_with_optional + year_after_retire_with_optional_reduce):
        income_active_year.append(income_active_year[-1] * (income_growth + 1.0))
        income_passive_year.append(income_passive_year[-1] * (inflation + 1.0))
        basic_expense_year.append(basic_expense_year[-1] * (inflation + 1.0))
        # 可选消费递减处理
        optional_expense_year.append(optional_expense_year[-1] * (inflation + 1.0) * (retire_year + year_after_retire_with_optional + year_after_retire_with_optional_reduce - i) / year_after_retire_with_optional_reduce)
        loan_year.append(0.0)
        kid_expense_year.append(0.0)
        insurance_year.append(0.0)
    # 计算全部年份的收支各自汇总
    for i in range(retire_year + year_after_retire_with_optional + year_after_retire_with_optional_reduce):
        income_year.append(income_active_year[i] + income_passive_year[i])
        expense_year.append(basic_expense_year[i] + optional_expense_year[i] + loan_year[i] + kid_expense_year[i] + insurance_year[i])
        net_cash_flow.append(income_year[i] - expense_year[i])
    return income_year, expense_year, net_cash_flow

# 把现金流拆分成退休前后的
def split_cash_flow(net_cash_flow, retire_year):
    cf_before_retire = []
    cf_after_retire = []
    year_after_retire_with_optional = const_values.year_after_retire_with_optional()
    year_after_retire_with_optional_reduce = const_values.year_after_retire_with_optional_reduce()
    # TODO:退休前现金流应该结合当前现金做正负方向的调整
    for i in range(retire_year):
        cf_before_retire.append(net_cash_flow[i])
    for i in range(year_after_retire_with_optional + year_after_retire_with_optional_reduce):
        cf_after_retire.append(net_cash_flow[i + retire_year])
    return cf_before_retire,cf_after_retire

# 可投资现金流是退休前的现金流，并且把建议的存量金融投资资产一次性加入首年，未来算法可以进一步优化
def get_investable_cf(suggested_non_liquidity, cf_before_retire):
    cf_investable = []
    i = 0
    for value in cf_before_retire:
        if i == 0:
            cf_investable.append(suggested_non_liquidity + value)
        else:
            cf_investable.append(value)
        i += 1
    return cf_investable