import const_values

def datasource(income_active, income_passive, basic_expense, optional_expense, loan, loan_left, kid_expense, kid_left, insurance, insurance_left, retire_year, retire_income, inflation, income_growth):
    income_active_total_year = []
    income_passive_total_year = []
    basic_expense_year = []
    optional_expense_year = []
    loan_year = []
    kid_expense_year = []
    insurance_year = []
    income_year = []
    expense_year = []

    # 退休后，可选消费维持原水平的年份
    year_after_retire_with_optional = const_values.year_after_retire_with_optional()
    # 退休一段是假后，可选消费从原水平逐渐递减为0的年份
    year_after_retire_with_optional_reduce = const_values.year_after_retire_with_optional_reduce

    for i in range(retire_year):
        if i == 0:
            income_active_total_year.append(income_active * 1.0)
            income_passive_total_year.append(income_passive * 1.0)
            basic_expense_year.append(basic_expense * 1.0)
            optional_expense_year.append(optional_expense * 1.0)
            loan_year.append(loan * 1.0)
            kid_expense_year.append(kid_expense * 1.0)
            insurance_year.append(insurance * 1.0)
        else:
            income_active_total_year.append(income_active_total_year[-1] * (income_growth + 1.0))
            income_passive_total_year.append(income_passive_total_year[-1] * (income_growth + 1.0))
            basic_expense_year.append(basic_expense_year[-1] * (inflation + 1.0))
            optional_expense_year.append(optional_expense_year[-1] * (inflation + 1.0))
            if loan_left > i:
                loan_year.append(loan * 1.0)
            else:
                loan_year.append(0.0)
            if kid_expense_year > i:
                kid_expense_year.append(kid_expense_year[-1] * (inflation + 1.0))
            else:
                kid_expense_year.append(0.0)
            if insurance_left > i:
                insurance_year.append(insurance * 1.0)
            else:
                insurance_year.append(0.0)
    for i in range(retire_year, retire_year + year_after_retire_with_optional):
        if i == retire_year:
            # 退休当年，用退休替代率处理主动收入
            income_active_total_year.append(income_active_total_year[-1] * (income_growth + 1.0) * retire_income)
        else:
            income_active_total_year.append(income_active_total_year[-1] * (income_growth + 1.0))
        income_passive_total_year.append(income_passive_total_year[-1] * (income_growth + 1.0))
        basic_expense_year.append(basic_expense_year[-1] * (inflation + 1.0))
        optional_expense_year.append(optional_expense_year[-1] * (inflation + 1.0))
        if loan_left > i:
            loan_year.append(loan * 1.0)
        else:
            loan_year.append(0.0)
        if kid_expense_year > i:
            kid_expense_year.append(kid_expense_year[-1] * (inflation + 1.0))
        else:
            kid_expense_year.append(0.0)
        if insurance_left > i:
            insurance_year.append(insurance * 1.0)
        else:
            insurance_year.append(0.0)
    for i in range(retire_year + year_after_retire_with_optional, retire_year + year_after_retire_with_optional + year_after_retire_with_optional_reduce):
        income_active_total_year.append(income_active_total_year[-1] * (income_growth + 1.0))
        income_passive_total_year.append(income_passive_total_year[-1] * (income_growth + 1.0))
        basic_expense_year.append(basic_expense_year[-1] * (inflation + 1.0))
        # 可选消费递减处理
        optional_expense_year.append(optional_expense_year[-1] * (inflation + 1.0) * (retire_year + year_after_retire_with_optional + year_after_retire_with_optional_reduce - i) / year_after_retire_with_optional_reduce)
        loan_year.append(0.0)
        kid_expense_year.append(0.0)
        insurance_year.append(0.0)
    # 接下来需要计算收支各自汇总