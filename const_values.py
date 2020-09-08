# 各种可能用到的常数

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

# 约定的报错时float的输出值
def get_error_float():
    return -4444.44

# 判断float是否报错值
def is_float_error(test_float):
    if abs(test_float - get_error_float()) <= zero_float():
        return True
    else:
        return False

# 默认趸交年金利率
def default_annual_return_rate():
    return 0.028

# “短期”的年数
def short_term():
    return 5