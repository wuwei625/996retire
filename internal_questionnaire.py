import internal_fund_data_process
import const_values

def family_raw_data():
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
    tips_current_liquidity = "你家目前的净流动资产有多少？（存款+货币基金+银行短期理财-信用卡等短期负债，单位：元）"
    tips_current_non_liquidity = "你家目前的投资性金融资产有多少？（非货币基金、股票、万能投连险等用于投资增值的资产，单位：元）"
    tips_inflation = "你觉得通胀百分几（3%写3，我觉得3差不多）？"
    tips_income_growth = "你觉得收入增长百分几（3%写3，你要不会写就写3吧）？"
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
    current_liquidity = int(input(tips_current_liquidity))
    current_non_liquidity = int(input(tips_current_non_liquidity))
    while current_non_liquidity < 0:
        print(tips_stupid)
        current_non_liquidity = int(input(tips_current_non_liquidity))
    inflation = float(input(tips_inflation)) / 100.0
    while inflation < -0.1 or inflation > 0.2:
        print(tips_stupid)
        inflation = float(input(tips_inflation)) / 100.0
    income_growth = float(input(tips_income_growth)) / 100.0
    while income_growth < -0.1 or income_growth > 0.2:
        print(tips_stupid)
        income_growth = float(input(tips_income_growth)) / 100.0

    return income_active, income_passive, basic_expense, optional_expense, loan, loan_left, kid_expense, kid_left, insurance, insurance_left, retire_year, retire_income, inflation,current_liquidity, current_non_liquidity, income_growth

def fund_analysis():
    tips_code = "输入基金代码，输入0退出。（特殊代码：1：保险年金；2：沪深300；3：中证500；4：上证50；5：创业板）"
    tips_fund_error = "没找到这个基金，或者这个基金的可用数据太少，请换一个。"
    
    fund_code = input(tips_code)
    if fund_code != "0":
        # 先查询历史净值
        fund_history_filename = "./history/" + fund_code + ".txt"
        fund_nav = internal_fund_data_process.do_get(fund_history_filename)
        nav_amount = len(fund_nav)
        # 至少需要10个值才有意义处理这个基金
        while nav_amount < 10 and (fund_code != "0"):
            print(tips_fund_error)
            fund_code = input(tips_code)
            fund_history_filename = "./history/" + fund_code + ".txt"
            fund_nav = internal_fund_data_process.do_get(fund_history_filename)
            nav_amount = len(fund_nav)
    # 此处不用else是因为可能用户重新输入的code为0，需要再判断
    if fund_code == "0":
        return "0", "0"

    
    return fund_code, fund_nav

def fund_invest():
    tips_code = "输入基金代码，输入0退出。（特殊代码：1：保险年金；2：沪深300；3：中证500；4：上证50；5：创业板）"
    tips_month_amount = "你每月想定投多少钱（按周定投没写，要的话自己改程序）？比如1000块就输入1000："
    tips_invest_years = "你想定投几年？"
    tips_terminate_years = "从第一笔开始算，几年结束投资？"
    tips_fee_rate = "交易手续费是百分几？输入0.5表示0.5%："
    tips_target_amount = "你觉得有多少钱算养老自由？比如想100万就输入1000000："
    tips_fund_error = "没找到这个基金，或者这个基金的可用数据太少，请换一个。"
    tips_stupid = "你他妈输入的啥玩意儿"
    
    fund_code = input(tips_code)
    if fund_code != "0":
        # 先查询历史净值
        fund_history_filename = "./history/" + fund_code + ".txt"
        fund_nav = internal_fund_data_process.do_get(fund_history_filename)
        nav_amount = len(fund_nav)
        # 至少需要10个值才有意义处理这个基金
        while nav_amount < 10 and (fund_code != "0"):
            print(tips_fund_error)
            fund_code = input(tips_code)
            fund_history_filename = "./history/" + fund_code + ".txt"
            fund_nav = internal_fund_data_process.do_get(fund_history_filename)
            nav_amount = len(fund_nav)
    # 此处不用else是因为可能用户重新输入的code为0，需要再判断
    if fund_code == "0":
            return "0", "0", "0", "0", "0", "0", "0"

    month_amount = int(input(tips_month_amount))
    invest_years = int(input(tips_invest_years))
    terminate_years = int(input(tips_terminate_years))
    fee_rate = float(input(tips_fee_rate)) / 100.0
    target_amount = int(input(tips_target_amount))

    while target_amount < month_amount or invest_years < 1 or terminate_years < invest_years or month_amount < 1 or fee_rate < const_values.zero_float("NEG") or fee_rate > const_values.max_fee_rate():
        print(tips_stupid)
        month_amount = int(input(tips_month_amount))
        invest_years = int(input(tips_invest_years))
        terminate_years = int(input(tips_terminate_years))
        fee_rate = float(input(tips_fee_rate)) / 100.0
        target_amount = int(input(tips_target_amount))
    # 手续费0的修正
    if fee_rate < const_values.zero_float():
        fee_rate = 0.0
    return fund_code, fund_nav, month_amount, invest_years, terminate_years, fee_rate, target_amount
