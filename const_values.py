# 各种可能用到的常数

# 公共提示信息
def tips_ask_fund():
    return "输入基金代码，输入0退出。（特殊代码：1：保险年金；2：沪深300；3：中证500；4：上证50；5：创业板；list：查看所有）"

def tips_stupid():
    return "你他妈输入的啥玩意儿"

def tips_fund_error():
    return "没找到这个基金，或者这个基金的可用数据太少，请换一个。"
    
# 历史数据路径
def history_path():
    return "./history/"

def special_code(special_type = "EXIT"):
    if special_type == "EXIT":
        return "0"
    elif special_type == "ANNUAL":
        return "1"
    elif special_type == "LS":
        return "list"
    else:
        return "0"
        
# 周期内交易日数量
def days(days_type):
    if days_type == "YEAR":
        return 244
    elif days_type == "MONTH":
        return 20
    elif days_type == "WEEK":
        return 5
    else:
        return 1

# 一年的投资周期数量
def period_times(period_type = "MONTH"):
    if period_type == "MONTH":
        return 12
    elif period_type == "DAY":
        return 244
    elif period_type == "WEEK":
        return 50
    elif period_type == "YEAR":
        return 1
    else:
        return 1

# float的0
def zero_float(zero_type=""):
    if (zero_type == "NEG"):
        return -0.00000000000000001
    else:
        return 0.00000000000000001

# 费率上限
def max_fee_rate():
    return 10.0

# 蒙特卡洛测试次数
def test_times():
    return 7000

# 退休后第一阶段时长（维持可选消费标准不变的时间）
def year_after_retire_with_optional():
    return 20

# 退休后第一阶段时长（消费标准逐年递减的时间）
def year_after_retire_with_optional_reduce():
    return 40

# 算irr的初始测试值
def irr_guess():
    return 0.05

# 算irr误差收敛
def error_tolerance():
    return 0.1

# 算irr重试次数最大
def irr_retry_limit():
    return 100000

# 约定的无意义时float的输出值
def get_non_sense_float():
    return -4444.44

# 默认趸交年金利率
def default_annual_return_rate():
    return 0.028

# “短期”的年数
def short_term():
    return 5