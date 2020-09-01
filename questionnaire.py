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
# 调试入口：家庭问卷
if __name__ == "__main__":
    tips = "AI吴小蔚梦游中为你服务，请勿当真。\n程序可以离线运行，隐私随便说。"#\n请确保要模拟的基金净值数据已经导入到./history/文件夹。"
    tips_income_active = "家庭年收入（主动收入，单位：元）？"
    tips_income_passive = "家庭年被动收入（诸如收租子、家庭信托等，单位：元）？"
    tips_basic_expense = "家庭每年基本生活支出（单位：元）？"
    tips_optional_expense = "家庭每年享受生活支出（单位：元）？"
    tips_loan = "每年还贷多少钱（单位：元）？"
    tips_loan_left = "贷款还要还几年？"
    tips_kid_expense = "每年养娃（所有的娃一共）多少钱（单位：元）？"
    tips_kid_left = "娃还要啃你们多少年？"
    tips_insurance = "每年买保险多少钱（不知道怎么买保险或者被忽悠了可以搜小程序理先生，本程序不管）（单位：元）？"
    tips_insurance_left = "保险还要交几年？"
    tips_retire_year = "你们想几年后退休？"
    tips_retire_income = "退休后收入预计占现在主动收入的百分比（25%的话写25，收入在社保封顶线附近大约25）？"
    tips_inflation = "你觉得通胀百分几（3%写3，我觉得3差不多）？"
    tips_income_growth = "你觉得收入增长百分几（4%写4，你要不会写就写4吧）？"
    tips_stupid = "你他妈输入的啥玩意儿"

    print(tips)
    income_active = int(input(tips_income_active))
    while income_active < 1:
        print(tips_stupid)
        income_active = int(input(tips_income_active))
    income_passive = int(input(tips_income_passive))
    while income_passive < 0:
        print(tips_stupid)
        income_passive = int(input(tips_income_passive))
    basic_expense = int(input(tips_basic_expense))
    while basic_expense < 1:
        print(tips_stupid)
        basic_expense = int(input(tips_basic_expense))
    optional_expense = int(input(tips_optional_expense))
    while optional_expense < 0:
        print(tips_stupid)
        optional_expense = int(input(tips_optional_expense))
    loan = int(input(tips_loan))
    while loan < 0:
        print(tips_stupid)
        loan = int(input(tips_loan))
    loan_left = int(input(tips_loan_left))
    while loan_left < 0:
        print(tips_stupid)
        loan_left = int(input(tips_loan_left))
    kid_expense = int(input(tips_kid_expense))
    while kid_expense < 0:
        print(tips_stupid)
        kid_expense = int(input(tips_kid_expense))
    kid_left = int(input(tips_kid_left))
    while kid_left < 0:
        print(tips_stupid)
        kid_left = int(input(tips_kid_left))
    insurance = int(input(tips_insurance))
    while insurance < 0:
        print(tips_stupid)
        insurance = int(input(tips_insurance))
    insurance_left = int(input(tips_insurance_left))
    while insurance_left < 0:
        print(tips_stupid)
        insurance_left = int(input(tips_insurance_left))
    retire_year = int(input(tips_retire_year))
    while retire_year < 0:
        print(tips_stupid)
        retire_year = int(input(tips_retire_year))
    retire_income = float(input(tips_retire_income)) / 100.0
    while retire_income < 0.0:
        print(tips_stupid)
        float(input(tips_retire_income)) / 100.0
    inflation = float(input(tips_inflation)) / 100.0
    while inflation < -0.1 or inflation > 0.2:
        print(tips_stupid)
        inflation = float(input(tips_inflation)) / 100.0
    income_growth = float(input(tips_income_growth)) / 100.0
    while income_growth < -0.1 or income_growth > 0.2:
        print(tips_stupid)
        income_growth = float(input(tips_income_growth)) / 100.0