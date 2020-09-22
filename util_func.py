# 基本的处理逻辑函数
import const_values

# 判断float为0
def is_float_zero(test_float):
    return abs(test_float) <= const_values.zero_float()

# 判断float是否报错值
def is_float_error(test_float):
    return is_float_zero(test_float - const_values.get_error_float())

def isExitCode(code):
    return code == const_values.special_code("EXIT")

def isAnnualCode(code):
    return code == const_values.special_code("ANNUAL")

def isLs(code):
    return code == const_values.special_code("LS")